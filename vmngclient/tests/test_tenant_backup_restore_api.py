import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from vmngclient.api.tenant_backup_restore_api import TenantBackupRestoreAPI


class TestTenantBackupRestoreAPI(unittest.TestCase):
    def setUp(self):
        self.processId = "5a6250c5ef1b1202"
        self.download_file_content = "Downloaded file content"
        self.full_name = Path("/dataservice")
        self.full_name = (
            self.full_name
            / "tenantbackup"
            / "download"
            / "3cf632d2-5a62-45cb-af50-50c5ef1b1202"
            / "bkup_3cf632d2-5a62-45cb-af50-50c5ef1b1202_010823-180713_88aba4772eef495ab6857a5076625ba9.tar.gz"
        )
        self.downloaded_file = Path("/tmp") / self.full_name.name

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_delete_full_name(self, mock_session, mock_response):
        # Arrange
        mock_session.delete.return_value = mock_response
        mock_response.json.return_value = mock_response
        expected_api = f"/dataservice/tenantbackup/delete?fileName={self.full_name}"
        # Act
        TenantBackupRestoreAPI(mock_session).delete(str(self.full_name))
        # Assert
        mock_session.delete.assert_called_once_with(expected_api)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_delete_name(self, mock_session, mock_response):
        # Arrange
        mock_session.delete.return_value = mock_response
        mock_response.json.return_value = mock_response
        expected_api = f"/dataservice/tenantbackup/delete?fileName={self.full_name.name}"
        # Act
        TenantBackupRestoreAPI(mock_session).delete(str(self.full_name.name))
        # Assert
        mock_session.delete.assert_called_once_with(expected_api)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_delete_all(self, mock_session, mock_response):
        # Arrange
        mock_session.delete.return_value = mock_response
        mock_response.json.return_value = mock_response
        expected_api = "/dataservice/tenantbackup/delete?fileName=all"
        # Act
        TenantBackupRestoreAPI(mock_session).delete_all()
        # Assert
        mock_session.delete.assert_called_once_with(expected_api)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_download_full(self, mock_session, mock_response):
        # Arrange
        mock_session.get_file.return_value = mock_response
        mock_session.get.return_value = mock_response
        mock_response.status_code = 200
        mock_response.content = self.download_file_content
        with tempfile.TemporaryDirectory() as tmpdir:
            # Act
            download_path = TenantBackupRestoreAPI(mock_session).download(str(self.full_name), Path(tmpdir))
            # Assert
            self.assertEqual(download_path, Path(tmpdir) / self.full_name.name)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_download_name(self, mock_session, mock_response):
        # Arrange
        mock_session.get_file.return_value = mock_response
        mock_session.get.return_value = mock_response
        mock_response.status_code = 200
        mock_response.content = self.download_file_content
        with tempfile.TemporaryDirectory() as tmpdir:
            # Act
            download_path = TenantBackupRestoreAPI(mock_session).download(self.full_name.name, Path(tmpdir))
            # Assert
            self.assertEqual(download_path, Path(tmpdir) / self.full_name.name)
