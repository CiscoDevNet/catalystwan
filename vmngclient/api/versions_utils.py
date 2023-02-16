import logging
from enum import Enum
from pathlib import PurePath
from typing import Dict, List, Optional, Union

from attr import define, field  # type: ignore

from vmngclient.dataclasses import DataclassBase, Device
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass

logger = logging.getLogger(__name__)


class DeviceCategory(Enum):
    CONTROLLERS = "controllers"
    VEDGES = "vedges"


@define
class DeviceSoftwareRepository(DataclassBase):
    installed_versions: List[str] = field(default=None)
    available_versions: List[str] = field(default=None, metadata={FIELD_NAME: "availableVersions"})
    current_version: str = field(default=None, metadata={FIELD_NAME: "version"})
    default_version: str = field(default=None, metadata={FIELD_NAME: "defaultVersion"})
    device_id: str = field(default=None, metadata={FIELD_NAME: "uuid"})


@define(frozen=False)
class DeviceVersionPayload(DataclassBase):
    deviceId: str
    deviceIP: str
    version: Optional[str] = ""


@define(frozen=False)
class PayloadRemovePartition(DataclassBase):
    deviceId: str
    deviceIP: str
    version: Optional[List[str]] = [""]


class RepositoryAPI:
    """
    API methods to get information about images and devices versions
    """

    def __init__(
        self,
        session: vManageSession,
    ):
        self.session = session

    def get_all_software_images(self) -> list:
        """
        Get all info about all software images stored
        in Vmanage repository

        Returns:
            list: software images list
        """
        url = "/dataservice/device/action/software/images?imageType=software"
        software_images = list(self.session.get_data(url))
        return software_images

    def get_devices_versions_repository(self, device_category: DeviceCategory) -> Dict[str, DeviceSoftwareRepository]:
        """
        Create DeviceSoftwareRepository dataclass,
        which cointains information about all possible version types for certain devices

        Returns:
            Dict[str, DeviceSoftwareRepository]: Dictionary containing all versions
            information
        """

        url = f"/dataservice/system/device/{device_category.value}"
        devices_versions_info = self.session.get_data(url)
        devices_versions_repository = {}
        for device in devices_versions_info:
            device_all_versions = create_dataclass(DeviceSoftwareRepository, device)
            device_all_versions.installed_versions = [version for version in device_all_versions.available_versions]
            device_all_versions.installed_versions.append(device_all_versions.current_version)
            devices_versions_repository[device_all_versions.device_id] = device_all_versions
        return devices_versions_repository

    def get_image_version(self, software_image: str) -> Union[str, None]:
        """
        Get proper software image version

        Args:
            software_image (str): path to software image

        Returns:
            Union[str, None]: image version or None
        """

        image_name = PurePath(software_image).name
        software_images = self.get_all_software_images()
        for img in software_images:
            if image_name in img["availableFiles"]:
                image_version = img["versionName"]
                return image_version
        logger.error(f"Software image {image_name} is not in available images")
        return None


class DeviceVersions:
    """
    Methods to prepare devices list for payload
    """

    def __init__(self, repository: RepositoryAPI, device_category: DeviceCategory):
        self.repository = repository
        self.device_category = device_category

    def _get_device_list_in(
        self, version_to_set_up: str, devices: List[Device], version_type: str
    ) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included requested version, if requested version
        is in specified version type

        Args:
            version_to_set_up (str): requested version
            devices List[Device]: list of Device dataclass instances
            version_type: type of version (installed, available, etc.)

        Returns:
            list : list of devices
        """
        devices_payload = [DeviceVersionPayload(device.uuid, device.id) for device in devices]
        all_dev_versions = self.repository.get_devices_versions_repository(self.device_category)
        for device in devices_payload:
            device_versions = getattr(all_dev_versions[device.deviceId], version_type)
            try:
                for version in device_versions:
                    if version_to_set_up in version:
                        device.version = version
                        break
            except IndexError:
                logger.error(
                    f"Software version {version_to_set_up} for {device} is not included in {version_type}."
                    "Action for that device is not going to proceed."
                )
        return devices_payload

    def get_device_list_in_installed(self, version_to_set_up: str, devices: List[Device]) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included requested version, if requested version
        is in installed versions

        Args:
            version_to_set_up (str): requested version
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """
        return self._get_device_list_in(version_to_set_up, devices, "installed_versions")

    def get_device_list_in_available(self, version_to_set_up: str, devices: List[Device]) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included requested, if requested version
        is in available versions

        Args:
            version_to_set_up (str): requested version
            devices (List[Device]): devices on which action going to be performed


        Returns:
            list : list of devices
        """
        return self._get_device_list_in(version_to_set_up, devices, "available_versions")

    def _get_devices_chosen_version(self, devices: List[Device], version_type: str) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included software version key
        for every device in devices list

        Args:
            version_to_set_up (str): requested version
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """
        devices_payload = [DeviceVersionPayload(device.uuid, device.id) for device in devices]
        all_dev_versions = self.repository.get_devices_versions_repository(self.device_category)
        for device in devices_payload:
            device.version = getattr(all_dev_versions[device.deviceId], version_type)
        return devices_payload

    def get_devices_current_version(self, devices: List[Device]) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included current software version key
        for every device in devices list

        Args:
            version_to_set_up (str): requested version
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """

        return self._get_devices_chosen_version(devices, "current_version")

    def get_devices_available_versions(self, devices: List[Device]) -> List[DeviceVersionPayload]:
        """
        Create devices payload list included available software versions key
        for every device in devices list

        Args:
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """

        return self._get_devices_chosen_version(devices, "available_versions")

    def get_device_list(self, devices: List[Device]) -> List[DeviceVersionPayload]:

        return [DeviceVersionPayload(device.uuid, device.id) for device in devices]
