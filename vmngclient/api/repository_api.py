import logging
import os
from enum import Enum
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

class ApiCallData:
    """
    API methods to prepare data for most of software actions
    """

    def __init__(
        self,
        session: Session,
        devices: List[Device],
        device_category: DeviceCategory,
    ):

        self.session = session
        self.devices = []
        self.device_category = device_category

        for dev in devices:
            dev_dict = dict()
            dev_dict["deviceId"] = dev.uuid
            dev_dict["deviceIP"] = dev.id
            self.devices.append(dev_dict)

class RepositoryAPI:
    """
    API methods to prepare data for most of software actions
    """

    def __init__(
        self,
        api_call_data: ApiCallData,
    ):
        self.api_call_data = api_call_data

    def get_image_version(self, software_image: str) -> Union[str, None]:
        """
        Method to get proper software image version

        Args:
            software_image (str): path to software image

        Returns:
            Union[str, None]: image version or None
        """
        url = "/dataservice/device/action/software/images?imageType=software"
        image_name = os.path.basename(software_image)
        software_images = self.api_call_data.session.get_data(url)
        for img in software_images:
            if image_name in img["availableFiles"]:
                image_version = img["versionName"]
                return image_version
        logger.error(f"Software image {image_name} is not in available images")
        return None

    def get_devices_versions_repository(self) -> Dict[str, DeviceSoftwareRepository]:
        """
        Method for create DeviceSoftwareRepository dataclass,
        which cointains information about all possible version types for certain devices

        Returns:
            Dict[str, DeviceSoftwareRepository]: Dictionary containing all versions
            information
        """

        url = f"/dataservice/system/device/{self.api_call_data.device_category}"
        devices_versions_info = self.api_call_data.session.get_data(url)
        self.devices_versions_repository = {}
        for device in devices_versions_info:
            device_all_versions = create_dataclass(DeviceSoftwareRepository, device)
            device_all_versions.installed_versions = [version for version in device_all_versions.available_versions]
            device_all_versions.installed_versions.append(device_all_versions.current_version)
            self.devices_versions_repository[device_all_versions.device_id] = device_all_versions
        return self.devices_versions_repository

    def complete_device_list(self, version_to_set_up, version_type: str) -> None:

        all_dev_versions = self.get_devices_versions_repository()
        for dev in self.api_call_data.devices:
            dev_versions = getattr(all_dev_versions[dev["deviceId"]], version_type)
            for version in dev_versions:
                if version_to_set_up in version:
                    dev["version"] = version
                    break
            if 'version' not in dev:
                raise ValueError(f"Software version {version_to_set_up} is not included in {version_type}")
        return None
