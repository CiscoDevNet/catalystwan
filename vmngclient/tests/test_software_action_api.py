import unittest
from unittest.mock import Mock, patch

from vmngclient.api.software_action_api import SoftwareActionAPI
from vmngclient.api.versions_utils import DeviceSoftwareRepository, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.typed_list import DataSequence
from vmngclient.utils.upgrades_helper import Family, InstallSpecHelper


class TestSoftwareAcionAPI(unittest.TestCase):
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
                "20.8",
                "def_ver",
                "mock_uuid",
            ),
        }

        self.mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]
        self.install_spec = InstallSpecHelper.VMANAGE.value

        mock_session = Mock()
        self.mock_repository_object = RepositoryAPI(mock_session)
        self.mock_device_versions = DeviceVersions(self.mock_repository_object)
        self.mock_software_action_obj = SoftwareActionAPI(mock_session)

    @patch("vmngclient.session.vManageSession")
    @patch.object(SoftwareActionAPI, "_downgrade_check")
    @patch.object(RepositoryAPI, "get_image_version")
    def test_upgrade_software_if_downgrade_check_is_none(
        self, mock_get_image_version, mock_downgrade_check, mock_session
    ):

        # Prepare mock data
        mock_downgrade_check.return_value = False
        self.mock_repository_object.session.post.return_value.json.return_value = {"id": "mock_action_id"}
        mock_session.post.return_value = {"id": "mock_action_id"}

        # Assert
        answer = self.mock_software_action_obj.install(DataSequence(Device, [self.device]), True, True, "path").task_id
        self.assertEqual(answer, "mock_action_id")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_downgrade_check_no_incorrect_devices(self, mock_get_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.9"
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(mock_devices, upgrade_version, Family.VMANAGE.value)
        self.assertEqual(answer, None, "downgrade detected, but should not")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_downgrade_check_incorrect_devices_exists(self, mock_get_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.6"
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        # answer = self.mock_software_action_obj._downgrade_check(mock_devices, upgrade_version, Family.VMANAGE.value)
        self.assertRaises(
            ValueError,
            self.mock_software_action_obj._downgrade_check,
            mock_devices,
            upgrade_version,
            Family.VMANAGE.value,
        )
