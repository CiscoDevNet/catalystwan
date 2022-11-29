import unittest
from unittest.mock import patch

from vmngclient.session import Session


class TestSessionConstructor(unittest.TestCase):
    def test_session_str(self):
        # Arrange, Act
        session = Session("1.1.1.1", "admin", None, port=111)
        # Assert
        self.assertEqual(str(session), "admin@https://1.1.1.1:111")

    def test_session_repr(self):
        # Arrange, Act
        session = Session("domain.com", "user1", "$password", port=111)
        session_str = "Session('domain.com', 'user1', '$password', port=111, subdomain='None', timeout=30)"
        # Assert
        self.assertEqual(repr(session), session_str)

    def test_session_repr_different_sessions(self):
        # Arrange, Act
        session = Session("domain.com", "user1", "$password", port=111)
        session_str = "Session('not.domain.com', 'different_user', '$password', port=111, subdomain='None', timeout=30)"
        # Assert
        self.assertNotEqual(repr(session), session_str)

    @patch("vmngclient.session.Session.__repr__")
    def test_session_eval_repr(self, mock_repr):
        # Arrange, Act
        mock_repr.return_value = "Session('domain.com', 'user1', '$password', port=111, subdomain='None', timeout=30)"
        session = Session("domain.com", "user1", "$password", port=111)
        # Assert
        self.assertEqual(eval(mock_repr()), session)

    @patch("vmngclient.session.Session.__repr__")
    def test_session_eval_repr_different_sessions(self, mock_repr):
        # Arrange, Act
        mock_repr.return_value = "Session('domain.com', 'user1', '$password', port=111, subdomain='None', timeout=30)"
        session = Session("not.domain.com", "different_user", "$password", port=111)
        # Assert
        self.assertNotEqual(eval(mock_repr()), session)

    def test_session_eq(self):
        # Arrange, Act
        session_1 = Session("domain.com", "user1", "$password", port=111)
        session_2 = Session("domain.com", "user1", "$password", port=111)
        # Assert
        self.assertEqual(session_1, session_2)

    def test_session_eq_different_sessions(self):
        # Arrange, Act
        session_1 = Session("domain.com", "user1", "$password", port=111)
        session_2 = Session("not.domain.com", "different_user", "$password", port=111)
        # Assert
        self.assertNotEqual(session_1, session_2)
