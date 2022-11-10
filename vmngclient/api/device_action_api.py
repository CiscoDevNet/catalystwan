import logging
from abc import ABC, abstractmethod
from typing import cast,Union,List

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed

from vmngclient.api.basic_api import DevicesAPI, DeviceStateAPI
from vmngclient.dataclasses import DeviceInfo
from vmngclient.session import Session
from vmngclient.utils.certificate_status import CertificateStatus
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.reachability import Reachability
from vmngclient.utils.validate_status import ValidateStatus

logger = logging.getLogger(get_logger_name(__name__))


class ActionAPI(ABC):
    """API methods to execute action and verify its status """

    def __init__(self, session: Session, dev: DeviceInfo):
        self.session = session
        self.action_status = ''
        self.action_id = ''

    def __str__(self):
        return str(self.session)

    def wait_for_completed(self, 
        sleep_seconds: int,
        timeout_seconds: int,
        exit_statuses : Union[List(str),str],
        action_id : str,
        action_url: str = '/dataservice/device/action/status/',
         ) -> None:
        
        def check_status(action_data):
            return not action_data in exit_statuses

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_action_finish():
            url = f'{action_url}{action_id}'
            try:
                action_data = self.session.get_data(url)[0]['status']
                logger.debug(f"Status of action {action_id} is: {action_data}")
            except IndexError:
                action_data = ''

            return action_data

        wait_for_action_finish()

class RebootAction(ActionAPI):
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
        response = self.session.post_json('/dataservice/device/action/reboot', data=body)
        if response.get('id'):
            self.action_id = response['id']
        else:
            raise Exception(f'Problem with reboot of {self.dev.id} occurred')

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 1800,
        expected_status: str = 'Success',
        expected_reachability: str = Reachability.reachable.value,
    ):
        def check_status(action_data):
            return not action_data == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_come_up():
            status_api = f'{self.action_status_api}{self.action_id}'
            # from my observation it is necessary to wait minimum 1 second for data related with reboot
            try:
                action_data = self.session.get_data(f'{status_api}')[0]['status']
                logger.debug(f"Status of device {self.dev.hostname} reboot is: {action_data}")
            except IndexError:
                action_data = ''
            status = DeviceStateAPI(self.session).get_system_status(self.dev.id)
            # it is necessary to wait also for Success of reboot because device can be reachable even several
            # seconds after execute reboot
            if status.reachability.value == expected_reachability:
                return action_data
            else:
                return None

        wait_for_come_up()


class ValidateAction(ActionAPI):
    """
    API method to perform validate Device
    """

    def execute(self, valid: bool = True):
        """
        validate device
        """
        body = [
            {
                "chasisNumber": self.dev.uuid,
                "serialNumber": self.dev.board_serial,
                "validity": "valid" if valid else "invalid",
            }
        ]

        response = cast(dict, self.session.post_json('/dataservice/certificate/save/vedge/list', data=body))
        if response.get('id'):
            self.action_id = response['id']
        else:
            raise Exception(f'Problem with validate of {self.dev.id} occurred')

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 180,
        expected_status: str = ValidateStatus.validate.value,
        expected_reachability: str = Reachability.reachable.value,
    ):
        def check_status(action_data):
            return not action_data['validity'] == expected_status

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
        )
        def wait_for_come_up():
            status = DeviceStateAPI(self.session).get_system_status(self.dev.id)
            if status.reachability.value == expected_reachability:
                return self.session.get_data(f'/dataservice/device?host-name={self.dev.hostname}')[0]
            else:
                return None

        wait_for_come_up()

class DecommissionAction(ActionAPI):
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
            raise Exception(f'Problem with decomission of {self.dev.id} occurred')

    def wait_for_completed(
        self,
        sleep_seconds: int = 15,
        timeout_seconds: int = 20,
        expected_status: str = CertificateStatus.generated.value,
        expected_reachability=Reachability.unreachable.value,
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
