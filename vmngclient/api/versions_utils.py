import logging
from enum import Enum
from pathlib import PurePath
from typing import Dict, List, Union

from attr import define, field

from vmngclient.dataclasses import Device
from vmngclient.session import Session
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass, get_logger_name

logger = logging.getLogger(get_logger_name(__name__))


class DeviceCategory(Enum):
    VSMART = "controllers"
    VBOND = "controllers"
    VEDGE = "vedges"
    CEDGE = "vedges"
    VMANAGE = "controllers"


@define
class DeviceSoftwareRepository:
    installed_versions: List[str] = field(default=None)
    available_versions: List[str] = field(default=None, metadata={FIELD_NAME: "availableVersions"})
    current_version: str = field(default=None, metadata={FIELD_NAME: "version"})
    default_version: str = field(default=None, metadata={FIELD_NAME: "defaultVersion"})
    device_id: str = field(default=None, metadata={FIELD_NAME: "uuid"})


class RepositoryAPI:
    """
    API methods to prepare data for most of software actions
    """

    def __init__(
        self,
        session: Session,
    ):
        self.session = session

    def get_all_software_images(self) -> list:
        """
        Method to get all info about all software images stored
        in Vmanage repository

        Returns:
            list: software images list
        """
        url = "/dataservice/device/action/software/images?imageType=software"
        software_images = list(self.session.get_data(url))
        return software_images

    def get_devices_versions_repository(self, device_category) -> Dict[str, DeviceSoftwareRepository]:
        """
        Method for create DeviceSoftwareRepository dataclass,
        which cointains information about all possible version types for certain devices

        Returns:
            Dict[str, DeviceSoftwareRepository]: Dictionary containing all versions
            information
        """

        url = f"/dataservice/system/device/{device_category}"
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
        Method to get proper software image version

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
    """_summary_
    """
    def __init__(self, devices: List[Device], repository: RepositoryAPI, device_category: DeviceCategory):
        self.devices = [{"deviceId": dev.uuid, "deviceIP": dev.id} for dev in devices]
        self.repository = repository
        self.device_category = device_category

    def complete_device_list_if_in_available(self, version_to_set_up: str) -> None:
        """
        Create version key fir every device dict in device list, if requested version
        is in available versions

        Args:
            version_to_set_up (str): requested version

        Returns:
            None
        """

        all_dev_versions = self.repository.get_devices_versions_repository(self.device_category)
        for dev in self.devices:
            dev_available_versions = all_dev_versions[dev["deviceId"]].available_versions
            for version in dev_available_versions:
                if version_to_set_up in version:
                    dev["version"] = version
                    break
            if 'version' not in dev:
                logger.error(f"Software version {version_to_set_up} for {dev} is not included in available_versions")
        return 

    def complete_device_list_if_in_installed(self, version_to_set_up: str) -> None:
        """
        Create version key fir every device dict in device list, if requested version
        is in available versions

        Args:
            version_to_set_up (str): requested version

        Returns:
            None
        """

        all_dev_versions = self.repository.get_devices_versions_repository(self.device_category)
        for dev in self.devices:
            dev_installed_versions = all_dev_versions[dev["deviceId"]].installed_versions
            for version in dev_installed_versions:
                if version_to_set_up in version:
                    dev["version"] = version
                    break
            if 'version' not in dev:
                logger.error(f"Software version {version_to_set_up} for {dev} is not included in available_versions")
        return None
