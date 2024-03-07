# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional, cast

from catalystwan.api.task_status_api import Task
from catalystwan.api.versions_utils import DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration_device_actions import (
    PartitionActionPayload,
    RemovePartitionActionPayload,
    RemovePartitionDevice,
)
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.exceptions import EmptyVersionPayloadError
from catalystwan.typed_list import DataSequence
from catalystwan.utils.upgrades_helper import get_install_specification, validate_personality_homogeneity

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class PartitionManagerAPI:
    """
    API methods for partitions actions. All methods
    are exececutable on all device categories.

    Usage example:
        # Create session
        session = create_manager_session(...)

        # Prepare devices list
        devices = session.api.devices.get()
        vsmarts = devices.filter(personality=Personality.VSMART)

        # Set current partion as default partition
        partition_manager = PartitionManagerAPI(session)
        set_partition_id = partition_manager.set_default_partition(vsmarts)

        # Check action status
        TaskAPI(session, software_action_id).wait_for_completed()

    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_version = DeviceVersions(self.session)

    def set_default_partition(
        self, devices: DataSequence[DeviceDetailsResponse], partition: Optional[str] = None
    ) -> Task:
        """
        Set default software versions for devices

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

        for device in payload_devices:
            if not device.version:
                raise EmptyVersionPayloadError("PartitionDevice payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        partition_payload = PartitionActionPayload(
            action="defaultpartition", devices=[dev for dev in payload_devices], device_type=device_type
        )

        partition_action = self.session.endpoints.configuration_device_actions.process_mark_default_partition(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)

    def remove_partition(
        self, devices: DataSequence[DeviceDetailsResponse], partition: Optional[str] = None, force: bool = False
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

        for device in payload_devices:
            if not device.version:
                raise EmptyVersionPayloadError("PartitionDevice payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        partition_payload = RemovePartitionActionPayload(
            action="removepartition",
            devices=[RemovePartitionDevice(**dev.model_dump()) for dev in payload_devices],
            device_type=device_type,
        )

        if force is False:
            self._check_remove_partition_possibility(cast(list, partition_payload.devices))

        partition_action = self.session.endpoints.configuration_device_actions.process_remove_partition(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)

    def _check_remove_partition_possibility(self, payload_devices: List[RemovePartitionDevice]) -> None:
        devices_versions_repository = self.repository.get_devices_versions_repository()
        invalid_devices = []
        for device in payload_devices:
            for version in device.version:
                if version in (
                    devices_versions_repository[device.device_id].current_version,
                    devices_versions_repository[device.device_id].default_version,
                ):
                    invalid_devices.append((device.device_id))
        if invalid_devices:
            raise ValueError(
                f"Current or default version of devices with ids {invalid_devices} \
                    are equal to remove version. Action denied!"
            )
