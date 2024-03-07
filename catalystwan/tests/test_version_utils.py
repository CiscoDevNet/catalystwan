# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, Mock, patch

from catalystwan.api.versions_utils import DeviceSoftwareRepository, DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration.software_actions import SoftwareImageDetails
from catalystwan.endpoints.configuration_device_actions import InstalledDeviceData, PartitionDevice
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.typed_list import DataSequence


class TestRepositoryAPI(unittest.TestCase):
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
                version="curr_ver",
                defaultVersion="def_ver",
                uuid="mock_uuid",
            )
        }
        mock_session = Mock()
        self.mock_repository_object = RepositoryAPI(mock_session)

    @patch("catalystwan.session.Session")
    def test_get_image_version_if_image_available(self, mock_session):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [SoftwareImageDetails(**{"availableFiles": "vmanage-20.9.1-x86_64.tar.gz", "versionName": "20.9.1"})],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)
        image_version = "20.9.1"
        answer = self.mock_repository_object.get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, image_version, "not same version")

    @patch("catalystwan.session.Session")
    def test_get_image_version_if_image_unavailable(self, mock_session):
        api_mock_response = [{"availableFiles": "vmanage-20.9.2-x86_64.tar.gz", "versionName": "20.9.1"}]
        mock_session.get_data.return_value = api_mock_response
        image_version = None
        answer = RepositoryAPI(mock_session).get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, image_version, "not same version")

    def test_get_remote_image(self):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": "abcd-1234",
                    }
                )
            ],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)
        answer = self.mock_repository_object.get_remote_image("vmanage-20.9.1-x86_64.tar.gz", "remote-server-test")

        self.assertEqual(answer.version_id, "abcd-1234", "not same version")

    def test_get_remote_image_non_existing(self):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": "abcd-1234",
                    }
                )
            ],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)
        answer = self.mock_repository_object.get_remote_image("vmanage-20.10.1-x86_64.tar.gz", "remote-server-test")

        self.assertEqual(answer, None, "not same version")

    def test_get_remote_image_no_version_id(self):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": None,
                    }
                )
            ],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)

        with self.assertRaises(ValueError):
            self.mock_repository_object.get_remote_image("vmanage-20.9.1-x86_64.tar.gz", "remote-server-test")

    def test_get_version_when_same_available_file_present_for_remote_version(self):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": "abcd-1234",
                    }
                ),
                SoftwareImageDetails(**{"availableFiles": "vmanage-20.9.1-x86_64.tar.gz", "versionName": "20.9.1"}),
            ],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)
        image_version = "20.9.1"
        answer = self.mock_repository_object.get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, image_version, "not same version")

    def test_get_version_when_remote_available_file_is_matching(self):
        versions_response = DataSequence(
            SoftwareImageDetails,
            [
                SoftwareImageDetails(
                    **{
                        "availableFiles": "vmanage-20.9.1-x86_64.tar.gz",
                        "versionType": "remote-server-test",
                        "remoteServerId": "123456789-abcdabcd",
                        "versionId": "abcd-1234",
                    }
                ),
                SoftwareImageDetails(**{"availableFiles": "vmanage-20.10.1-x86_64.tar.gz", "versionName": "20.9.1"}),
            ],
        )
        self.mock_repository_object.get_all_software_images = MagicMock(return_value=versions_response)
        answer = self.mock_repository_object.get_image_version("vmanage-20.9.1-x86_64.tar.gz")

        self.assertEqual(answer, None)

    @patch("catalystwan.session.Session")
    def test_get_devices_versions_repository(self, mock_session):
        endpoint_mock_response = DataSequence(
            InstalledDeviceData,
            [
                InstalledDeviceData(
                    **{
                        "availableVersions": ["ver1", "ver2"],
                        "version": "curr_ver",
                        "defaultVersion": "def_ver",
                        "uuid": "mock_uuid",
                    }
                )
            ],
        )

        self.mock_repository_object.session.endpoints.configuration_device_actions.get_list_of_installed_devices = (
            MagicMock(return_value=endpoint_mock_response)
        )

        answer = self.mock_repository_object.get_devices_versions_repository()

        self.assertEqual(
            answer["mock_uuid"],
            self.DeviceSoftwareRepository_obj["mock_uuid"],
            "DeviceSoftwareRepository object created uncorrectly",
        )

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_get_device_available(self, mock_get_devices_versions_repository):
        # Prepare mock data
        mock_get_devices_versions_repository.return_value = Mock()
        mock_session = Mock()
        mock_repository_object = RepositoryAPI(mock_session)
        mock_device_versions = DeviceVersions(mock_repository_object)
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        answer = mock_device_versions.get_device_available("ver1", [self.device])
        expected_result = DataSequence(
            PartitionDevice, [PartitionDevice(device_id="mock_uuid", device_ip="mock_ip", version="ver1")]
        )

        # Assert
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
        mock_device_versions = DeviceVersions(mock_repository_object)
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        answer = mock_device_versions.get_device_list_in_installed("ver1", [self.device])
        expected_result = DataSequence(
            PartitionDevice, [PartitionDevice(device_id="mock_uuid", device_ip="mock_ip", version="ver1")]
        )

        # Assert
        self.assertEqual(
            answer,
            expected_result,
            "Version add incorrectly",
        )

    @patch.object(RepositoryAPI, "get_devices_versions_repository")
    def test_get_devices_current_version(self, mock_get_devices_versions_repository):
        # Arrange
        mock_session = Mock()
        mock_get_devices_versions_repository.return_value = Mock()
        mock_get_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_repository_object = RepositoryAPI(mock_session)
        mock_device_versions = DeviceVersions(mock_repository_object)
        # Act
        answer = mock_device_versions.get_devices_current_version([self.device])
        # Answer
        proper_answer = DataSequence(
            PartitionDevice, [PartitionDevice(device_id="mock_uuid", device_ip="mock_ip", version="curr_ver")]
        )
        self.assertEqual(answer, proper_answer)
