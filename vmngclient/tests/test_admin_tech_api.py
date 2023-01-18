import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import ANY, patch

from vmngclient.api.admin_tech_api import (
    AdminTechAPI,
    DownloadAdminTechLogError,
    GenerateAdminTechLogError,
    RequestTokenIdNotFound,
)
from vmngclient.dataclasses import DeviceAdminTech


class TestAdminTechAPI(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.device_ip = "169.254.10.4"
        self.admin_tech_generate_response = {
            "size": 1479740,
            "fileName": "172.16.253.129-vm129-20221116-065219-admin-tech.tar.gz",
        }
        self.device_admin_tech_infos = {
            "data": [
                {
                    "fileName": "172.16.255.200-vm200-20221116-060922-admin-tech.tar.gz",
                    "creationTime": 1668578961380,
                    "size": 31934859,
                    "state": "done",
                    "requestTokenId": "null",
                }
            ]
        }
        self.admin_tech_infos = {
            "data": [
                {
                    "creationTime": 1668581537503,
                    "size": self.admin_tech_generate_response["size"],
                    "fileName": self.admin_tech_generate_response["fileName"],
                    "state": "done",
                    "tac_state": "notStarted",
                    "deviceIP": self.device_ip,
                    "local-system-ip": "172.16.253.129",
                    "requestTokenId": "aace1605-ba9a-40fa-990b-c694a011a866",
                },
                {
                    "creationTime": 1668578961380,
                    "size": 31934859,
                    "fileName": "172.16.255.200-vm200-20221116-060922-admin-tech.tar.gz",
                    "state": "done",
                    "tac_state": "notStarted",
                    "deviceIP": "169.254.10.1",
                    "local-system-ip": "172.16.255.200",
                    "requestTokenId": "8b7f9a3a-e137-4af4-b2f9-b04808e1e2eb",
                },
            ]
        }
        self.admin_tech_info = self.admin_tech_infos["data"][0]
        self.download_file_content = "Downloaded file content"
        self.download_file = io.BytesIO(self.download_file_content.encode())

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.json.return_value = self.device_admin_tech_infos
        # Act
        admintechs = AdminTechAPI(mock_session).get(self.device_ip)
        # Assert
        mock_session.post.assert_called_once_with(
            url="/dataservice/device/tools/admintechlist",
            json={"deviceIP": self.device_ip},
        )
        self.assertIsInstance(admintechs[0], DeviceAdminTech)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_get_all(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_response.json.return_value = self.admin_tech_infos
        # Act
        admintechs = AdminTechAPI(mock_session).get_all()
        # Assert
        mock_session.get.assert_called_once_with("/dataservice/device/tools/admintechs")
        self.assertEqual(len(admintechs), len(self.admin_tech_infos["data"]))

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_generate(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 200
        mock_response.json.return_value = self.admin_tech_generate_response
        # Act
        filename = AdminTechAPI(mock_session).generate(
            device_id=self.device_ip, polling_timeout=0.01, polling_interval=0.01
        )
        print(filename)
        # Assert
        mock_session.post.assert_called_once_with(url="/dataservice/device/tools/admintech", json=ANY, timeout=ANY)
        self.assertEqual(filename, self.admin_tech_generate_response["fileName"])

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_generate_in_progress_error_retry(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": {"details": "Admin tech creation already in progress"}}
        interval = 0.01
        count = 2
        # Act/Assert
        with self.assertRaises(GenerateAdminTechLogError):
            AdminTechAPI(mock_session).generate(
                device_id=self.device_ip,
                polling_timeout=interval * count,
                polling_interval=interval,
            )
        self.assertEqual(mock_session.post.call_count, count)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_generate_error(self, mock_session, mock_response):
        # Arrange
        mock_session.post.return_value = mock_response
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": {"details": "Server Error"}}
        interval = 0.01
        count = 3
        # Act/Assert
        with self.assertRaises(GenerateAdminTechLogError):
            AdminTechAPI(mock_session).generate(
                device_id=self.device_ip,
                polling_timeout=interval * count,
                polling_interval=interval,
            )
        mock_session.post.assert_called_once()

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_delete(self, mock_session, mock_response):
        # Arrange
        filename = self.admin_tech_generate_response["fileName"]
        token_id = self.admin_tech_info["requestTokenId"]
        mock_session.get.return_value = mock_response
        mock_response.json.return_value = self.admin_tech_infos
        # Act
        AdminTechAPI(mock_session).delete(filename)
        # Assert
        mock_session.delete.assert_called_once_with(f"/dataservice/device/tools/admintech/{token_id}")

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_delete_token_not_found(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_response.json.return_value = self.admin_tech_infos
        # Act/Assert
        with self.assertRaises(RequestTokenIdNotFound):
            AdminTechAPI(mock_session).delete("fake-filename.tar.gz")

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_download(self, mock_session, mock_response):
        # Arrange
        filename = self.admin_tech_generate_response["fileName"]
        mock_session.get_file.return_value = mock_response
        mock_session.get.return_value = mock_response
        mock_response.status_code = 200
        mock_response.content = self.download_file_content
        with tempfile.TemporaryDirectory() as tmpdir:
            # Act
            download_path = AdminTechAPI(mock_session).download(filename, Path(tmpdir))
            # Assert
            self.assertEqual(download_path, Path(tmpdir) / filename)

    @patch("vmngclient.session.vManageSession")
    @patch("requests.Response")
    def test_download_error(self, mock_session, mock_response):
        # Arrange
        mock_session.get.return_value = mock_response
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": {"details": "Server Error"}}
        with tempfile.TemporaryDirectory() as tmpdir:
            # Act/Assert
            with self.assertRaises(DownloadAdminTechLogError):
                AdminTechAPI(mock_session).download("fake-filename.tar.gz", Path(tmpdir))
