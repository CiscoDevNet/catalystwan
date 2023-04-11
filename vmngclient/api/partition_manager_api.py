from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Optional, cast

from vmngclient.api.task_status_api import Task
from vmngclient.api.versions_utils import DeviceVersions, RemovePartitionPayload, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import asdict
from vmngclient.utils.upgrades_helper import get_install_specification, validate_personality_homogeneity

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class PartitionManagerAPI:
    """
    API methods for partitions actions. All methods
    are exececutable on all device categories.

    Usage example:
        # Create session
        session = create_vManageSession(...)

        # Prepare devices list
        devices = session.api.devices.get()
        vsmarts = devices.filter(personality=Personality.VSMART)

        # Set current partion as default partition
        partition_manager = PartitionManagerAPI(session)
        set_partition_id = partition_manager.set_default_partition(vsmarts)

        # Check action status
        TaskAPI(session, software_action_id).wait_for_completed()

    """

    def __init__(self, session: vManageSession) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_version = DeviceVersions(self.session)

    def set_default_partition(self, devices: DataSequence[Device], partition: Optional[str] = None) -> Task:
        """
        Set defualt software versions for devices

        Args:
            devices (DataSequence[Device]): devices
            partition (Optional[str], optional): If none, current partition will be set as default,
                else selected partition will be set as default

        Returns:
            str: set partition task id
        """
        validate_personality_homogeneity(devices)
        if partition:
            payload_devices = self.device_version.get_device_available(partition, devices)
        else:
            payload_devices = self.device_version.get_devices_current_version(devices)

        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": [asdict(device) for device in payload_devices],  # type: ignore
            "deviceType": get_install_specification(devices.first()).device_type.value,
        }
        set_default = dict(self.session.post(url, json=payload).json())
        return Task(self.session, set_default["id"])

    def remove_partition(
        self, devices: DataSequence[Device], partition: Optional[str] = None, force: bool = False
    ) -> Task:
        """
        Remove chosen software version from device

        Args:
            devices (DataSequence[Device]): remove partition for those devices
            partition (str): If none, all availables partitions will be removed,
                else selected partition will be removed
            force (bool): bypass version checks

        Returns:
            str: action id
        """
        validate_personality_homogeneity(devices)
        if partition:
            payload_devices = self.device_version.get_device_available(partition, devices)
        else:
            payload_devices = self.device_version.get_devices_available_versions(devices)

        remove_partition_payload = [
            RemovePartitionPayload(device.deviceId, device.deviceIP, device.version)  # type: ignore
            for device in payload_devices
        ]

        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": [asdict(device) for device in remove_partition_payload],  # type: ignore
            "deviceType": get_install_specification(devices.first()).device_type.value,
        }
        if force is False:
            self._check_remove_partition_possibility(cast(list, payload["devices"]))
        remove_action: Dict[str, str] = self.session.post(url, json=payload).json()
        return Task(self.session, remove_action["id"])

    def _check_remove_partition_possibility(self, payload_devices: List[dict]) -> None:
        devices_versions_repository = self.repository.get_devices_versions_repository()
        invalid_devices = []
        for device in payload_devices:

            if device["version"] in (
                devices_versions_repository[device["deviceId"]].current_version,
                devices_versions_repository[device["deviceId"]].default_version,
            ):
                invalid_devices.append((device["deviceId"]))
        if invalid_devices:
            raise ValueError(
                f"Current or default version of devices with ids {invalid_devices} \
                    are equal to remove version. Action denied!"
            )
