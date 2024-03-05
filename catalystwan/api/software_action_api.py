# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional, cast

from catalystwan.api.task_status_api import Task
from catalystwan.api.versions_utils import DeviceVersions, RepositoryAPI
from catalystwan.endpoints.configuration_device_actions import (
    InstallActionPayload,
    InstallData,
    InstallDevice,
    InstallInput,
    PartitionActionPayload,
)
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
from catalystwan.exceptions import EmptyVersionPayloadError, ImageNotInRepositoryError  # type: ignore
from catalystwan.typed_list import DataSequence
from catalystwan.utils.personality import Personality
from catalystwan.utils.upgrades_helper import get_install_specification, validate_personality_homogeneity
from catalystwan.version import parse_vmanage_version

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class SoftwareActionAPI:
    """
    API methods for software actions. All methods
    are exececutable on all device categories.

    Usage example:
    # Create session
    session = create_manager_session(...)

    # Prepare devices list
    controllers = session.endpoints.configuration_device_inventory.get_device_details('controllers')
    vsmarts = controllers.filter(personality=Personality.VSMART)
    software_image = "viptela-20.7.2-x86_64.tar.gz"

    # Upgrade
    upgrade_id = SoftwareActionAPI(session).install(devices = vsmarts, software_image=software_image)

    # Check upgrade status
    TaskAPI(session, software_action_id).wait_for_completed()
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session)

    def activate(
        self,
        devices: DataSequence[DeviceDetailsResponse],
        version_to_activate: Optional[str] = "",
        image: Optional[str] = "",
    ) -> Task:
        """
        Set chosen version as current version. Requires that selected devices have already version_to_activate
        or image present in their available files.

        Args:
            devices (List[DeviceDetailsResponse]): For those devices software will be activated
            version_to_activate (Optional[str]): version to be set as current version
            image (Optional[str]): software image name in available files

            Notice: Have to pass one of those arguments (version_to_activate, image)

        Raises:
            EmptyVersionPayloadError: If selected version_to_activate or image not detected in available files

        Returns:
            str: Activate software action id
        """
        validate_personality_homogeneity(devices)
        if image and not version_to_activate:
            version = cast(str, self.repository.get_image_version(image))
        elif version_to_activate and not image:
            version = cast(str, version_to_activate)
        else:
            raise ValueError("You can not provide software_image and image version at the same time!")

        if not version:
            raise ImageNotInRepositoryError(
                "Based on provided arguments, software version to activate on device(s) cannot be detected."
            )

        payload_devices = self.device_versions.get_device_available(version, devices)
        for device in payload_devices:
            if not device.version:
                raise EmptyVersionPayloadError("PartitionDevice payload contains entry with empty version field.")

        device_type = get_install_specification(devices.first()).device_type.value
        partition_payload = PartitionActionPayload(
            action="changepartition", devices=[dev for dev in payload_devices], device_type=device_type
        )

        partition_action = self.session.endpoints.configuration_device_actions.process_mark_change_partition(
            payload=partition_payload
        )

        return Task(self.session, partition_action.id)

    def install(
        self,
        devices: DataSequence[DeviceDetailsResponse],
        reboot: bool = False,
        sync: bool = True,
        v_edge_vpn: int = 0,
        v_smart_vpn: int = 0,
        image: Optional[str] = None,
        image_version: Optional[str] = None,
        downgrade_check: bool = True,
        remote_server_name: Optional[str] = None,
        remote_image_filename: Optional[str] = None,
    ) -> Task:
        """
        Method to install new software

        Args:
            devices (List[DeviceDetailsResponse]): For those devices software will be activated
            reboot (bool, optional): reboot device after action end
            sync (bool, optional): Synchronize settings. Defaults to True.
            v_edge_vpn (int, optional): vEdge VPN
            v_smart_vpn (int, optional): vSmart VPN
            image (str): path to software image or its name from available files
            image_version (str): version of software image
            downgrade_check (bool, optional): perform a downgrade check when applicable
            remote_server_name (str): name of configured Remote Server
            remote_image_filename (str): filename to choose from selected Remote Server

            Notice: Have to pass one of those:
                - image_version
                - image
                - remote_server_name and remote_image_filename

        Raises:
            ValueError: Raise error if downgrade in certain cases or wrong arguments combination provided
            ImageNotInRepositoryError: If selected image, image_version or remote_image_filename not found

        Returns:
            Task: Task object representing started install process
        """
        validate_personality_homogeneity(devices)

        if (
            sum(
                [
                    image is not None,
                    image_version is not None,
                    all([remote_server_name is not None, remote_image_filename is not None]),
                ]
            )
            != 1
        ):
            raise ValueError(
                "Please provide one option to detect software to install. "
                "Pick either 'image', 'image_version', or both 'remote_server_name' and 'remote_image_filename'."
            )

        # FIXME downgrade_check will be supported when software images from Remote Server will have versions fields
        if remote_server_name and remote_image_filename and downgrade_check:
            raise ValueError("Downgrade check is not supported for install action for images from Remote Server.")

        version, remote_image_details = None, None
        if image:
            version = cast(str, self.repository.get_image_version(image))
        if image_version:
            version = cast(str, image_version)
        if remote_server_name and remote_image_filename:
            remote_image_details = self.repository.get_remote_image(remote_image_filename, remote_server_name)

        if not any([version, remote_image_details]):
            raise ImageNotInRepositoryError(
                "Based on provided arguments, software version to install on device(s) cannot be detected."
            )

        install_specification = get_install_specification(devices.first(), remote=bool(remote_image_details))
        install_devices = [
            InstallDevice(**device.model_dump(by_alias=True))
            for device in self.device_versions.get_device_list(devices)
        ]

        if version:
            input = InstallInput(
                v_edge_vpn=v_edge_vpn,
                v_smart_vpn=v_smart_vpn,
                family=install_specification.family.value,
                version=version,
                version_type=install_specification.version_type.value,
                reboot=reboot,
                sync=sync,
            )
        else:
            input = InstallInput(
                v_edge_vpn=v_edge_vpn,
                v_smart_vpn=v_smart_vpn,
                data=[
                    InstallData(
                        family=install_specification.family.value,
                        version=remote_image_details.version_id,  # type: ignore
                        remote_server_id=remote_image_details.remote_server_id,  # type: ignore
                        version_id=remote_image_details.version_id,  # type: ignore
                    )
                ],
                version_type=install_specification.version_type.value,
                reboot=reboot,
                sync=sync,
            )

        device_type = install_specification.device_type.value
        install_payload = InstallActionPayload(
            action="install", input=input, devices=install_devices, device_type=device_type
        )

        if downgrade_check and devices.first().personality in (Personality.VMANAGE, Personality.EDGE):
            self._downgrade_check(
                install_payload.devices,
                install_payload.input.version,  # type: ignore
                install_specification.family.value,  # type: ignore
            )

        install_action = self.session.endpoints.configuration_device_actions.process_install_operation(
            payload=install_payload
        )

        return Task(self.session, install_action.id)

    def _downgrade_check(self, payload_devices: List[InstallDevice], version_to_upgrade: str, family: str) -> None:
        """
        Check if upgrade operation is not actually a downgrade opeartion.
        If so, in some cases action is being blocked.

        Args:
            version_to_upgrade (str): version to upgrade
            payload_devices List[InstallDevice]: list of Devices to check downgrade possibility

        Raises:
            ValueError: If for any of the devices upgrade action is denied
        """
        incorrect_devices = []
        devices_versions_repo = self.repository.get_devices_versions_repository()
        for device in payload_devices:
            current_version = parse_vmanage_version(devices_versions_repo[device.device_id].current_version)
            upgrade_version = parse_vmanage_version(version_to_upgrade)
            # check if downgrade
            if current_version > upgrade_version:
                logger.warning(
                    f"Requested to downgrade device: {device.device_id} from {current_version} to {upgrade_version}"
                )
                # allow vmanage downgrade only if major and minor version match, downgrade for other devices is allowed
                if family == "vmanage":
                    if not current_version.release[:2] == upgrade_version.release[:2]:
                        logger.error(
                            f"Blocking downgrade of device: {device.device_id} "
                            f"from {current_version.release} to {upgrade_version.release}"
                        )
                        incorrect_devices.append(device)

        if incorrect_devices:
            raise ValueError(
                f"Current version of devices with id's {incorrect_devices} is "
                "higher than upgrade version. Action denied!"
            )
