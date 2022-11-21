import unittest
from unittest.mock import Mock, patch

<<<<<<< HEAD
=======
from vmngclient.api.repository_api import (
    DeviceCategory,
    DeviceSoftwareRepository,
    RepositoryAPI,
)
from vmngclient.api.software_action_api import (
    SoftwareActionAPI,
    InstallSpecification,
    Family,
    VersionType,
    DeviceType,
)

from vmngclient.api.repository_api import DeviceCategory, DeviceSoftwareRepository, RepositoryAPI
from vmngclient.api.software_action_api import DeviceType, Family, InstallSpecification, SoftwareActionAPI, VersionType
from vmngclient.dataclasses import DeviceInfo
>>>>>>> ab43e0c (tests refactor)
from tenacity import RetryError

from vmngclient.api.repository_api import DeviceCategory, DeviceSoftwareRepository, RepositoryAPI
from vmngclient.api.software_action_api import DeviceType, Family, InstallSpecification, SoftwareActionAPI, VersionType
from vmngclient.dataclasses import Device


class TestSoftwareAcionAPI(unittest.TestCase):
    def setUp(self):
<<<<<<< HEAD
        self.device_info = Device(
=======
        self.device_info = DeviceInfo(
>>>>>>> ab43e0c (tests refactor)
            personality="vedge",
            uuid="mock_uuid",
            id="mock_ip",
            hostname="mock_host",
            reachability="reachable",
            local_system_ip="mock_ip",
            vedgeCertificateState="NA",
            cpuState="normal",
            chasisNumber="NA",
            memState="normal",
            status="normal",
            memUsage=1.0,
            cpuLoad=1.0,
            serialNumber="NA",
            configStatusMessage="NA",
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
            stateDescription="All daemons up",
            board_serial=None,
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

<<<<<<< HEAD
        self.mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}]
=======
        self.mock_devices = [
            {"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": "ver1"}
        ]
>>>>>>> ab43e0c (tests refactor)
        self.install_spec = InstallSpecification(
            Family.VMANAGE.value, VersionType.VMANAGE.value, DeviceType.VMANAGE.value
        )

        mock_session = Mock()
<<<<<<< HEAD
        self.mock_repository_object = RepositoryAPI(mock_session, [self.device_info], DeviceCategory.VMANAGE.value)
=======
        self.mock_repository_object = RepositoryAPI(
            mock_session, [self.device_info], DeviceCategory.VMANAGE.value
        )
>>>>>>> ab43e0c (tests refactor)
        self.mock_software_action_obj = SoftwareActionAPI(self.mock_repository_object)

    @patch.object(SoftwareActionAPI, "_downgrade_check")
    @patch.object(RepositoryAPI, "get_image_version")
<<<<<<< HEAD
    def test_upgrade_software_if_downgrade_check_not_none(self, mock_get_image_version, mock_downgrade_check):
=======
    def test_upgrade_software_if_downgrade_check_not_none(
        self, mock_get_image_version, mock_downgrade_check
    ):
>>>>>>> ab43e0c (tests refactor)

        # Prepare mock data
        mock_downgrade_check.return_value = ["mock_uuid"]

        # Assert
        self.assertRaises(
            ValueError,
            self.mock_software_action_obj.upgrade_software,
            "path",
            self.install_spec,
            True,
            True,
        )

    @patch.object(SoftwareActionAPI, "_downgrade_check")
    @patch.object(RepositoryAPI, "get_image_version")
<<<<<<< HEAD
    def test_upgrade_software_if_downgrade_check_is_none(self, mock_get_image_version, mock_downgrade_check):

        # Prepare mock data
        mock_downgrade_check.return_value = None
        self.mock_repository_object.session.post_json.return_value = {"id": "mock_action_id"}

        # Assert
        answer = self.mock_software_action_obj.upgrade_software("path", self.install_spec, True, True)
        self.assertEqual(answer, "mock_action_id", "action ids not equal")

    @patch.object(RepositoryAPI, "create_devices_versions_repository")
    def test_downgrade_check_no_incorrect_devices(self, mock_create_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.9"
        mock_create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(upgrade_version, DeviceCategory.VMANAGE.value)
        self.assertEqual(answer, None, "downgrade detected, but should not")

    @patch.object(RepositoryAPI, "create_devices_versions_repository")
    def test_downgrade_check_incorrect_devices_exists(self, mock_create_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.6"
        mock_create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(upgrade_version, DeviceCategory.VMANAGE.value)
=======
    def test_upgrade_software_if_downgrade_check_is_none(
        self, mock_get_image_version, mock_downgrade_check
    ):

        # Prepare mock data
        mock_downgrade_check.return_value = None
        self.mock_repository_object.session.post_json.return_value = {"id": "mock_action_id"}

        # Assert
        answer = self.mock_software_action_obj.upgrade_software("path", self.install_spec, True, True)
        self.assertEqual(answer, "mock_action_id", "action ids not equal")

    @patch.object(RepositoryAPI, "create_devices_versions_repository")
    def test_downgrade_check_no_incorrect_devices(self, mock_create_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.9"
        mock_create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(upgrade_version, DeviceCategory.VMANAGE.value)
        self.assertEqual(answer, None, "downgrade detected, but should not")

    @patch.object(RepositoryAPI, "create_devices_versions_repository")
    def test_downgrade_check_incorrect_devices_exists(self, mock_create_devices_versions_repository):
        # Preapre mock data
        upgrade_version = "20.6"
        mock_create_devices_versions_repository.return_value = self.DeviceSoftwareRepository_obj
        mock_devices = [{"deviceId": "mock_uuid", "deviceIP": "mock_ip", "version": upgrade_version}]
        self.mock_repository_object.devices = mock_devices
        # Assert
        answer = self.mock_software_action_obj._downgrade_check(
            upgrade_version, DeviceCategory.VMANAGE.value
        )
>>>>>>> ab43e0c (tests refactor)
        self.assertEqual(answer, ["mock_uuid"], "downgrade detected, but should not")

    def test_wait_for_completed_success(self):

        # Prepare mock data
<<<<<<< HEAD
        self.mock_repository_object.session.get_data.return_value = [{"status": "Success"}]

        # Assert
        answer = self.mock_software_action_obj.wait_for_completed(5, 500, ["Success", "Failure"], "mock_action_id")
=======
        self.mock_repository_object.session.get_data.return_value = [
            {"status": "Success"}
        ]

        # Assert
        answer = self.mock_software_action_obj.wait_for_completed(
            5, 500, ["Success", "Failure"], "mock_action_id"
        )
>>>>>>> ab43e0c (tests refactor)
        self.assertEqual(answer, "Success", "job status incorrect")

    def test_wait_for_completed_status_out_of_range(self):

        # Prepare mock data
<<<<<<< HEAD
        self.mock_repository_object.session.get_data.return_value = [{"status": "other_status"}]
=======
        self.mock_repository_object.session.get_data.return_value = [
            {"status": "other_status"}
        ]
>>>>>>> ab43e0c (tests refactor)
        # assert

        self.assertRaises(
            RetryError,
            self.mock_software_action_obj.wait_for_completed,
            1,
            1,
            ["Success", "Failure"],
            "mock_action_id",
        )
