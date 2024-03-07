# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from pathlib import PurePath
from typing import TYPE_CHECKING, Dict, List, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints.configuration.software_actions import SoftwareImageDetails
from catalystwan.endpoints.configuration_device_actions import PartitionDevice
from catalystwan.endpoints.configuration_device_inventory import DeviceDetailsResponse
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
        Get all info about all software images stored in Vmanage repository

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
        vmanages_versions_info = self.session.endpoints.configuration_device_actions.get_list_of_installed_devices(
            device_type="vmanage"
        )
        devices_versions_repository = {}
        for device in controllers_versions_info + edges_versions_info + vmanages_versions_info:
            device_software_repository = DeviceSoftwareRepository(**device.model_dump(by_alias=True))
            device_software_repository.installed_versions = [a for a in device_software_repository.available_versions]
            device_software_repository.installed_versions.append(device_software_repository.current_version)
            devices_versions_repository[device_software_repository.device_id] = device_software_repository
        return devices_versions_repository

    def get_image_version(self, software_image: str) -> Union[str, None]:
        """
        Get proper software image version, based on name in available files.

        If software_image detected in available files, but doesn't include version_name, software_image won't be used.

        Args:
            software_image (str): path to software image

        Returns:
            Union[str, None]: image version or None
        """

        image_name = PurePath(software_image).name
        software_images = self.get_all_software_images()
        for image in software_images:
            if image.available_files and image_name in image.available_files:
                if image.version_name and not image.version_name == "--":
                    return image.version_name
                logger.warning(
                    f"Detected image {image_name} in available files has version_name: {image.version_name} as value."
                    "Image will not be used and image version won't be returned."
                )
        logger.error(f"Software image {image_name} is not in available images")
        return None

    def get_remote_image(
        self, remote_image_filename: str, remote_server_name: str
    ) -> Union[SoftwareImageDetails, None]:
        """
        Get remote software image details, based on name in available files and remote server name.

        Args:
            remote_image_filename (str): path to software image on remote server
            remote_server_name (str): remote server name

        Returns:
            Union[SoftwareImageDetails, None]: remote image image details
        """

        image_name = PurePath(remote_image_filename).name
        software_images = self.get_all_software_images()
        for image_details in software_images:
            if (
                image_details.available_files
                and image_details.version_type
                and image_name in image_details.available_files
                and remote_server_name in image_details.version_type
            ):
                if not (image_details.remote_server_id and image_details.version_id):
                    raise ValueError(
                        f"Requested image: '{image_name}' does not include include required fields for this operation:"
                        f"image_details.remote_server_id - (current value: {image_details.remote_server_id})"
                        f"image_details.version_id - (current value: {image_details.version_id})"
                    )
                return image_details
        logger.error(
            f"Software image {image_name} is not in available in images from remote server {remote_server_name}"
        )
        return None

    def upload_image(self, image_path: str) -> None:
        """
        Upload software image ('tar.gz' or 'SPA.bin') to vManage software repository

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
            image_name (str): image name (in available files)

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
                return None
        raise ImageNotInRepositoryError(f"Image: {image_name} is not the vManage software repository")


class DeviceVersions:
    """
    Methods to prepare devices list for payload
    """

    def __init__(self, session: ManagerSession):
        self.repository = RepositoryAPI(session)

    def _validate_devices_required_fields(self, devices: DataSequence[DeviceDetailsResponse]):
        for device in devices:
            if not device.uuid or not device.device_ip:
                raise ValueError(
                    f"Provided device '{device.host_name}' doesn't include required fields for this operation:"
                    f"device.uuid (current value: {device.uuid})"
                    f"device.device_ip (current value: {device.device_ip})"
                )

    def _get_device_list_in(
        self, version_to_set_up: str, devices: DataSequence[DeviceDetailsResponse], version_type: str
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included requested version, if requested version
        is in specified version type

        Args:
            version_to_set_up (str): requested version
            devices List[DeviceDetailsResponse]: list of Device dataclass instances
            version_type: type of version (installed, available, etc.)

        Returns:
            list : list of devices
        """
        self._validate_devices_required_fields(devices)
        devices_payload = DataSequence(
            PartitionDevice,
            [PartitionDevice(device_id=device.uuid, device_ip=device.device_ip) for device in devices],  # type: ignore
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
        self, version_to_set_up: str, devices: DataSequence[DeviceDetailsResponse]
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included requested version, if requested version
        is in installed versions

        Args:
            version_to_set_up (str): requested version
            devices (List[DeviceDetailsResponse]): devices on which action going to be performed

        Returns:
            list : list of devices
        """
        return self._get_device_list_in(version_to_set_up, devices, "installed_versions")

    def get_device_available(
        self, version_to_set_up: str, devices: DataSequence[DeviceDetailsResponse]
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included requested, if requested version
        is in available versions

        Args:
            version_to_set_up (str): requested version
            devices (List[DeviceDetailsResponse]): devices on which action going to be performed


        Returns:
            list : list of devices
        """
        return self._get_device_list_in(version_to_set_up, devices, "available_versions")

    def _get_devices_chosen_version(
        self, devices: DataSequence[DeviceDetailsResponse], version_type: str
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included software version key
        for every device in devices list

        Args:
            version_to_set_up (str): requested version
            devices (List[DeviceDetailsResponse]): devices on which action going to be performed

        Returns:
            list : list of devices
        """
        self._validate_devices_required_fields(devices)

        devices_payload = DataSequence(
            PartitionDevice,
            [PartitionDevice(device_id=device.uuid, device_ip=device.device_ip) for device in devices],  # type: ignore
        )
        all_dev_versions = self.repository.get_devices_versions_repository()
        for device in devices_payload:
            device.version = getattr(all_dev_versions[device.device_id], version_type)
        return devices_payload

    def get_devices_current_version(
        self, devices: DataSequence[DeviceDetailsResponse]
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included current software version key
        for every device in devices list

        Args:
            version_to_set_up (str): requested version
            devices (List[DeviceDetailsResponse]): devices on which action going to be performed

        Returns:
            list : list of devices
        """

        return self._get_devices_chosen_version(devices, "current_version")

    def get_devices_available_versions(
        self, devices: DataSequence[DeviceDetailsResponse]
    ) -> DataSequence[PartitionDevice]:
        """
        Create devices payload list included available software versions key
        for every device in devices list

        Args:
            devices (List[DeviceDetailsResponse]): devices on which action going to be performed

        Returns:
            list : list of devices
        """

        return self._get_devices_chosen_version(devices, "available_versions")

    def get_device_list(self, devices: DataSequence[DeviceDetailsResponse]) -> List[PartitionDevice]:
        self._validate_devices_required_fields(devices)

        return [
            PartitionDevice(device_id=device.uuid, device_ip=device.device_ip) for device in devices  # type: ignore
        ]
