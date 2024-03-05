# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, Mock, patch

from catalystwan.api.partition_manager_api import PartitionManagerAPI
from catalystwan.api.versions_utils import DeviceSoftwareRepository, DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration_device_actions import ActionId, RemovePartitionDevice
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.typed_list import DataSequence


class TestPartitionManagerAPI(unittest.TestCase):
    def setUp(self):
        self.device = DataSequence(
            DeviceDetailsResponse,
            [
                DeviceDetailsResponse(
                    personality="vedge",
                    uuid="mock_uuid",
                    device_ip="mock_ip",
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
                installed_versions=["ver1", "ver2", "curr_ver"],
                availableVersions=["ver1", "ver2"],
                version="curr_ver",
                defaultVersion="def_ver",
                uuid="mock_uuid",
            ),
        }

        self.mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]
        self.mock_device_version_payload = DataSequence(
            RemovePartitionDevice, [RemovePartitionDevice(device_id="mock_uuid", device_ip="mock_ip", version="ver1")]
        )
        mock_session = Mock()
        self.mock_repository_object = RepositoryAPI(mock_session)
        self.mock_device_versions = DeviceVersions(self.mock_repository_object)
        self.mock_partition_manager_obj = PartitionManagerAPI(mock_session)

    @patch("catalystwan.utils.upgrades_helper.get_install_specification")
    @patch.object(DeviceVersions, "get_devices_available_versions")
    def test_remove_partition_if_force_true(self, mock_get_device_list, mock_get_spec):
        # Prepare mock data
        mock_get_device_list.return_value = Mock()
        mock_devices = Mock()
        mock_devices.return_value = self.mock_devices
        mock_get_device_list.return_value = self.mock_device_version_payload
        self.mock_repository_object.devices = self.mock_devices
        expected_id = ActionId(id="mock_action_id")
        self.mock_repository_object.session.endpoints.configuration_device_actions.process_remove_partition = MagicMock(
            return_value=expected_id
        )

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
        expected_id = ActionId(id="mock_action_id")
        self.mock_repository_object.session.endpoints.configuration_device_actions.process_remove_partition = MagicMock(
            return_value=expected_id
        )

        # Assert
        answer = self.mock_partition_manager_obj.remove_partition(self.device, force=False).task_id
        self.assertEqual(answer, "mock_action_id", "action ids not equal")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_check_remove_partition_possibility_if_version_incorrect(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [
            RemovePartitionDevice(**{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "curr_ver"})
        ]

        # Assert
        with self.assertRaises(ValueError):
            self.mock_partition_manager_obj._check_remove_partition_possibility(mock_devices)

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_check_remove_partition_possibility_if_version_correct(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [RemovePartitionDevice(**{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "any_ver"})]

        # Assert
        answer = self.mock_partition_manager_obj._check_remove_partition_possibility(mock_devices)
        self.assertEqual(answer, None, "lists are not equal")

    @patch.object(DeviceVersions, "get_devices_current_version")
    @patch("catalystwan.session.ManagerSession")
    def test_set_default_partition(self, mock_session, mock_get_devices):
        # Arrange
        mock_partition_manager = PartitionManagerAPI(mock_session)
        expected_id = ActionId(id="id_1")
        mock_partition_manager.session.endpoints.configuration_device_actions.process_mark_default_partition = (
            MagicMock(return_value=expected_id)
        )

        # Act
        answer = mock_partition_manager.set_default_partition(self.device).task_id

        # Assert
        self.assertEqual(answer, "id_1")
