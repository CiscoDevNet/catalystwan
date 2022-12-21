import logging
from abc import ABC, abstractmethod

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.api.basic_api import DevicesAPI, DeviceStateAPI
from vmngclient.dataclasses import Device
from vmngclient.session import vManageSession
from vmngclient.utils.certificate_status import CertificateStatus
from vmngclient.utils.operation_status import OperationStatus
from vmngclient.utils.reachability import Reachability
from vmngclient.utils.validate_status import ValidateStatus

logger = logging.getLogger(__name__)


class DeviceActionAPI(ABC):
    """API method to execute action on Device."""

    def __init__(self, session: vManageSession, dev: Device):
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
        """
        body = {
            "action": "reboot",
            "deviceType": "controller",
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


class ValidateAction(DeviceActionAPI):  # TODO check
    """
    API method to perform validate Device
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
    """

    def execute(self):
        """
        validate device
        """
        url = f"/dataservice/system/device/decommission/{self.dev.uuid}"
        response = self.session.put(url)
        if response.status != 200:
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
