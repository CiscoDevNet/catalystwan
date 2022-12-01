import logging
from enum import Enum
from typing import Any, Dict, List, Union
from urllib.error import HTTPError

from attr import define
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from vmngclient.api.basic_api import Session
from vmngclient.api.versions_utils import DeviceCategory, DeviceVersions, RepositoryAPI
from vmngclient.dataclasses import Device
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.operation_status import OperationStatus

logger = logging.getLogger(get_logger_name(__name__))


class Family(Enum):
    VEDGE = "vedge"
    VMANAGE = "vmanage"


class VersionType(Enum):
    VMANAGE = "vmanage"


class DeviceType(Enum):
    CONTROLLER = "controller"
    VEDGE = "vedge"
    VMANAGE = "vmanage"


@define
class InstallSpecification:

    family: Family
    version_type: VersionType
    device_type: DeviceType


class InstallSpecHelper(Enum):
    VMANAGE = InstallSpecification(Family.VMANAGE, VersionType.VMANAGE, DeviceType.VMANAGE)
    VSMART = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER)
    VBOND = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.CONTROLLER)
    VEDGE = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.VEDGE)
    CEDGE = InstallSpecification(Family.VEDGE, VersionType.VMANAGE, DeviceType.VEDGE)


class SoftwareActionAPI:
    """
    API methods for software actions. All methods
    are exececutable on all device categories.
    """

    def __init__(self, session: Session, device_versions: DeviceVersions, repository: RepositoryAPI) -> None:

        self.session = session
        self.device_versions = device_versions
        self.repository = repository

    def activate_software(self, version_to_activate: str, devices: List[Device]) -> str:
        """
        Method to set choosen version as current version

        Args:
            version_to_activate (str): version to be set as current version

        Returns:
            str: action id
        """

        url = "/dataservice/device/action/changepartition"
        payload = {
            "action": "changepartition",
            "devices": self.device_versions.get_device_list_if_in_available(version_to_activate, devices),
            "deviceType": "vmanage",
        }
        activate = dict(self.session.post_json(url, payload))
        return activate["id"]

    def upgrade_software(
        self,
        devices: List[Device],
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

        url = "/dataservice/device/action/install"
        payload: Dict[str, Any] = {
            "action": "install",
            "input": {
                "vEdgeVPN": 0,
                "vSmartVPN": 0,
                "family": install_spec.value.family.value,  # type: ignore
                "version": self.repository.get_image_version(software_image),
                "versionType": install_spec.value.version_type.value,  # type: ignore
                "reboot": reboot,
                "sync": sync,
            },
            "devices": self.device_versions.get_device_list(devices),
            "deviceType": install_spec.value.device_type.value,  # type: ignore
        }

        if install_spec.value.family.value in (Family.VMANAGE.value, Family.VEDGE.value):  # type: ignore
            incorrect_devices = self._downgrade_check(
                payload["devices"],
                payload["input"]["version"],
                self.device_versions.device_category,
                install_spec.value.family.value,  # type: ignore
            )  # type: ignore
            if incorrect_devices:
                raise ValueError(
                    f"Current version of devices with id's {incorrect_devices} is \
                    higher than upgrade version. Action denied!"
                )
        upgrade = dict(self.session.post_json(url, payload))
        return upgrade["id"]

    def _downgrade_check(
        self, devices, version_to_upgrade: str, devices_category: DeviceCategory, family
    ) -> Union[None, List]:
        """
        Check if upgrade operation is not actually and downgrade opeartion.
        If so, in some cases action is being blocked.

        Args:
            version_to_upgrade (str): version to upgrade
            devices_category (DeviceCategory): devices category

        Returns:
            Union[None, List]: [None, list of devices with no permission to downgrade]
        """
        incorrect_devices = []
        devices_versions_repo = self.repository.get_devices_versions_repository(
            self.device_versions.device_category.value
        )
        for dev in devices:
            dev_current_version = str(devices_versions_repo[dev["deviceId"]].current_version)
            splited_version_to_upgrade = version_to_upgrade.split(".")
            for priority, label in enumerate(dev_current_version.split("-")[0].split(".")):
                if str(label) > str(splited_version_to_upgrade[priority]):
                    if family == "vmanage" and label == 2:
                        continue
                    incorrect_devices.append(dev["deviceId"])
                    break
                elif str(label) < str(splited_version_to_upgrade[priority]):
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

        def _log_exception(self):
            logger.error("Operation status not achieved in given time")
            return None

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
            retry_error_callback=_log_exception,
        )
        def wait_for_end_software_action():
            url = f"/dataservice/device/action/status/{action_id}"
            try:
                action_data = self.session.get_data(url)[0]["status"]
                logger.debug(f"Status of action {action_id} is: {action_data}")
                print(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ""
            except HTTPError as error:
                if error.code == 503:
                    pass

            return action_data

        return wait_for_end_software_action()
