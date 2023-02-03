import logging
from typing import Dict, List

from vmngclient.api.versions_utils import DeviceCategory, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class PartitionManagerAPI:
    """
    API methods for partitions actions. All methods
    are exececutable on all device categories.

    Usage example:
        #Create session
        ip_address = ""
        port = 10100
        admin_username = 'admin_username'
        tenant_username = 'tenant_username'
        password = "password"
        subdomain = "subdomain"
        provider_session = create_vManageSession(ip_address,admin_username,password,port)
        provider_session_as_tenant_session = create_vManageSession(ip_address,admin_username,password,port, subdomain)

        #Prepare devices list
        cedges = [dev for dev in DevicesAPI(provider_session_as_tenant_session).devices
                    if dev.hostname in ["vm5", "vm6"]]

        #Set default partition
        partition_manager = PartitionManagerAPI(provider_session_as_tenant_session,DeviceCategory.VEDGES.value)
        set_partition_id = partition_manager.set_default_partition(cedges, version="9.17.06.03a.0.56")

        #Check action status
        wait_for_completed(provider_session,set_partition_id,3000)

    """

    def __init__(self, session: vManageSession, device_category: DeviceCategory) -> None:

        self.session = session
        self.repository = RepositoryAPI(self.session)
        self.device_versions = DeviceVersions(self.repository, device_category)

    def _set_default_partition(self, payload_devices: List[dict]) -> str:
        url = "/dataservice/device/action/defaultpartition"
        payload = {
            "action": "defaultpartition",
            "devices": payload_devices,
            "deviceType": "vmanage",
        }
        set_default = dict(self.repository.session.post(url, json=payload).json())
        return set_default["id"]

    def set_current_partition_as_default(self, devices: List[Device]) -> str:
        """
        Method to set current software version as default version

        Args:
            devices (List[Device]): For those devices default partition
            going to be set

        Returns:
            str: action id
        """
        devs = self.device_versions.get_devices_current_version(devices)
        return self._set_default_partition(devs)

    def set_default_partition_by_version(self, devices: List[Device], version) -> str:
        """
        Method to set choosen software version as current version

        Args:
            devices (List[Device]): For those devices default partition
            going to be set
            version (_type_): version to be set as default version

        Returns:
            str: action id
        """
        devs = self.device_versions.get_device_list_in_installed(version, devices)
        return self._set_default_partition(devs)

    def remove_partition(self, devices: List[Device], version: str, force: bool = False) -> str:
        """
        Method to remove choosen software version from Vmanage repository

        Args:
            version (str): software version to be removed from repository

        Returns:
            str: action id
        """

        url = "/dataservice/device/action/removepartition"
        payload = {
            "action": "removepartition",
            "devices": self.device_versions.get_device_list_in_available(version, devices),
            "deviceType": "vmanage",
        }
        if force is False:
            invalid_devices = self._check_remove_partition_possibility(payload["devices"])
            if invalid_devices:
                raise ValueError(
                    f"Current or default version of devices with ids {invalid_devices} \
                        are equal to remove version. Action denied!"
                )
        remove_action: Dict[str, str] = self.repository.session.post(url, json=payload).json()
        return remove_action["id"]

    def _check_remove_partition_possibility(self, devices) -> List:

        devices_versions_repository = self.repository.get_devices_versions_repository(
            self.device_versions.device_category.value
        )
        invalid_devices = []
        for device in devices:

            if device["version"] in (
                devices_versions_repository[device["deviceId"]].current_version,
                devices_versions_repository[device["deviceId"]].default_version,
            ):
                invalid_devices.append((device["deviceId"]))
        return invalid_devices
