# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, Mock, patch

from catalystwan.api.software_action_api import SoftwareActionAPI
from catalystwan.api.versions_utils import DeviceSoftwareRepository, DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration.software_actions import SoftwareImageDetails
from catalystwan.endpoints.configuration_device_actions import ActionId, InstallDevice, PartitionDevice
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.exceptions import ImageNotInRepositoryError
from catalystwan.typed_list import DataSequence
from catalystwan.utils.upgrades_helper import Family, InstallSpecHelper


class TestSoftwareAcionAPI(unittest.TestCase):
    def setUp(self):
        self.device = DeviceDetailsResponse(
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
        self.DeviceSoftwareRepository_obj = {
            "mock_uuid": DeviceSoftwareRepository(
                installed_versions=["ver1", "ver2", "curr_ver"],
                availableVersions=["ver1", "ver2"],
                version="20.8",
                defaultVersion="def_ver",
                uuid="mock_uuid",
            ),
        }

        self.mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]
        self.install_spec = InstallSpecHelper.VMANAGE.value

        mock_session = Mock()
        self.mock_repository_object = RepositoryAPI(mock_session)
        self.mock_device_versions = DeviceVersions(self.mock_repository_object)
        self.mock_software_action_obj = SoftwareActionAPI(mock_session)

    @patch.object(SoftwareActionAPI, "_downgrade_check")
    @patch.object(RepositoryAPI, "get_image_version")
    def test_upgrade_software_if_downgrade_check_is_none(self, mock_get_image_version, mock_downgrade_check):
        # Prepare mock data
        mock_downgrade_check.return_value = False
        expected_id = ActionId(id="mock_action_id")
        mock_get_image_version.return_value = "any_version"
        self.mock_software_action_obj.session.endpoints.configuration_device_actions.process_install_operation = (
            MagicMock(return_value=expected_id)
        )

        # Assert
        answer = self.mock_software_action_obj.install(
            devices=DataSequence(DeviceDetailsResponse, [self.device]),
            reboot=True,
            sync=True,
            image="path",
        )
        self.assertEqual(answer.task_id, "mock_action_id")

    @patch.object(DeviceVersions, "get_device_available")
    @patch.object(RepositoryAPI, "get_all_software_images")
    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_activate_software(
        self, mock_get_devices_versions_repository, mock_get_all_software_images, mock_get_device_available
    ):
        # Prepare mock data
        expected_id = ActionId(id="mock_action_id")
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_get_device_available.return_value = DataSequence(
            PartitionDevice, [PartitionDevice(device_id="mock_uuid", device_ip="mock_ip", version="ver2")]
        )
        mock_get_all_software_images.return_value = DataSequence(
            SoftwareImageDetails,
            [SoftwareImageDetails(**{"availableFiles": "vmanage-20.9.1-x86_64.tar.gz", "versionName": "ver2"})],
        )

        self.mock_software_action_obj.session.endpoints.configuration_device_actions.process_mark_change_partition = (
            MagicMock(return_value=expected_id)
        )

        # Assert
        answer = self.mock_software_action_obj.activate(
            devices=DataSequence(DeviceDetailsResponse, [self.device]),
            image="vmanage-20.9.1-x86_64.tar.gz",
        )
        self.assertEqual(answer.task_id, "mock_action_id")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_downgrade_check_no_incorrect_devices(self, mock_get_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.9"
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [InstallDevice(**{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version})]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(mock_devices, upgrade_version, Family.VMANAGE.value)
        self.assertEqual(answer, None, "downgrade detected, but should not")

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_downgrade_check_incorrect_devices_exists(self, mock_get_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.6"
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [InstallDevice(**{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version})]
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

    def test_install_software_from_remote_image_not_available_with_downgrade_check(self):
        with self.assertRaises(ValueError):
            self.mock_software_action_obj.install(
                devices=DataSequence(DeviceDetailsResponse, [self.device]),
                remote_server_name="dummy",
                remote_image_filename="dummy",
            )

    @patch.object(RepositoryAPI, "get_all_software_images")
    def test_install_software_from_remote_image_with_wrong_version(self, mock_get_all_software_images):
        mock_get_all_software_images.return_value = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": "ver1",
                    }
                )
            ],
        )

        with self.assertRaises(ImageNotInRepositoryError):
            self.mock_software_action_obj.install(
                devices=DataSequence(DeviceDetailsResponse, [self.device]),
                remote_server_name="remote-server-test",
                remote_image_filename="not-ver1",
                downgrade_check=False,
            )
