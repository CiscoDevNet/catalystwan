# Copyright 2022 Cisco Systems, Inc. and its affiliates

import unittest
from unittest import TestCase, mock
from uuid import uuid4

from requests import Request

from catalystwan import USER_AGENT
from catalystwan.vmanage_auth import UnauthorizedAccessError, vManageAuth


class MockResponse:
    def __init__(self, status_code: int, text: str):
        self._status_code = status_code
        self._text = text
        self.request = Request()

    def cookies(self) -> str:  # TODO
        return "JSESSIONID=xyz"

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def text(self) -> str:  # TODO
        return self._text


def mocked_requests_method(*args, **kwargs):
    url_response = {
        "https://1.1.1.1:1111/j_security_check": {
            "admin": MockResponse(200, ""),
            "invalid_username": MockResponse(200, "<html>error</html>"),
        }
    }

    full_url = kwargs.get("url", "")
    data = kwargs.get("data", {})
    if full_url in url_response:
        return url_response[full_url][data["j_username"]]

    return MockResponse(404, "error")


class TestvManageAuth(TestCase):
    def setUp(self):
        self.base_url = "https://1.1.1.1:1111"
        self.password = str(uuid4())

    @mock.patch("requests.post", side_effect=mocked_requests_method)
    def test_get_cookie(self, mock_post):
        # Arrange
        username = "admin"
        security_payload = {
            "j_username": username,
            "j_password": self.password,
        }
        auth = vManageAuth(self.base_url, username, self.password)
        # Act
        auth.get_cookie()

        # Assert
        mock_post.assert_called_with(
            url="https://1.1.1.1:1111/j_security_check",
            data=security_payload,
            verify=False,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT},
        )

    @mock.patch("requests.post", side_effect=mocked_requests_method)
    def test_get_cookie_invalid_username(self, mock_post):
        # Arrange
        username = "invalid_username"
        security_payload = {
            "j_username": username,
            "j_password": self.password,
        }
        auth = vManageAuth(self.base_url, username, self.password)
        # Act
        with self.assertRaises(UnauthorizedAccessError):
            auth.get_cookie()

        # Assert
        mock_post.assert_called_with(
            url="https://1.1.1.1:1111/j_security_check",
            data=security_payload,
            verify=False,
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": USER_AGENT},
        )

    @mock.patch("requests.cookies.RequestsCookieJar")
    @mock.patch("requests.get", side_effect=mocked_requests_method)
    def test_fetch_token(self, mock_get, cookies):
        # Arrange
        valid_url = "https://1.1.1.1:1111/dataservice/client/token"
        auth = vManageAuth(self.base_url, "admin", self.password)

        # Act
        auth.fetch_token(cookies)

        # Assert
        mock_get.assert_called_with(
            url=valid_url,
            verify=False,
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
            cookies=cookies,
        )


if __name__ == "__main__":
    unittest.main()
