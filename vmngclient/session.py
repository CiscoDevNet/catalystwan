from __future__ import annotations

import logging
import time
from enum import Enum
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, List, Optional, Union
from urllib.parse import urljoin

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Request, Response, Session, head
from requests.auth import AuthBase
from requests.exceptions import ConnectionError, HTTPError, RequestException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.api.api_containter import APIContainter
from vmngclient.exceptions import (
    AuthenticationError,
    CookieNotValidError,
    InvalidOperationError,
    SessionNotCreatedError,
    TenantSubdomainNotFound,
    vManageClientError,
)
from vmngclient.primitives.client import AboutInfo, ServerInfo
from vmngclient.primitives.primitive_container import APIPrimitiveContainter
from vmngclient.response import ErrorInfo, response_history_debug, vManageResponse
from vmngclient.utils.session_type import SessionType
from vmngclient.vmanage_auth import vManageAuth

JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]


class vManageBadRequestError(vManageClientError):
    """Indicates that vManage returned HTTP status code 400.

    A 400 Bad Request response status code indicates that the server
    could not understand the request due to invalid syntax,
    malformed request message, or missing request parameters.
    """

    def __init__(self, error_info: Optional[ErrorInfo], response: vManageResponse):
        self.response = response
        self.info = error_info
        super().__init__(error_info)


class UserMode(Enum):
    PROVIDER = "provider"
    TENANT = "tenant"
    NOT_RECOGNIZED = "not recognized"
    NOT_FOUND = "not found"


class ViewMode(Enum):
    PROVIDER = "provider"
    TENANT = "tenant"
    NOT_RECOGNIZED = "not recognized"
    NOT_FOUND = "not found"


def create_vManageSession(
    url: str,
    username: str,
    password: str,
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> vManageSession:
    """Factory function that creates session object based on provided arguments.

    Args:
        url (str): IP address or domain name
        username (str): username
        password (str): password
        port (int): port
        subdomain: subdomain specifying to which view switch when creating provider as a tenant session,
            works only on provider user mode
        logger: logger for logging API requests

    Returns:
        Session object

    """
    session = vManageSession(url=url, username=username, password=password, port=port, subdomain=subdomain)
    session.auth = vManageAuth(session.base_url, username, password, verify=False)
    if logger:
        session.logger = logger
        session.auth.logger = logger

    if subdomain:
        tenant_id = session.get_tenant_id()
        vsession_id = session.get_virtual_session_id(tenant_id)
        session.headers.update({"VSessionId": vsession_id})

    try:
        server_info = session.server()
    except InvalidOperationError:
        server_info = ServerInfo.parse_obj({})

    session.server_name = server_info.server
    session.on_session_create_hook()

    try:
        user_mode = UserMode(server_info.user_mode or "not found")
    except ValueError:
        user_mode = UserMode.NOT_RECOGNIZED
        session.logger.warning(f"Unrecognized user mode is: '{server_info.user_mode}'")

    try:
        view_mode = ViewMode(server_info.view_mode or "not found")
    except ValueError:
        view_mode = ViewMode.NOT_RECOGNIZED
        session.logger.warning(f"Unrecognized user mode is: '{server_info.view_mode}'")

    if user_mode is UserMode.TENANT and not subdomain and view_mode is ViewMode.TENANT:
        session._session_type = SessionType.TENANT
    elif user_mode is UserMode.PROVIDER and not subdomain and view_mode is ViewMode.PROVIDER:
        session._session_type = SessionType.PROVIDER
    elif user_mode is UserMode.PROVIDER and view_mode is ViewMode.TENANT:
        session._session_type = SessionType.PROVIDER_AS_TENANT
    elif user_mode is UserMode.TENANT and subdomain:
        raise SessionNotCreatedError(
            f"Session not created. Subdomain {subdomain} passed to tenant session, "
            "cannot switch to tenant from tenant user mode."
        )
    else:
        session._session_type = SessionType.NOT_DEFINED
        session.logger.warning(f"Session created with {user_mode} and {view_mode}.")

    session.logger.info(
        f"Logged to vManage({session.platform_version}) as {username}. The session type is {session.session_type}"
    )
    return session


class vManageResponseAdapter(Session):
    def request(self, method, url, *args, **kwargs) -> vManageResponse:
        return vManageResponse(super().request(method, url, *args, **kwargs))

    def get(self, url, *args, **kwargs) -> vManageResponse:
        return vManageResponse(super().get(url, *args, **kwargs))

    def post(self, url, *args, **kwargs) -> vManageResponse:
        return vManageResponse(super().post(url, *args, **kwargs))

    def put(self, url, *args, **kwargs) -> vManageResponse:
        return vManageResponse(super().put(url, *args, **kwargs))

    def delete(self, url, *args, **kwargs) -> vManageResponse:
        return vManageResponse(super().delete(url, *args, **kwargs))


class vManageSession(vManageResponseAdapter):
    """Base class for API sessions for vManage client.

    Defines methods and handles session connectivity available for provider, provider as tenant, and tenant.

    Args:
        url: IP address or domain name, i.e. '10.0.1.200' or 'example.com'
        port: port
        username: username
        password: password

    Attributes:
        enable_relogin (bool): defaults to True, in case that session is not properly logged-in, session will try to
            relogin and try the same request again
    """

    on_session_create_hook: ClassVar[Callable[[vManageSession], Any]] = lambda *args: None

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        verify: bool = False,
        port: Optional[int] = None,
        subdomain: Optional[str] = None,
        auth: Optional[AuthBase] = None,
    ):
        self.url = url
        self.port = port
        self.base_url = self.__create_base_url()
        self.username = username
        self.password = password
        self.subdomain = subdomain

        self._session_type = SessionType.NOT_DEFINED
        self.server_name: Optional[str] = None
        self.logger = logging.getLogger(__name__)
        self.enable_relogin: bool = True
        self.__second_relogin_try: bool = False
        self.response_trace: Callable[
            [Optional[Response], Union[Request, PreparedRequest, None]], str
        ] = response_history_debug
        super(vManageSession, self).__init__()
        self.__prepare_session(verify, auth)

        self.api = APIContainter(self)
        self.primitives = APIPrimitiveContainter(self)
        self._platform_version: Version
        self._api_version: Version

    def request(self, method, url, *args, **kwargs) -> vManageResponse:
        full_url = self.get_full_url(url)
        try:
            response = super(vManageSession, self).request(method, full_url, *args, **kwargs)
            self.logger.debug(self.response_trace(response, None))
        except RequestException as exception:
            self.logger.debug(self.response_trace(exception.response, exception.request))
            self.logger.error(exception)
            raise
        except CookieNotValidError as exception:
            if self.enable_relogin and not self.__second_relogin_try:
                self.logger.warning(f"Loging to session again. Reason: '{str(exception)}'")
                self.auth = vManageAuth(self.base_url, self.username, self.password, verify=False)
                self.__second_relogin_try = True
                return self.request(method, url, *args, **kwargs)
            elif self.enable_relogin and self.__second_relogin_try:
                raise AuthenticationError("Session is not properly logged in and relogin failed.")
            else:
                raise AuthenticationError("Session is not properly logged in and relogin is not enabled.")

        self.__second_relogin_try = False

        if response.request.url and "passwordReset.html" in response.request.url:
            raise InvalidOperationError("Password must be changed to use this session.")

        try:
            response.raise_for_status()
        except HTTPError as error:
            self.logger.debug(error)
            if response.status_code == 403:
                self.logger.info(f"User {self.username} is unauthorized for method {method} {full_url}")
            elif response.status_code == 400:
                raise vManageBadRequestError(response.get_error_info(), response)
            else:
                raise error
        return response

    def get_full_url(self, url_path: str) -> str:
        """Returns base API url plus given url path."""
        return urljoin(self.base_url, url_path)

    def __create_base_url(self) -> str:
        """Creates base url based on ip address or domain and port if provided.

        Returns:
            str: Base url shared for every request.
        """
        if self.port:
            return f"https://{self.url}:{self.port}"
        return f"https://{self.url}"

    def about(self) -> AboutInfo:
        return self.primitives.client.about()

    def server(self) -> ServerInfo:
        server_info = self.primitives.client.server()
        self.platform_version = server_info.platform_version
        return server_info

    def get_data(self, url: str) -> Any:
        return self.get_json(url)["data"]

    def get_json(self, url: str) -> Any:
        response = self.get(url)
        return response.json()

    def get_file(self, url: str, filename: Path) -> Response:
        """Get a file using session get.

        Args:
            url: dataservice api.
            filename: Filename to write download file to.

        Returns:
            http response.

        Example usage:
            response = self.session.get_file(url, filename)

        """
        with self.get(url) as response:
            with open(filename, "wb") as file:
                file.write(response.content)
        return response

    def wait_for_server_reachability(self, retries: int, delay: int, initial_delay: int = 0) -> bool:
        """Checks if vManage API is reachable by sending server request.

        Retries on HTTPError for specified number of times.
        Delays between each request are configurable,
        It is intended to be used as a probe, so it doesn't raise original error from exception.

        Args:
            retries: total number of retires
            delay: time to wait between each retry
            initial_delay: time before sending first request

        Returns:
            Bool: True if device is reachable, False if not
        """

        def _log_exception(retry_state):
            self.logger.error(f"Cannot reach server, original exception: {retry_state.outcome.exception()}")
            return False

        if initial_delay:
            time.sleep(initial_delay)

        @retry(
            wait=wait_fixed(delay),
            retry=retry_if_exception_type(HTTPError),
            stop=stop_after_attempt(retries),
            retry_error_callback=_log_exception,
        )
        def _send_server_request():
            return self.server()

        return True if _send_server_request() else False

    def get_tenant_id(self) -> str:
        """Gets tenant UUID for its subdomain.

        Returns:
            Tenant UUID.
        """
        tenants = self.primitives.tenant_management.get_all_tenants()
        tenant = tenants.filter(sub_domain=self.subdomain).single_or_default()

        if not tenant:
            raise TenantSubdomainNotFound(f"Tenant with sub-domain: {self.subdomain} not found")

        return tenant.tenant_id

    def get_virtual_session_id(self, tenant_id: str) -> str:
        """Get VSessionId for a specific tenant

        Note: In a multitenant vManage system, this API is only available in the Provider view.

        Args:
            tenant_id: provider or tenant UUID
        Returns:
            Virtual session token
        """
        url_path = f"/dataservice/tenant/{tenant_id}/vsessionid"
        response = self.post(url_path)
        return response.json()["VSessionId"]

    def __prepare_session(self, verify: bool, auth: Optional[AuthBase]) -> None:
        self.auth = auth
        self.verify = verify

    def check_vmanage_server_connection(self) -> bool:
        try:
            head(self.base_url, timeout=15, verify=False)
        except ConnectionError:
            return False
        else:
            return True

    @property
    def session_type(self) -> SessionType:
        return self._session_type

    @property
    def platform_version(self) -> Version:
        return self._platform_version

    @platform_version.setter
    def platform_version(self, version: Version):
        self._platform_version = version
        self._api_version = Version(f"{version.major}.{version.minor}")

    @property
    def api_version(self) -> Version:
        return self._api_version

    def __str__(self) -> str:
        return f"{self.username}@{self.base_url}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}('{self.url}', '{self.username}', '{self.password}', port={self.port}, "
            f"subdomain='{self.subdomain}')"
        )

    def __eq__(self, other):
        if isinstance(other, vManageSession):
            comparison_list = [
                self.url == other.url,
                self.username == other.username,
                self.password == other.password,
                self.port == other.port,
                str(self.subdomain) == str(other.subdomain),
            ]
            return True if all(comparison_list) else False
        return False
