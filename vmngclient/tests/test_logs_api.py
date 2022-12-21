import unittest
from pathlib import Path
from unittest.mock import patch

from vmngclient.api.logs_api import LogsAPI


class TestLogsAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.logs = [
            {"logid": "12345", "logmessage": "message from log 1", "tenant": "tenant234", "entry_time": 1671028426000},
            {"logid": "67890", "logmessage": "message from log 2", "tenant": "tenant987", "entry_time": 1671028426000},
        ]

    @patch("vmngclient.session.vManageSession")
    def test_get_auditlogs_file_path_not_provided(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.logs
        default_file_path = Path(__file__).parents[1].joinpath("api").joinpath("audit.log")
        # Act
        LogsAPI(mock_session).get_auditlogs()
        does_file_exist = default_file_path.is_file()
        # Assert
        self.assertTrue(does_file_exist)

    @patch("vmngclient.session.vManageSession")
    def test_get_auditlogs_file_path_provided(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.logs
        file_path = Path(__file__).parents[0].joinpath("test_file.log")
        # Act
        LogsAPI(mock_session).get_auditlogs(file_path=str(file_path))
        does_file_exist = file_path.is_file()
        # Assert
        self.assertTrue(does_file_exist)
