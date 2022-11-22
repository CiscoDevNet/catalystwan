import unittest

from vmngclient.session import Session


class TestSessionConstructor(unittest.TestCase):
    def test_session_str(self):
        # Arrange, Act
        session = Session("1.1.1.1", "admin", None, port=111)
        # Assert
        self.assertEqual(str(session), "admin@https://1.1.1.1:111")
