from __future__ import annotations

import logging
from pathlib import PurePath
from typing import TYPE_CHECKING, Dict, List, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.dataclasses import Device
from catalystwan.endpoints.configuration.software_actions import SoftwareImageDetails
from catalystwan.endpoints.configuration_device_actions import PartitionDevice
from catalystwan.exceptions import ImageNotInRepositoryError
from catalystwan.typed_list import DataSequence
from catalystwan.utils.upgrades_helper import SoftwarePackageUploadPayload

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class DeviceSoftwareRepository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    installed_versions: List[str] = Field(default_factory=list)
    available_versions: List[str] = Field(
        default_factory=list, serialization_alias="availableVersions", validation_alias="availableVersions"
    )
    current_version: str = Field(
        default="",
        serialization_alias="version",
        validation_alias="version",
        description="Current active version of software on device",
    )
    default_version: str = Field(default="", serialization_alias="defaultVersion", validation_alias="defaultVersion")
    device_id: str = Field(default="", serialization_alias="uuid", validation_alias="uuid")


class RepositoryAPI:
    """
    API methods to get information about images and devices software versions

    Usage example:
        # Create session
        session = create_manager_session(...)

        # Upload image
        software_image = <path_to_your_image>
        RepositoryAPI(provider).upload_image(software_image)
    """

    def __init__(
        self,
        session: ManagerSession,
    ):
        self.session = session

    def get_all_software_images(self) -> DataSequence[SoftwareImageDetails]:
        """
        Get all info about all software images stored
        in Vmanage repository

        Returns:
            list: software images list
        """
        software_images = self.session.endpoints.configuration_software_actions.get_list_of_all_images()
        return software_images

    def get_devices_versions_repository(self) -> Dict[str, DeviceSoftwareRepository]:
        """
        Create DeviceSoftwareRepository dataclass,
        which cointains information about all possible version types for certain devices

        Returns:
            Dict[str, DeviceSoftwareRepository]: Dictionary containing all versions
            information
        """

        controllers_versions_info = self.session.endpoints.configuration_device_actions.get_list_of_installed_devices(
            device_type="controller"
        )
        edges_versions_info = self.session.endpoints.configuration_device_actions.get_list_of_installed_devices(
            device_type="vedge"
        )
        devices_versions_repository = {}
        for device in controllers_versions_info + edges_versions_info:
            device_software_repository = DeviceSoftwareRepository(**device)
            device_software_repository.installed_versions = [a for a in device_software_repository.available_versions]
            device_software_repository.installed_versions.append(device_software_repository.current_version)
            devices_versions_repository[device_software_repository.device_id] = device_software_repository
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
        for image in software_images:
            if image.available_files and image_name in image.available_files:
                image_version = image.version_name
                return image_version
        logger.error(f"Software image {image_name} is not in available images")
        return None

    def upload_image(self, image_path: str) -> None:
        """
        Upload software image 'tar.gz' to Vmanage
        software repository

        Args:
            image_path (str): path to software image

        Returns:
            str: Response status code
        """
        self.session.endpoints.configuration_device_software_update.upload_software_to_manager(
            payload=SoftwarePackageUploadPayload(image_path=image_path)
        )

    def delete_image(self, image_name: str) -> None:
        """
        Delete image from vManage software repository

        Args:
            image_name (str): image name

        Raises:
            ImageNotInRepositoryError: raise error if image not in repository

        Returns:
            int: Reponse status code
        """
        for image in self.get_all_software_images():
            if image.available_files and image_name in image.available_files:
                version_id = image.version_id
                self.session.endpoints.configuration_software_actions.delete_software_from_software_repository(
                    version_id=version_id
                )
                # return delete.status_code
        raise ImageNotInRepositoryError(f"Image: {image_name} is not the vManage software repository")


class DeviceVersions:
    """
    Methods to prepare devices list for payload
    """

    def __init__(self, session: ManagerSession):
        self.repository = RepositoryAPI(session)

    def _get_device_list_in(
        self, version_to_set_up: str, devices: DataSequence[Device], version_type: str
    ) -> DataSequence[PartitionDevice]:
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
        devices_payload = DataSequence(
            PartitionDevice,
            [PartitionDevice(device_id=device.uuid, device_ip=device.id) for device in devices],
        )
        all_dev_versions = self.repository.get_devices_versions_repository()
        for device in devices_payload:
            device_versions = getattr(all_dev_versions[device.device_id], version_type)
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

    def get_device_list_in_installed(
        self, version_to_set_up: str, devices: DataSequence[Device]
    ) -> DataSequence[PartitionDevice]:
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

    def get_device_available(
        self, version_to_set_up: str, devices: DataSequence[Device]
    ) -> DataSequence[PartitionDevice]:
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

    def _get_devices_chosen_version(
        self, devices: DataSequence[Device], version_type: str
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included software version key
        for every device in devices list

        Args:
            version_to_set_up (str): requested version
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """
        devices_payload = DataSequence(
            PartitionDevice,
            [PartitionDevice(device_id=device.uuid, device_ip=device.id) for device in devices],
        )
        all_dev_versions = self.repository.get_devices_versions_repository()
        for device in devices_payload:
            device.version = getattr(all_dev_versions[device.device_id], version_type)
        return devices_payload

    def get_devices_current_version(self, devices: DataSequence[Device]) -> DataSequence[PartitionDevice]:
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

    def get_devices_available_versions(self, devices: DataSequence[Device]) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included available software versions key
        for every device in devices list

        Args:
            devices (List[Device]): devices on which action going to be performed

        Returns:
            list : list of devices
        """

        return self._get_devices_chosen_version(devices, "available_versions")

    def get_device_list(self, devices: DataSequence[Device]) -> List[PartitionDevice]:
        return [PartitionDevice(device_id=device.uuid, device_ip=device.id) for device in devices]  # type: ignore
