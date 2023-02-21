import logging
from typing import Dict, List, cast

from vmngclient.api.versions_utils import (
    DeviceCategory,
    DeviceVersionPayload,
    DeviceVersions,
    PayloadRemovePartition,
    RepositoryAPI,
)
from vmngclient.dataclasses import Device
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import asdict

logger = logging.getLogger(__name__)


class PartitionManagerAPI:
    """
    API methods for partitions actions. All methods
    are exececutable on all device categories.

    Usage example:
        # Create session
        session = create_vManageSession(...)

        # Prepare devices list
        cedges = [dev for dev in DevicesAPI(session).devices
                    if dev.hostname in ["vm5", "vm6"]]

        # Set default partition
        partition_manager = PartitionManagerAPI(provider_session_as_tenant_session,DeviceCategory.VEDGES)
        set_partition_id = partition_manager.set_default_partition(cedges, version="9.17.06.03a.0.56")

        # Check action status
        wait_for_completed(session, set_partition_id, 3000)

    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.repository, device_category)

    def _set_default_partition(self, payload_devices: List[DeviceVersionPayload]) -> str:
        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": [asdict(device) for device in payload_devices],  # type: ignore
            "deviceType": "vmanage",
        }
        set_default = dict(self.session.post(url, json=payload).json())
        return set_default["id"]

    def set_current_partition_as_default(self, devices: List[Device]) -> str:
        """
        Set current software version as default version

        Args:
            devices (List[Device]): For those devices default partition is
                going to be set

        Returns:
            str: set default partition action id
        """
        devices_current_versions = self.device_versions.get_devices_current_version(devices)
        return self._set_default_partition(devices_current_versions)

    def set_default_partition(self, devices: List[Device], version: str) -> str:
        """
        Set chosen software version as default version

        Args:
            devices (List[Device]): For those devices default partition
            going to be set
            version (str): version to be set as default version

        Returns:
            str: action id
        """

        devices_version = self.device_versions.get_device_list_in_installed(version, devices)
        return self._set_default_partition(devices_version)

    def remove_partition(self, devices: List[Device], version: str, force: bool = False) -> str:
        """
        Remove chosen software version from Vmanage repository

        Args:
            devices (List[Device]): remove partition for those devices
            version (str): software version to be removed from repository
            force (bool): bypass version checks

        Returns:
            str: action id
        """

        url = "/dataservice/device/action/removepartition"
        devices_payload = [
            PayloadRemovePartition(device.deviceId, device.deviceIP, [cast(str, device.version)])
            for device in self.device_versions.get_device_available(version, devices)
        ]
        payload = {
            "action": "removepartition",
            "devices": [asdict(device) for device in devices_payload],  # type: ignore
            "deviceType": "vmanage",
        }
        if force is False:
            invalid_devices = self._check_remove_partition_possibility(cast(list, payload["devices"]))
            if invalid_devices:
                raise ValueError(
                    f"Current or default version of devices with ids {invalid_devices} \
                        are equal to remove version. Action denied!"
                )
        remove_action: Dict[str, str] = self.session.post(url, json=payload).json()
        return remove_action["id"]

    def remove_available_partitions(self, devices: List[Device]) -> str:
        """
        Remove all available partitions for devices in devices list.

        Args:
            devices (List[Device]): _description_

        Returns:
            str: remove action id
        """
        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": [
                asdict(device)  # type: ignore
                for device in self.device_versions.get_devices_available_versions(devices)
            ],
            "deviceType": "vmanage",
        }
        remove_action: Dict[str, str] = self.session.post(url, json=payload).json()
        return remove_action["id"]

    def _check_remove_partition_possibility(self, payload_devices: List[dict]) -> List["str"]:
        devices_versions_repository = self.repository.get_devices_versions_repository(
            self.device_versions.device_category
        )
        invalid_devices = []
        for device in payload_devices:

            if device["version"] in (
                devices_versions_repository[device["deviceId"]].current_version,
                devices_versions_repository[device["deviceId"]].default_version,
            ):
                invalid_devices.append((device["deviceId"]))
        return invalid_devices
