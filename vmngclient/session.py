from __future__ import annotations

import logging
import time
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union
from urllib.error import HTTPError
from urllib.parse import urljoin

# import requests
from requests import Response, Session
from requests.auth import AuthBase
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.vmanage_auth import vManageAuth

logger = logging.getLogger(get_logger_name(__name__))


class SessionType(Enum):
    PROVIDER = auto()
    TENANT = auto()
    PROVIDER_AS_TENANT = auto()
    NOT_DEFINED = auto()


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


class SessionNotCreatedError(Exception):
    pass


def create_vManageSession(
    url: str,
    username: str,
    password: str,
    port: Optional[int] = None,
    subdomain: Optional[str] = None,
) -> vManageSession:
    """Factory function that creates session object based on provided arguments.

    Args:
        url (str): IP address or domain name
        port (int): port
        username (str): username
        password (str): password
        subdomain: subdomain specifying to which view switch when creating provider as a tenant session,
            works only on provider user mode
        timeout (int): timeout

    Returns:
        Session object
    """
    a = vManageAuth("https://sandbox-sdwan-2.cisco.com/", username, password, verify=False)
    session = vManageSession(url=url, username=username, password=password, port=port, subdomain=subdomain, auth=a)
    auth = vManageAuth(session.base_url, username, password, verify=False)
    session.auth = auth
    server_info = session.server()
    print(server_info)

    try:
        user_mode = UserMode(server_info.get("userMode", "not found"))
    except ValueError:
        user_mode = UserMode.NOT_RECOGNIZED
        logger.warning(f"Unrecognized user mode is: '{server_info.get('userMode')}'")

    try:
        view_mode = ViewMode(server_info.get("viewMode", "not found"))
    except ValueError:
        view_mode = ViewMode.NOT_RECOGNIZED
        logger.warning(f"Unrecognized user mode is: '{server_info.get('viewMode')}'")

    if user_mode is UserMode.TENANT and not subdomain and view_mode is ViewMode.TENANT:
        session.session_type = SessionType.TENANT
    elif user_mode is UserMode.PROVIDER and not subdomain and view_mode is ViewMode.PROVIDER:
        session.session_type = SessionType.PROVIDER
    elif user_mode is UserMode.PROVIDER and view_mode is ViewMode.TENANT:
        # session.__switch_to_tenant()
        session.session_type = SessionType.PROVIDER_AS_TENANT
    elif user_mode is UserMode.TENANT and subdomain:
        raise SessionNotCreatedError(
            f"Session not created. Subdomain {subdomain} passed to tenant session, "
            "cannot switch to tenant from tenant user mode."
        )
    else:
        session.session_type = SessionType.NOT_DEFINED
        logger.warning(
            f"Session created with {user_mode.value} user mode and {view_mode.value} view mode.\n"
            f"Session type set to not defined"
        )

    return session


class vManageSession(Session):
    """Base class for API sessions for vManage client.

    Defines methods and handles session connectivity available for provider, provider as tenant, and tenant.

    Args:
        url: IP address or domain name, i.e. '10.0.1.200' or 'fruits.com'
        port: port
        username: username
        password: password
        timeout: timeout
    """

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
        self.base_url = self.__create_base_url(url, port)
        self.username = username
        self.password = password
        self.port = port
        self.subdomain = subdomain

        self.session_type = SessionType.NOT_DEFINED  # TODO readonly

        super(vManageSession, self).__init__()
        self.__prepare_session(verify, auth)

    def request(self, method, url, *args, **kwargs) -> Response:
        full_url = self.get_full_url(url)
        return super(vManageSession, self).request(method, full_url, args, kwargs)

    def get_full_url(self, url_path: str) -> str:
        """Returns base API url plus given url path."""
        return urljoin(self.base_url, url_path)

    def __create_base_url(self, url: str, port: Optional[int]) -> str:
        """Creates base url based on ip address and port.

        Args:
            url: IP address or domain name, i.e. '10.0.1.200' or 'fruits.com'
            port (int): Port of reachable vManage.

        Returns:
            str: Base url shared for every request.
        """
        if port:
            return f"https://{url}:{port}"
        return f"https://{url}"

    def about(self) -> Union[List[Any], Dict[Any, Any]]:
        response = self.get(url="/dataservice/client/about")
        data = self.get_data(response)
        return data

    def server(self) -> Dict[Any, Any]:
        response = self.get(url="/dataservice/client/server")
        data = self.get_data(response)
        return data

    def get_data(self, response: Response):
        return response.json()['data']

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
            logger.error(f"Cannot reach server, orignial exception: {retry_state.outcome.exception()}")
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

    # def __get_tenant_id(self) -> str:
    #     """Gets tenant UUID for tenant subdomain.
    #     Returns:
    #         tenant UUID
    #     """
    #     tenants = self.get_data('/dataservice/tenant')
    #     tenant_ids = [tenant.get('tenantId') for tenant in tenants if tenant['subDomain'] == self.subdomain]
    #     return tenant_ids[0]

    # def __create_vsession(self, tenant_id: str) -> str:
    #     """Creates virtual session for tenant.
    #     Args:
    #         tenant_id: provider or tenant UUID
    #     Returns:
    #         virtual session token
    #     """
    #     response = cast(dict, self.post_json(f'/dataservice/tenant/{tenant_id}/vsessionid'))
    #     return response['VSessionId']

    # def __switch_to_tenant(self) -> None:
    #     """As provider impersonate tenant session."""
    #     tenant_id = self.__get_tenant_id()
    #     vsession_id = self.__create_vsession(tenant_id)
    #     self.session_headers['VSessionId'] = vsession_id

    def __prepare_session(self, verify: bool, auth: Optional[AuthBase]) -> None:
        self.auth = auth
        self.verify = verify

    def __str__(self) -> str:
        return f"{self.username}@{self.base_url}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.username}@{self.base_url})"
