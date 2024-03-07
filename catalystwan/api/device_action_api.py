# Copyright 2022 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from catalystwan.api.basic_api import DevicesAPI, DeviceStateAPI
from catalystwan.dataclasses import Device
from catalystwan.session import vManageBadResponseError
from catalystwan.utils.certificate_status import CertificateStatus
from catalystwan.utils.operation_status import OperationStatus
from catalystwan.utils.personality import Personality
from catalystwan.utils.reachability import Reachability
from catalystwan.utils.validate_status import ValidateStatus

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class DeviceActionAPI(ABC):
    """API method to execute action on Device."""

    def __init__(self, session: ManagerSession, dev: Device):
        self.session = session
        self.dev = dev
        self.action_status = ""
        self.action_id = ""
        self.action_status_api = "/dataservice/device/action/status/"

    def __str__(self):
        return str(self.session)

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def wait_for_completed(
        self,
        sleep_seconds: int,
        timeout_seconds: int,
        expected_status: str,
        expected_reachability: str,
    ):
        raise NotImplementedError


class RebootAction(DeviceActionAPI):
    """API method to perform reboot on Device."""

    def execute(self):
        """Reboots the device.

        Returns:
            reboot process id

        Raises:
            Exception when reboot was not successful.

        Usage example:
        # Create session and chose device
        session = create_manager_session(...)
        device = DevicesAPI(session).get().filter(personality = Personality.VSMART)[0]
        # Restart device
        RebootAction(session, device).execute()
        """
        controllers = (Personality.VBOND, Personality.VSMART)
        device_type = "controller" if self.dev.personality in controllers else self.dev.personality.value

        body = {
            "action": "reboot",
            "deviceType": device_type,
            "devices": [{"deviceIP": self.dev.id, "deviceId": self.dev.uuid}],
        }
        response = self.session.post("/dataservice/device/action/reboot", json=body).json()
        if response.get("id"):
            self.action_id = response["id"]
        else:
            raise Exception(f"Problem with reboot of {self.dev.id} occurred")

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 1800,
        expected_status: str = OperationStatus.SUCCESS.value,
        expected_reachability: str = Reachability.REACHABLE.value,
    ):
        def check_status(action_data):
            return not action_data == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_come_up():
            status_api = f"{self.action_status_api}{self.action_id}"
            # from my observation it is necessary to wait minimum 1 second for data related with reboot
            try:
                action_data = self.session.get_data(f"{status_api}")[0]["status"]
                logger.debug(f"Status of device {self.dev.hostname} reboot is: {action_data}")
            except IndexError:
                action_data = ""
            status = DeviceStateAPI(self.session).get_system_status(self.dev.id)
            # it is necessary to wait also for Success of reboot because device can be reachable even several
            # seconds after execute reboot
            if status.reachability.value == expected_reachability:
                return action_data
            else:
                return None

        wait_for_come_up()


class PatchUpgradeAction(DeviceActionAPI):
    """API method to perform reboot on Device."""

    def execute(self, patch_version: str = "default"):
        """Patches vmanage

        Returns:
            patching process id

        Raises:
            Exception when patching times out.

        Usage example:
        # Create session and chose vmanage device
        session = create_manager_session(...)
        device = DevicesAPI(session).get().filter(personality = Personality.VMANAGE)[0]
        # Patch device. Requires passing the vmanage version vmanage will be patched to.
        PatchAction(session, device).execute(version)
        """
        if self.dev.personality != Personality.VMANAGE:
            raise Exception(f"Patch upgrade cannot be executed for {self.dev.personality}")

        body = {
            "action": "patchupgrade",
            "deviceType": "vmanage",
            "patchversion": patch_version,
            "devices": [{"deviceIP": self.dev.id, "deviceId": self.dev.uuid}],
        }

        response = self.session.post("/dataservice/device/action/patchupgrade", json=body).json()
        if response.get("id"):
            self.action_id = response["id"]
        else:
            raise Exception(f"Problem with patching {self.dev.id} occurred")

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 6000,
        expected_status: str = OperationStatus.SUCCESS.value,
        expected_reachability: str = Reachability.REACHABLE.value,
    ):
        def check_status(action_data):
            task_done_status = {
                OperationStatus.SUCCESS.value,
                OperationStatus.FAILURE.value,
                OperationStatus.VALIDATION_FAILURE.value,
            }
            return action_data not in task_done_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=(retry_if_result(check_status)),
        )
        def wait_for_come_up():
            status_api = f"{self.action_status_api}{self.action_id}"
            try:
                status = DeviceStateAPI(self.session).get_system_status(self.dev.id)
            except (ConnectionError, vManageBadResponseError):
                print(f"Waiting for {self.dev.hostname} to become reachable or task timeout...")
                logger.debug(f"Waiting for {self.dev.hostname} to become reachable or task timeout...")
                return None

            try:
                action_data = self.session.get_data(f"{status_api}")[0]["status"]
                print(f"Status of device {self.dev.hostname}  job is: {action_data}")
                logger.debug(f"Status of device {self.dev.hostname} patch job is: {action_data}")
            except IndexError:
                action_data = ""

            print(f"{self.dev.hostname} reachability: {status.reachability.value}")
            logger.debug(f"{self.dev.hostname} reachability: {status.reachability.value}")
            if status.reachability.value == expected_reachability:
                return action_data
            else:
                return None

        wait_for_come_up()


class ValidateAction(DeviceActionAPI):  # TODO check
    """
    API method to perform validate Device

    Usage example:
    # Create session and chose device
    session = create_manager_session(...)
    device = DevicesAPI(session).get().filter(personality = Personality.VSMART)[0]
    # Validate device
    ValidateAction(session, device).execute()
    """

    def execute(self, valid: bool = True):
        """
        validate device
        """
        body = {
            "chasisNumber": self.dev.uuid,
            "serialNumber": self.dev.board_serial,
            "validity": "valid" if valid else "invalid",
        }

        response = self.session.post(url="/dataservice/certificate/save/vedge/list", json=body).json()
        if response.get("id"):
            self.action_id = response["id"]
        else:
            raise Exception(f"Problem with validate of {self.dev.id} occurred")

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 180,
        expected_status: str = ValidateStatus.validate.value,
        expected_reachability: str = Reachability.REACHABLE.value,
    ):
        def check_status(action_data):
            return not action_data["validity"] == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_come_up():
            status = DeviceStateAPI(self.session).get_system_status(self.dev.id)
            if status.reachability.value == expected_reachability:
                return self.session.get_data(f"/dataservice/device?host-name={self.dev.hostname}")[0]
            else:
                return None

        wait_for_come_up()


class DecommissionAction(DeviceActionAPI):
    """
    API method to decommission Device

    Usage example:
    # Create session and chose device
    session = create_manager_session(...)
    device = DevicesAPI(session).get().filter(personality = Personality.VSMART)[0]
    # Decommission device
    DecommissionAction(session, device).execute()
    """

    def execute(self):
        """
        Decommission device.
        """
        url = f"/dataservice/system/device/decommission/{self.dev.uuid}"
        response = self.session.put(url)
        if response.status_code != 200:
            raise Exception(f"Problem with decomission of {self.dev.id} occurred")

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 20,
        expected_status: str = CertificateStatus.generated.value,
        expected_reachability=Reachability.UNREACHABLE.value,
    ):
        def check_status(action_data):
            return not action_data.vedgeCertificateState == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_status():
            status = DevicesAPI(self.session).get_device_details(self.dev.uuid)
            if status.reachability.value == expected_reachability:
                return status
            else:
                return None

        wait_for_status()
