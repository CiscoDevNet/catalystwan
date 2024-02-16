from __future__ import annotations

import logging
import time
from enum import Enum
from importlib import metadata
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, List, Optional, Union
from urllib.parse import urljoin, urlparse, urlunparse

from packaging.version import Version  # type: ignore
from requests import PreparedRequest, Request, Response, Session, head
from requests.auth import AuthBase
from requests.exceptions import ConnectionError, HTTPError, RequestException
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed  # type: ignore

from catalystwan.api.api_container import APIContainer
from catalystwan.endpoints import APIEndpointClient
from catalystwan.endpoints.client import AboutInfo, ServerInfo
from catalystwan.endpoints.endpoints_container import APIEndpointContainter
from catalystwan.exceptions import (
    DefaultPasswordError,
    ManagerHTTPError,
    ManagerRequestException,
    SessionNotCreatedError,
    TenantSubdomainNotFound,
)
from catalystwan.models.tenant import Tenant
from catalystwan.response import ManagerResponse, response_history_debug
from catalystwan.utils.session_type import SessionType
from catalystwan.version import NullVersion, parse_api_version
from catalystwan.vmanage_auth import vManageAuth

JSON = Union[Dict[str, "JSON"], List["JSON"], str, int, float, bool, None]
USER_AGENT = f"{__package__}/{metadata.version(__package__)}"


class UserMode(str, Enum):
    PROVIDER = "provider"
    TENANT = "tenant"


class ViewMode(str, Enum):
    PROVIDER = "provider"
    TENANT = "tenant"


class TenancyMode(str, Enum):
    SINGLE_TENANT = "SingleTenant"
    MULTI_TENANT = "MultiTenant"


def determine_session_type(
    tenancy_mode: Optional[str], user_mode: Optional[str], view_mode: Optional[str]
) -> SessionType:
    modes_map = {
        (TenancyMode.SINGLE_TENANT, UserMode.TENANT, ViewMode.TENANT): SessionType.SINGLE_TENANT,
        (TenancyMode.MULTI_TENANT, UserMode.PROVIDER, ViewMode.PROVIDER): SessionType.PROVIDER,
        (TenancyMode.MULTI_TENANT, UserMode.PROVIDER, ViewMode.TENANT): SessionType.PROVIDER_AS_TENANT,
        (TenancyMode.MULTI_TENANT, UserMode.TENANT, ViewMode.TENANT): SessionType.TENANT,
    }
    try:
        return modes_map.get(
            (TenancyMode(tenancy_mode), UserMode(user_mode), ViewMode(view_mode)), SessionType.NOT_DEFINED
        )
    except ValueError:
        return SessionType.NOT_DEFINED


def create_manager_session(
    url: str,
    username: str,
    password: str,
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> ManagerSession:
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
        ManagerSession: Configured Session to perform tasks on vManage.
    """
    session = ManagerSession(url=url, username=username, password=password, port=port, subdomain=subdomain)
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
    except DefaultPasswordError:
        server_info = ServerInfo.parse_obj({})

    session.server_name = server_info.server
    session.on_session_create_hook()

    tenancy_mode = server_info.tenancy_mode
    user_mode = server_info.user_mode
    view_mode = server_info.view_mode

    session._session_type = determine_session_type(tenancy_mode, user_mode, view_mode)
    if user_mode is UserMode.TENANT and subdomain:
        raise SessionNotCreatedError(
            f"Session not created. Subdomain {subdomain} passed to tenant session, "
            "cannot switch to tenant from tenant user mode."
        )
    elif session._session_type is SessionType.NOT_DEFINED:
        session.logger.warning(
            "Cannot determine session type for "
            f"tenancy-mode: {tenancy_mode}, user-mode: {user_mode}, view-mode: {view_mode}"
        )

    session.logger.info(
        f"Logged to vManage({session.platform_version}) as {username}. The session type is {session.session_type}"
    )

    return session


class vManageResponseAdapter(Session):
    def request(self, method, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().request(method, url, *args, **kwargs))

    def get(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().get(url, *args, **kwargs))

    def post(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().post(url, *args, **kwargs))

    def put(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().put(url, *args, **kwargs))

    def delete(self, url, *args, **kwargs) -> ManagerResponse:
        return ManagerResponse(super().delete(url, *args, **kwargs))


class ManagerSession(vManageResponseAdapter, APIEndpointClient):
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

    on_session_create_hook: ClassVar[Callable[[ManagerSession], Any]] = lambda *args: None

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
        self.response_trace: Callable[
            [Optional[Response], Union[Request, PreparedRequest, None]], str
        ] = response_history_debug
        super(ManagerSession, self).__init__()
        self.headers.update({"User-Agent": USER_AGENT})
        self.__prepare_session(verify, auth)
        self.api = APIContainer(self)
        self.endpoints = APIEndpointContainter(self)
        self._platform_version: str = ""
        self._api_version: Version

    def request(self, method, url, *args, **kwargs) -> ManagerResponse:
        full_url = self.get_full_url(url)
        try:
            response = super(ManagerSession, self).request(method, full_url, *args, **kwargs)
            self.logger.debug(self.response_trace(response, None))
        except RequestException as exception:
            self.logger.debug(self.response_trace(exception.response, exception.request))
            self.logger.error(exception)
            raise ManagerRequestException(request=exception.request, response=exception.response)

        if self.enable_relogin and self.__is_jsession_updated(response):
            self.logger.warning("Logging to session again. Reason: JSESSIONID cookie updated by response")
            self.auth = vManageAuth(self.base_url, self.username, self.password, verify=False)
            return self.request(method, url, *args, **kwargs)

        if response.request.url and "passwordReset.html" in response.request.url:
            raise DefaultPasswordError("Password must be changed to use this session.")

        try:
            response.raise_for_status()
        except HTTPError as error:
            self.logger.error(error)
            error_info = response.get_error_info()
            raise ManagerHTTPError(error_info=error_info, request=error.request, response=error.response)
        return response

    def get_full_url(self, url_path: str) -> str:
        """Returns base API url plus given url path."""
        return urljoin(self.base_url, url_path)

    def __create_base_url(self) -> str:
        """Creates base url based on ip address or domain and port if provided.

        Returns:
            str: Base url shared for every request.
        """
        url = urlparse(self.url)
        netloc: str = url.netloc or url.path
        scheme: str = url.scheme or "https"
        base_url = urlunparse((scheme, netloc, "", None, None, None))
        if self.port:
            return f"{base_url}:{self.port}"
        return base_url

    def about(self) -> AboutInfo:
        return self.endpoints.client.about()

    def server(self) -> ServerInfo:
        server_info = self.endpoints.client.server()
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
        tenants = self.get("dataservice/tenant").dataseq(Tenant)
        tenant = tenants.filter(subdomain=self.subdomain).single_or_default()

        if not tenant or not tenant.tenant_id:
            raise TenantSubdomainNotFound(f"Tenant ID for sub-domain: {self.subdomain} not found")

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

    def logout(self) -> Optional[ManagerResponse]:
        if isinstance((version := self.api_version), NullVersion):
            self.logger.warning("Cannot perform logout operation without known api_version.")
            return None
        else:
            return self.post("/logout") if version >= Version("20.12") else self.get("/logout")

    def close(self) -> None:
        """Closes the ManagerSession.

        This method is overrided from requests.Session.
        Firstly it cleans up any resources associated with vManage.
        Then it closes all adapters and as such the session.

        Note: It is generally recommended to use the session as a context manager
        using the `with` statement, which ensures that the session is properly
        closed and resources are cleaned up even in case of exceptions.
        """
        self.enable_relogin = False
        self.logout()
        super().close()

    def __prepare_session(self, verify: bool, auth: Optional[AuthBase]) -> None:
        self.auth = auth
        self.verify = verify

    def __is_jsession_updated(self, response: ManagerResponse) -> bool:
        if (jsessionid := response.cookies.get("JSESSIONID")) and isinstance(self.auth, vManageAuth):
            if jsessionid != self.auth.set_cookie.get("JSESSIONID"):
                return True
        return False

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
    def platform_version(self) -> str:
        return self._platform_version

    @platform_version.setter
    def platform_version(self, version: str):
        self._platform_version = version
        self._api_version = parse_api_version(version)

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
        if isinstance(other, ManagerSession):
            comparison_list = [
                self.url == other.url,
                self.username == other.username,
                self.password == other.password,
                self.port == other.port,
                str(self.subdomain) == str(other.subdomain),
            ]
            return True if all(comparison_list) else False
        return False
