import logging
from enum import Enum
from typing import Any, Dict, List, Union

from attr import define
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from vmngclient.api.repository_api import DeviceCategory, RepositoryAPI
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.operation_status import OperationStatus

logger = logging.getLogger(get_logger_name(__name__))


class Family(Enum):
    CEDGE = "vedge"
    VBOND = "vedge"
    VEDGE = "vedge"
    VSMART = "vedge"
    VMANAGE = "vmanage"


class VersionType(Enum):
    VSMART = "vmanage"
    VBOND = "vmanage"
    VEDGE = "vmanage"
    CEDGE = "vmanage"
    VMANAGE = "vmanage"


class DeviceType(Enum):
    VSMART = "controller"
    VBOND = "controller"
    VEDGE = "vedge"
    CEDGE = "vedge"
    VMANAGE = "vmanage"


@define
class InstallSpecification:

    family: Family
    version_type: VersionType
    device_type: DeviceType


class SoftwareActionAPI:
    """
    API methods for software actions. All methods
    are exececutable on all device categories.
    """

    def __init__(self, repository: RepositoryAPI) -> None:

        self.repository = repository

    def activate_software(self, version_to_activate: str) -> str:
        """
        Method to set choosen version as current version

        Args:
            version_to_activate (str): version to be set as current version

        Returns:
            str: action id
        """
        self.repository.complete_device_list(version_to_activate, "available_versions")
        url = "/dataservice/device/action/changepartition"
        payload = {
            "action": "changepartition",
            "devices": self.repository.devices,
            "deviceType": "vmanage",
        }
        activate = dict(self.repository.session.post_json(url, payload))
        return activate["id"]

    def upgrade_software(
        self,
        software_image: str,
        install_spec: InstallSpecification,
        reboot: bool,
        sync: bool = True,
    ) -> str:
        """
        Method to install new software

        Args:
            software_image (str): path to software image
            install_spec (InstallSpecification): specification of devices
            on which the action is to be performed
            reboot (bool): reboot device after action end
            sync (bool, optional): Synchronize settings. Defaults to True.

        Raises:
            ValueError: Raise error if downgrade in certain cases

        Returns:
            str: action id
        """
        self.install_spec = install_spec

        url = "/dataservice/device/action/install"
        payload: Dict[str, Any] = {
            "action": "install",
            "input": {
                "vEdgeVPN": 0,
                "vSmartVPN": 0,
                "family": self.install_spec.family,
                "version": self.repository.get_image_version(software_image),
                "versionType": self.install_spec.version_type,
                "reboot": reboot,
                "sync": sync,
            },
            "devices": self.repository.devices,
            "deviceType": self.install_spec.device_type,
        }

        if self.install_spec.family in (Family.VMANAGE.value, Family.CEDGE.value):
            incorrect_devices = self._downgrade_check(payload["input"]["version"], self.repository.device_category)
            if incorrect_devices:
                raise ValueError(
                    f"Current version of devices {incorrect_devices} is higher than upgrade version. Action denied!"
                )

        upgrade = dict(self.repository.session.post_json(url, payload))
        return upgrade["id"]

    def _downgrade_check(self, version_to_upgrade: str, devices_category: DeviceCategory) -> Union[None, List]:

        incorrect_devices = []
        for dev in self.repository.devices:
            dev_current_version = str(
                self.repository.create_devices_versions_repository()[dev["deviceId"]].current_version
            )
            splited_version_to_upgrade = version_to_upgrade.split(".")
            for priority, label in enumerate(dev_current_version.split(".")):
                if str(label) > str(splited_version_to_upgrade[priority]):
                    if devices_category == "vmanages" and label == 2:
                        continue
                    incorrect_devices.append(dev["deviceId"])
                    break
        if incorrect_devices == []:
            return None
        else:
            return incorrect_devices

    def wait_for_completed(
        self,
        sleep_seconds: int,
        timeout_seconds: int,
        exit_statuses: List[OperationStatus],
        action_id: str,
    ) -> str:
        """_summary_

        Args:
            sleep_seconds (int): _description_
            timeout_seconds (int): _description_
            exit_statuses (List[str]): _description_
            action_id (str): _description_
        """

        def check_status(action_data):
            return action_data not in (exit_statuses)

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_end_software_action():
            url = f"/dataservice/device/action/status/{action_id}"
            try:
                action_data = self.repository.session.get_data(url)[0]["status"]
                # logger.debug(f"Status of action {action_id} is: {action_data}")
                print(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ""

            return action_data

        return wait_for_end_software_action()
