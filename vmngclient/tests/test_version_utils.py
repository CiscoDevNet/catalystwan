import unittest
from unittest.mock import Mock, patch

from vmngclient.api.versions_utils import DeviceCategory, DeviceSoftwareRepository, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device


class TestRepositoryAPI(unittest.TestCase):
    def setUp(self):
        self.device = Device(
            personality="vedge",
            uuid="mock_uuid",
            id="mock_ip",
            hostname="mock_host",
            reachability="reachable",
            local_system_ip="mock_ip",
            status="normal",
            memUsage=1.0,
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
        )
        self.DeviceSoftwareRepository_obj = {
            "mock_uuid": DeviceSoftwareRepository(
                ["ver1", "ver2", "curr_ver"],
                ["ver1", "ver2"],
                "curr_ver",
                "def_ver",
                "mock_uuid",
            )
        }

    @patch("vmngclient.session.Session")
    def test_get_image_version_if_image_available(self, mock_session):

        versions_response = [{"availableFiles": "vmanage-20.9.1-x86_64.tar.gz", "versionName": "20.9.1"}]
        mock_session.get_data.return_value = versions_response
        image_version = "20.9.1"
        answer = RepositoryAPI(mock_session).get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, image_version, "not same version")

    @patch("vmngclient.session.Session")
    def test_get_image_version_if_image_unavailable(self, mock_session):

        api_mock_response = [{"availableFiles": "vmanage-20.9.2-x86_64.tar.gz", "versionName": "20.9.1"}]
        mock_session.get_data.return_value = api_mock_response
        image_version = None
        answer = RepositoryAPI(mock_session).get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, image_version, "not same version")

    @patch("vmngclient.session.Session")
    def test_get_devices_versions_repository(self, mock_session):

        api_mock_response = [
            {
                "availableVersions": ["ver1", "ver2"],
                "version": "curr_ver",
                "defaultVersion": "def_ver",
                "uuid": "mock_uuid",
            }
        ]
        mock_session.get_data.return_value = api_mock_response
        mock_repository_object = RepositoryAPI(mock_session)

        answer = mock_repository_object.get_devices_versions_repository(DeviceCategory.CONTROLLERS.value)

        self.assertEqual(
            answer["mock_uuid"],
            self.DeviceSoftwareRepository_obj["mock_uuid"],
            "DeviceSoftwareRepository object created uncorrectly",
        )

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_get_device_list_in_available(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session)
        mock_device_versions = DeviceVersions(mock_repository_object, DeviceCategory.CONTROLLERS.value)
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        answer = mock_device_versions.get_device_list_in_available("ver1", [self.device])
        expected_result = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]

        # Assertcom
        self.assertEqual(
            answer,
            expected_result,
            "Version add incorrectly",
        )

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_get_device_list_if_in_installed(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session)
        mock_device_versions = DeviceVersions(mock_repository_object, DeviceCategory.CONTROLLERS.value)
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        answer = mock_device_versions.get_device_list_in_installed("ver1", [self.device])
        expected_result = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]

        # Assert
        self.assertEqual(
            answer,
            expected_result,
            "Version add incorrectly",
        )
