import unittest
from typing import Optional

from parameterized import parameterized  # type: ignore

from vmngclient.session import vManageSession


class TestSession(unittest.TestCase):
    def setUp(self):
        self.url = "example.com"
        self.username = "admin"
        self.password = "admin_password"

    def test_session_str(self):
        # Arrange, Act
        session = vManageSession(self.url, self.username, self.password, port=111)

        # Assert
        self.assertEqual(str(session), "admin@https://example.com:111")

    @parameterized.expand(
        [
            (123, "https://example.com:123"),
            (None, "https://example.com"),
        ]
    )
    def test_base_url(self, port: Optional[int], base_url: str):
        # Arrange, Act
        session = vManageSession(self.url, self.username, self.password, port=port)

        # Assert
        self.assertEqual(session.base_url, base_url)

    @parameterized.expand(
        [
            (123, "/devices", "https://example.com:123/devices"),
            (123, "devices", "https://example.com:123/devices"),
            (None, "/devices", "https://example.com/devices"),
            (None, "devices", "https://example.com/devices"),
        ]
    )
    def test_get_full_url(self, port: Optional[int], url: str, full_url: str):
        # Arrange, Act
        session = vManageSession(self.url, self.username, self.password, port=port)

        # Assert
        self.assertEqual(session.get_full_url(url), full_url)


if __name__ == '__main__':
    unittest.main()
