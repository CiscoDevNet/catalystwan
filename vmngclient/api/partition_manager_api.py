from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, cast

from vmngclient.api.software_action_api import DeviceType
from vmngclient.api.versions_utils import (
    DeviceCategory,
    DeviceVersionPayload,
    DeviceVersions,
    RemovePartitionPayload,
    RepositoryAPI,
)
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import asdict

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
        devices = [device for device in DevicesAPI(session).devices
                    if device.personality == VSMART]

        # Set default partition
        payload_devices = DeviceVersions(provider,DeviceCategory.CONTROLLERS).get_devices_current_version(devices)
        partition_manager = PartitionManagerAPI(provider_session_as_tenant_session,DeviceCategory.CONTROLLERS,
                            DeviceType.CONTROLLERS)
        set_partition_id = partition_manager.set_default_partition(payload_devices)

        # Check action status
        wait_for_completed(session, set_partition_id, 3000)

    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory, device_type: DeviceType) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session, device_category)
        self.device_type = device_type

    def set_default_partition(self, payload_devices: DataSequence[DeviceVersionPayload]) -> str:

        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": [asdict(device) for device in payload_devices],  # type: ignore
            "deviceType": self.device_type.value,
        }
        set_default = dict(self.session.post(url, json=payload).json())
        return set_default["id"]

    def remove_partition(self, devices_payload: DataSequence[DeviceVersionPayload], force: bool = False) -> str:
        """
        Remove chosen software version from Vmanage repository

        Args:
            devices (List[Device]): remove partition for those devices
            version (str): software version to be removed from repository
            force (bool): bypass version checks

        Returns:
            str: action id
        """

        remove_partition_payload = [
            RemovePartitionPayload(device.deviceId, device.deviceIP, device.version) for device in devices_payload
        ]
        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": [asdict(device) for device in remove_partition_payload],  # type: ignore
            "deviceType": self.device_type.value,
        }
        if force is False:
            self._check_remove_partition_possibility(cast(list, payload["devices"]))
        remove_action: Dict[str, str] = self.session.post(url, json=payload).json()
        return remove_action["id"]

    def _check_remove_partition_possibility(self, payload_devices: List[dict]) -> None:
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
        if invalid_devices:
            raise ValueError(
                f"Current or default version of devices with ids {invalid_devices} \
                    are equal to remove version. Action denied!"
            )
