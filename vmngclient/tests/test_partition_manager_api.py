import unittest
from unittest.mock import Mock, patch

from vmngclient.api.partition_manager_api import PartitionManagerAPI
from vmngclient.api.versions_utils import DeviceSoftwareRepository, DeviceVersionPayload, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.typed_list import DataSequence


class TestPartitionManagerAPI(unittest.TestCase):
    def setUp(self):
        self.device = DataSequence(
            Device,
            [
                Device(
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
            ],
        )
        self.DeviceSoftwareRepository_obj = {
            "mock_uuid": DeviceSoftwareRepository(
                ["ver1", "ver2", "curr_ver"],
                ["ver1", "ver2"],
                "curr_ver",
                "def_ver",
                "mock_uuid",
            ),
        }

        self.mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]
        self.mock_device_version_payload = DataSequence(
            DeviceVersionPayload, [DeviceVersionPayload("mock_uuid", "mock_ip", "ver1")]
        )
        mock_session = Mock()
        self.mock_repository_object = RepositoryAPI(mock_session)
        self.mock_device_versions = DeviceVersions(self.mock_repository_object)
        self.mock_partition_manager_obj = PartitionManagerAPI(mock_session)

    @patch("vmngclient.utils.upgrades_helper.get_install_specification")
    @patch.object(DeviceVersions, "get_devices_available_versions")
    def test_remove_partition_if_force_true(self, mock_get_device_list, mock_get_spec):
        # Prepare mock data
        mock_get_device_list.return_value = Mock()
        mock_devices = Mock()
        mock_devices.return_value = self.mock_devices
        mock_get_device_list.return_value = self.mock_device_version_payload
        self.mock_repository_object.devices = self.mock_devices
        self.mock_repository_object.session.post.return_value.json.return_value = {"id": "mock_action_id"}

        # Assert
        answer = self.mock_partition_manager_obj.remove_partition(self.device, force=True).task_id
        self.assertEqual(answer, "mock_action_id")

    @patch.object(PartitionManagerAPI, "_check_remove_partition_possibility")
    @patch.object(DeviceVersions, "get_devices_available_versions")
    def test_remove_partition_not_raise_error_force_false(self, mock_get_device_list, mock_check_remove):
        # Prepare mock data
        mock_get_device_list.return_value = self.mock_device_version_payload
        mock_check_remove.return_value = []
        self.mock_repository_object.devices = self.mock_devices
        self.mock_repository_object.session.post.return_value.json.return_value = {"id": "mock_action_id"}

        # Assert
        answer = self.mock_partition_manager_obj.remove_partition(self.device, force=False).task_id
        self.assertEqual(answer, "mock_action_id", "action ids not equal")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_check_remove_partition_possibility_if_version_incorrect(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "curr_ver"}]

        # Assert
        self.assertRaises(ValueError, self.mock_partition_manager_obj._check_remove_partition_possibility, mock_devices)

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_check_remove_partition_possibility_if_version_correct(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "any_ver"}]

        # Assert
        answer = self.mock_partition_manager_obj._check_remove_partition_possibility(mock_devices)
        self.assertEqual(answer, None, "lists are not equal")

    @patch.object(DeviceVersions, "get_devices_current_version")
    @patch("vmngclient.session.vManageSession")
    def test_set_default_partition(self, mock_session, mock_get_devices):
        # Arrange
        mock_partition_manager = PartitionManagerAPI(mock_session)
        mock_partition_manager.session.post.return_value.json.return_value = {"id": "id_1"}
        # Act
        answer = mock_partition_manager.set_default_partition(self.device).task_id

        # Assert
        self.assertEqual(answer, "id_1")
