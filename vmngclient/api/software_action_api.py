from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from attr import define  # type: ignore

from vmngclient.api.versions_utils import DeviceCategory, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.exceptions import VersionDeclarationError  # type: ignore
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import asdict

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class Family(Enum):
    VEDGE = "vedge"
    VMANAGE = "vmanage"


class VersionType(Enum):
    VMANAGE = "vmanage"


class DeviceType(Enum):
    CONTROLLER = "controller"
    VEDGE = "vedge"
    VMANAGE = "vmanage"


class DeviceClass(Enum):
    VEDGE = "vedge"
    VMANAGE = "vmanage"
    VSMART = "vsmart"
    VBOND = "vbond"
    CEDGE = "cedge"


@define
class InstallSpecification:

    family: Family
    version_type: VersionType
    device_type: DeviceType
    device_class: DeviceClass


class InstallSpecHelper(Enum):

    VMANAGE = InstallSpecification(Family.VMANAGE, VersionType.VMANAGE, DeviceType.VMANAGE, DeviceClass.VMANAGE)
    VSMART = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER, DeviceClass.VSMART)
    VBOND = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER, DeviceClass.VBOND)
    VEDGE = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.VEDGE, DeviceClass.VEDGE)
    CEDGE = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.VEDGE, DeviceClass.CEDGE)


class SoftwareActionAPI:
    """
    API methods for software actions. All methods
    are exececutable on all device categories.

    Usage example:
    # Create session
    session = create_vManageSession(...)

    # Prepare devices list
    devices = [device for device in DevicesAPI(session).devices
                if device .personality == Personality.VSMART]
    software_image = "viptela-20.7.2-x86_64.tar.gz"

    # Upgrade
    devices_payload = DeviceVersions(session, DeviceCategory.CONTROLLERS).get_devices_current_version(devices)
    software_action = SoftwareActionAPI(session, DeviceCategory.VEDGES)
    software_action_id = software_action.upgrade_software(devices_payload,
        InstallSpecHelper.CEDGE.value, reboot = False, sync = True, software_image=software_image)

    # Check action status
    wait_for_completed(session, software_action_id, 3000)
    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.session, device_category)

    def activate_software(
        self,
        devices: DataSequence[Device],
        device_type: DeviceType,
        version_to_activate: Optional[str] = "",
        software_image: Optional[str] = "",
    ) -> str:
        """
        Set chosen version as current version

        Args:
            devices (List[Device]): For those devices software will be activated
            version_to_activate (Optional[str]): version to be set as current version
            software_image (Optional[str]): path to software image

            Notice: Have to pass one of those arguments (version_to_activate,
            software_image)

        Returns:
            str: Activate software action id
        """
        if software_image and not version_to_activate:
            version = cast(str, self.repository.get_image_version(software_image))
        elif version_to_activate and not software_image:
            version = cast(str, version_to_activate)
        else:
            raise VersionDeclarationError("You can not provide software_image and image version at the same time!")
        url = "/dataservice/device/action/changepartition"
        payload = {
            "action": "changepartition",
            "devices": [
                asdict(device) for device in self.device_versions.get_device_available(version, devices)  # type: ignore
            ],
            "deviceType": device_type.value,
        }
        activate = dict(self.session.post(url, json=payload).json())
        return activate["id"]

    def upgrade_software(
        self,
        devices: DataSequence[Device],
        install_spec: InstallSpecification,
        reboot: bool,
        sync: bool = True,
        software_image: Optional[str] = "",
        image_version: Optional[str] = "",
    ) -> str:
        """
        Method to install new software

        Args:
            devices (List[Device]): For those devices software will be activated
            install_spec (InstallSpecification): specification of devices
            on which the action is to be performed
            reboot (bool): reboot device after action end
            sync (bool, optional): Synchronize settings. Defaults to True.
            software_image (Optional[str]): path to software image
            image_version (Optional[str]): version of software image

            Notice: Have to pass one of those arguments (version_to_activate,
            software_image)

        Raises:
            ValueError: Raise error if downgrade in certain cases

        Returns:
            str: action id
        """
        if software_image and not image_version:
            version = cast(str, self.repository.get_image_version(software_image))
        elif image_version and not software_image:
            version = cast(str, image_version)
        else:
            raise VersionDeclarationError("You can not provide software_image and image version at the same time")
        url = "/dataservice/device/action/install"
        payload: Dict[str, Any] = {
            "action": "install",
            "input": {
                "vEdgeVPN": 0,
                "vSmartVPN": 0,
                "family": install_spec.family.value,
                "version": version,
                "versionType": install_spec.version_type.value,
                "reboot": reboot,
                "sync": sync,
            },
            "devices": [
                {"deviceId": device.deviceId, "deviceIP": device.deviceIP}
                for device in self.device_versions.get_device_list(devices)
            ],  # type: ignore
            "deviceType": install_spec.device_type.value,
        }
        if install_spec.family.value in (DeviceClass.VMANAGE.value, DeviceClass.CEDGE.value):
            self._downgrade_check(payload["devices"], payload["input"]["version"], install_spec.family.value)
        upgrade = dict(self.session.post(url, json=payload).json())
        return upgrade["id"]

    def _downgrade_check(self, payload_devices: List[dict], version_to_upgrade: str, family: str) -> None:
        """
        Check if upgrade operation is not actually a downgrade opeartion.
        If so, in some cases action is being blocked.

        Args:
            version_to_upgrade (str): version to upgrade
            devices_category (DeviceCategory): devices category

        Returns:
            List[str]: list of devices with no permission to downgrade
        """
        incorrect_devices = []
        devices_versions_repo = self.repository.get_devices_versions_repository(self.device_versions.device_category)
        for device in payload_devices:
            dev_current_version = str(devices_versions_repo[device["deviceId"]].current_version)
            splited_version_to_upgrade = version_to_upgrade.split(".")
            for priority, label in enumerate(dev_current_version.split("-")[0].split(".")):
                try:
                    label = int(label)  # type: ignore
                    version = int(splited_version_to_upgrade[priority])
                except ValueError:
                    pass

                if label > version:  # type: ignore
                    if family == "vmanage" and label == 2:
                        continue
                    incorrect_devices.append(device["deviceId"])
                    break
                elif label < version:  # type: ignore
                    break
        if incorrect_devices:
            raise ValueError(
                f"Current version of devices with id's {incorrect_devices} is \
                higher than upgrade version. Action denied!"
            )
