from __future__ import annotations

import logging
import socket
import ssl
import time
from enum import Enum, auto
from http import HTTPStatus
from http.client import HTTPException, HTTPResponse
from json import dumps, loads
from typing import Any, Dict, List, Optional, Union, cast
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from vmngclient.utils.creation_tools import get_logger_name

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


def create_session(
    url: str,
    username: str,
    password: str,
    port: int = None,
    subdomain: str = None,
    timeout: int = 30,
) -> Session:
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
    session = Session(url, username, password, port, subdomain, timeout)
    response = cast(dict, session.server())

    try:
        user_mode = UserMode(response.get("userMode", "not found"))
    except ValueError:
        user_mode = UserMode.NOT_RECOGNIZED
        logger.warning(f"Unrecognized user mode is: '{response.get('userMode')}'")

    try:
        view_mode = ViewMode(response.get("viewMode", "not found"))
    except ValueError:
        view_mode = ViewMode.NOT_RECOGNIZED
        logger.warning(f"Unrecognized user mode is: '{response.get('viewMode')}'")

    if user_mode is UserMode.TENANT and not subdomain and view_mode is ViewMode.TENANT:
        session.session_type = SessionType.TENANT
    elif user_mode is UserMode.PROVIDER and not subdomain and view_mode is ViewMode.PROVIDER:
        session.session_type = SessionType.PROVIDER
    elif user_mode is UserMode.PROVIDER and view_mode is ViewMode.TENANT:
        session.session_type = SessionType.PROVIDER_AS_TENANT
    elif user_mode is UserMode.TENANT and subdomain:
        raise SessionNotCreatedError(f"Session not created. Subdomain {subdomain} passed to tenant session, "
                                     "cannot switch to tenant from tenant user mode.")
    else:
        session.session_type = SessionType.NOT_DEFINED
        logger.warning(f"Session created with {user_mode.value} user mode and {view_mode.value} view mode.\n"
                       f"Session type set to not defined")

    return session


class Session:
    """Base class for API sessions for vmanage client.

    Defines methods and handles session connectivity available for provider, provider as tenant, and tenant.

    Args:
        url: IP address or domain name, i.e. '10.0.1.200' or 'fruits.com'
        port: port
        username: username
        password: password
        timeout: timeout
    """

    def __init__(
        self, url: str,
        username: str,
        password: str,
        port: Optional[int],
        subdomain: str = None,
        timeout: int = 30
    ):
        self.base_url = self.__create_base_url(url, port)
        self.username = username
        self.password = password
        self.subdomain = subdomain
        self.timeout = timeout

        self.session_type = SessionType.NOT_DEFINED

        self.ctx = self.__get_context()

        # TODO session headers as a function and serializable class
        self.session_headers: Dict[str, str] = dict()

    def get_full_url(self, url: str) -> str:
        """Returns base API URL plus relative URL.

        Args:
            url: relative API URL, i.e. '/dataservice/devices'

        Returns:
            str: Absolute API URL, i.e. 'https://10.0.1.200:8443/dataservice/devices'
        """
        return f'{self.base_url}{url}'

    def relogin_request(self, method: str, url: str, data: Union[dict, list, None] = None) -> HTTPResponse:
        """Generic method to send request to vManage API.

        Args:
            method: API method, i.e. POST, GET
            url: API endpoint without base URL
            data: (optional) Dictionary, list of tuples, bytes, or file-like
              object to send in the body of the request

        Returns:
            Response object
        """
        full_url = self.get_full_url(url)
        logger.debug(f'{method} {full_url}')
        response = self.session_request(method, full_url, data)
        if response.status == HTTPStatus.OK and 'set-cookie' in response.headers:
            self.session_headers = {
                name: value
                for name, value in self.session_headers.items()
                if name not in ['cookie', 'x-xsrf-token', 'VSessionId', 'content-type']
            }
            # in this case re-login is necessary because session is expired
            self.login()
            response = self.session_request(method, full_url, data)

        return response

    def get(self, url: str) -> HTTPResponse:
        """Send HTTP GET request using session headers.

        Used by methods: get_json.

        Args:
            url: API endpoint without base URL

        Returns:
            Response object
        """
        return self.relogin_request('GET', url)

    def decode_json(self, response: HTTPResponse) -> Union[dict, list]:
        """Try parsing API response as JSON and produce readable error message on failure.

        Args:
            response: response object

        Returns:
            Parsed data from JSON
        """
        response_text = response.read().decode('utf-8')
        try:
            json = loads(response_text)
            return json
        except ValueError as err:
            logger.error(f'Response status: {response.status}')
            logger.error(f'Invalid JSON response: {response_text}')
            raise err

    def get_json(self, url: str) -> Union[dict, list]:
        """Sends HTTP GET request and return parsed JSON data.

        Used by methods: get_data.

        Args:
            url: API endpoint without base URL

        Returns:
            JSON data parsed from response
        """
        return self.decode_json(self.get(url))

    def get_data(self, url: str) -> Union[list, dict]:
        """Sends HTTP GET request and return 'data' property from parsed JSON data.

        Args:
            url: API endpoint without base URL

        Returns:
            'data' property from the JSON response
        """
        json = cast(dict, self.get_json(url))
        assert 'data' in json, "Expecting data property in JSON response"

        return json['data']

    def post(self, url: str, data: Union[dict, list, None] = None) -> HTTPResponse:
        """Sends HTTP POST request using session headers.

        Used by methods: post_json, login.

        Args:
            url: API endpoint without base URL
            data: (optional) Dictionary, list of tuples, bytes, or file-like
              object to send in the body of the request

        Returns:
            response object
        """
        return self.relogin_request('POST', url, data)

    def post_json(self, url: str, data: Union[dict, list, None] = None) -> Union[dict, list]:
        """Sends HTTP POST request and return parsed JSON data.

        Args:
            url: API endpoint without base URL
            data: request payload

        Returns:
            JSON data parsed from response
        """
        return self.decode_json(self.post(url, data))

    def post_data(self, url: str, data: Optional[dict] = None) -> Union[list, dict]:
        """Sends HTTP POST request and return 'data' property from parsed JSON data.

        Args:
            url: API endpoint without base URL

        Returns:
            'data' property from the JSON response
        """
        json = cast(dict, self.post_json(url, data))
        assert 'data' in json, "Expecting data property in JSON response"

        return json['data']

    def put(self, url: str, data: Optional[dict] = None) -> HTTPResponse:
        """Sends HTTP PUT request using session headers.

        Used by methods: put_json.

        Args:
            url: API endpoint without base URL
            data: (optional) Dictionary, list of tuples, bytes, or file-like
              object to send in the body of the request

        Returns:
            response object
        """
        return self.relogin_request('PUT', url, data)

    def put_json(self, url: str, data: Optional[dict] = None) -> Union[list, dict]:
        """Sends HTTP PUT request and return parsed JSON data.

        Args:
            url: API endpoint without base URL
            data: request payload

        Returns:
            JSON data parsed from response
        """
        return self.decode_json(self.put(url, data))

    def put_data(self, url: str, data: Optional[dict] = None) -> Union[list, dict]:
        """Sends HTTP PUT request and return 'data' property from parsed JSON data.

        Args:
            url: API endpoint without base URL

        Returns:
            'data' property from the JSON response
        """
        json = cast(dict, self.put_json(url, data))
        assert 'data' in json, "Expecting data property in JSON response"

        return json['data']

    def delete(self, url: str) -> HTTPResponse:
        """Sends HTTP DELETE request for delete resource for example admin_tech file.

        Args:
            url: API endpoint without base URL

        Returns:
            response object
        """
        return self.relogin_request('DELETE', url)

    def login(self) -> None:
        """Login to vManage API using self username and password.

        Returns:
            Dictionary with Session headers.  # TODO
        """
        # send no session headers to login
        response = urlopen(
            Request(
                self.get_full_url('/j_security_check'),
                data=urlencode(
                    {
                        'j_username': self.username,
                        'j_password': self.password,
                    }
                ).encode('utf-8'),
                headers=self.session_headers,
            ),
            context=self.ctx,
            timeout=self.timeout,
        )

        assert 'set-cookie' in response.headers, 'Authentication error: cookie not found'

        self.session_headers['content-type'] = 'application/json'
        self.session_headers['cookie'] = response.headers['set-cookie']

        # use session_request instead of relogin_request to avoid infinite loop
        self.session_headers['x-xsrf-token'] = (
            self.session_request('GET', self.get_full_url('/dataservice/client/token')).read().decode('ascii')
        )

        if self.subdomain:
            self.__switch_to_tenant()

    def session_request(self, method: str, full_url: str, data: Union[dict, list, None] = None) -> HTTPResponse:
        available_methods = ["GET", "POST", "PUT", "PATCH", "HEAD", "DELETE"]
        assert method in available_methods, f"{method} is not supported. Available methods: {available_methods}."
        encoded = dumps(data).encode() if data else None
        try:
            return urlopen(
                Request(full_url, method=method, data=encoded, headers=self.session_headers),
                context=self.ctx,
                timeout=self.timeout,
            )
        except HTTPError as error:
            if error.code == 503:  # Catch Service Unavailable
                logger.warning("Server not ready to handle the request.")
                raise error
            logger.error(f"There was a problem with {method} method. URL: {full_url}. Error: {error}")
            raise error
        except socket.timeout as error:
            logger.error("Request timeout!")
            raise error
        except HTTPException as error:
            logger.error(error)
            raise error

    def __get_context(self) -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

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
        response = self.get_data(url="/dataservice/client/about")
        return response

    def server(self) -> Union[List[Any], Dict[Any, Any]]:
        response = self.get_data(url="/dataservice/client/server")
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

    def __get_tenant_id(self) -> str:
        """Gets tenant UUID for tenant subdomain.
        Returns:
            tenant UUID
        """
        tenants = self.get_data('/dataservice/tenant')
        tenant_ids = [tenant.get('tenantId') for tenant in tenants if tenant['subDomain'] == self.subdomain]
        return tenant_ids[0]

    def __create_vsession(self, tenant_id: str) -> str:
        """Creates virtual session for tenant.
        Args:
            tenant_id: provider or tenant UUID
        Returns:
            virtual session token
        """
        response = cast(dict, self.post_json(f'/dataservice/tenant/{tenant_id}/vsessionid'))
        return response['VSessionId']

    def __switch_to_tenant(self) -> None:
        """As provider impersonate tenant session."""
        tenant_id = self.__get_tenant_id()
        vsession_id = self.__create_vsession(tenant_id)
        self.session_headers['VSessionId'] = vsession_id

    def __str__(self) -> str:
        return f"{self.username}@{self.base_url}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.username}@{self.base_url})"
