from typing import Optional
from urllib.parse import urljoin

import requests
from requests import PreparedRequest
from requests.auth import AuthBase
from requests.cookies import RequestsCookieJar


class InvalidCredentialsError(Exception):
    """Exception raised for invalid credentials.

    Attributes:
        username (str): vManage username.
        password (str): vManage password.
        message (str): precise error explanation.
    """

    def __init__(
        self,
        username: str,
        password: str,
        message: str = "Username and/or password is incorrect. Please try again!",
    ):
        self.username = username
        self.password = password
        self.message = message

    def __str__(self):
        return (
            f"Trying to access vManage with the following credentials: {self.username}/{self.password}. {self.message}"
        )


class vManageAuth(AuthBase):
    """Attaches vManage Authentication to the given Requests object.

    vManage REST API access control is based on sessions.
    The call method do whatever is required to make the vManage authentication work.
    The following are typical steps for a user to consume the API:
    1. Log in with a user name and password to establish a session.
    2. Get a cross-site request forgery prevention token, which is required for most POST operations.

    Attributes:
        base_url (str): url (with port if applicable) f.e. https://1.1.1.1:1111
        username (str): vManage username
        password (str): vManage user's password
        verify (bool): Controls whether we verify the server's TLS certificate.
                Defaults to True.
        expiration_time (int): Expiration token time in seconds.
                Defaults to None (unlimited).
        token (str): Access token

    """

    def __init__(self, base_url: str, username: str, password: str, verify: bool = False):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify = verify  # TODO Handle `True` parameter
        self.expiration_time: Optional[int] = None  # Unlimited
        self.set_cookie: Optional[RequestsCookieJar] = None
        self.token: str = ""

    def get_cookie(self) -> RequestsCookieJar:
        """Check whether a user is successfully authenticated.

        If a user is successfully authenticated, the response body is empty and a valid session cookie is set.
        The response has entry in headers named `set-cookie` equal to JESSIONID={session hash}.
        If a user is un-authenticated, the response body contains a html login page with tag in it.

        Raises:
            InvalidCredentialsError: _description_

        Returns:
            RequestsCookieJar: _description_
        """
        security_payload = {
            "j_username": self.username,
            "j_password": self.password,
        }
        full_url = urljoin(self.base_url, "/j_security_check")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            url=full_url,
            data=security_payload,
            verify=self.verify,
            headers=headers,
        )
        if response.text != "":
            raise InvalidCredentialsError(self.username, self.password)
        return response.cookies

    def fetch_token(self, cookies: RequestsCookieJar) -> str:
        """If it is required, fetches vManage REST API token.

        The XSRF token is in the response body.
        XSRF token along with the JESSIONID cookie is used for ongoing API requests.

        Args:
            cookies (RequestsCookieJar): The JESSIONID={session hash} cookie is required to authenticate.

        Returns:
            str: Valid token.
        """
        full_url = urljoin(self.base_url, "/dataservice/client/token")
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=full_url,
            cookies=cookies,
            verify=self.verify,
            headers=headers,
        )
        return response.text

    def __call__(self, prepared_request: PreparedRequest) -> PreparedRequest:
        if self.expiration_time is None:
            if self.token == "":
                self.set_cookie = self.get_cookie()
                self.token = self.fetch_token(self.set_cookie)

        prepared_request.prepare_cookies(self.set_cookie)
        prepared_request.headers.update({"x-xsrf-token": self.token})
        return prepared_request
