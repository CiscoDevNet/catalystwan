import logging
from typing import Dict, List, cast

from vmngclient.api.versions_utils import (
    DeviceCategory,
    DeviceVersionPayload,
    DeviceVersions,
    RemovePartitionPayload,
    RepositoryAPI,
)
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
        payload_devices = DeviceVersions(provider,DeviceCategory.CONTROLLERS).get_devices_current_version(cedges)
        partition_manager = PartitionManagerAPI(provider_session_as_tenant_session,DeviceCategory.VEDGES)
        set_partition_id = partition_manager.set_default_partition(payload_devices)

        # Check action status
        wait_for_completed(session, set_partition_id, 3000)

    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session, device_category)

    def set_default_partition(self, payload_devices: List[DeviceVersionPayload]) -> str:

        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": [asdict(device) for device in payload_devices],  # type: ignore
            "deviceType": "vmanage",
        }
        set_default = dict(self.session.post(url, json=payload).json())
        return set_default["id"]

    def remove_partition(self, devices_payload: List[DeviceVersionPayload], force: bool = False) -> str:
        """
        Remove chosen software version from Vmanage repository

        Args:
            devices (List[Device]): remove partition for those devices
            version (str): software version to be removed from repository
            force (bool): bypass version checks

        Returns:
            str: action id
        """

        devices_payload = [
            RemovePartitionPayload(device.deviceId, device.deviceIP, device.version) for device in devices_payload
        ]
        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": [asdict(device) for device in devices_payload],  # type: ignore
            "deviceType": "vmanage",
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
