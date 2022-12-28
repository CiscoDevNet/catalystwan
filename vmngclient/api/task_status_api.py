import logging
from typing import List, cast

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(get_logger_name(__name__))


class TaskStatus:
    """
    API class to check task status
        Example usage:

        session = create_vManageSession(ip_address,admin_username,password,port=port)
        devices = DevicesAPI(session).devices
        vsmart_device = [dev for dev in devices if dev.personality == Personality.VSMART][0]
        exit_statuses = [OperationStatus.SUCCESS.value, OperationStatus.FAILURE.value]
        exit_statuses_ids = [OperationStatusId.SUCCESS.value, OperationStatusId.FAILURE.value]

        reboot_action = RebootAction(session,devices)
        reboot_action.execute()

        # Keep asking for reboot status until it's not in exit_statuses (Failure or Success)
        # or timeout is not achieved (3000s)
        TaskStatus(session).wait_for_completed(5,3000,exit_statuses,exit_statuses_ids,reboot_action.action_id)

    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session
        self.status: str = ''
        self.status_id: str = ''
        self.activity: List[str] = []

    def wait_for_completed(
        self,
        action_id: str,
        timeout_seconds: int = 300,
        sleep_seconds: int = 5,
        exit_statuses: List[OperationStatus] = [
            OperationStatus.SUCCESS,
            OperationStatus.FAILURE,
        ],
        exit_statuses_ids: List[OperationStatusId] = [
            OperationStatusId.SUCCESS,
            OperationStatusId.FAILURE,
        ],
        activity_text: str = '',
    ) -> "TaskStatus":
        """
        Method to check action status

        Args:
            sleep_seconds (int): interval between action status requests
            timeout_seconds (int): After this time, function will stop requesting action status
            exit_statuses (Union[List[OperationStatus], str]): actions statuses that cause stop requesting action status
            exit_statuses_ids (Union[List[OperationStatusId], str]): actions statuses ids
             that cause stop requesting action status id
            action_id (str): inspected action id
            activity_text (str): activity text
            action_url (str, optional): Action url. Defaults to '/dataservice/device/action/status/'

        Returns:
            bool: True if c
        """
        action_url = '/dataservice/device/action/status/'
        exit_statuses = [cast(OperationStatus, exit_status.value) for exit_status in exit_statuses]
        exit_statuses_ids = [cast(OperationStatusId, exit_status_id.value) for exit_status_id in exit_statuses_ids]

        def check_status(action_data) -> bool:
            """
            Function checks if condition is met. If so,
            wait_for_completed stops asking for task status

            Args:
                status (str): status of task
                status_id (str): status id of task
                activity (str): activity text

            Returns:
                bool: False if condition is met
            """

            if (self.status in exit_statuses) and (self.status_id in exit_statuses_ids):
                if not activity_text or activity_text in self.activity:
                    return False
            return True

        def _log_exception(self) -> None:
            logger.error("Operation status not achieved in given time")

        @retry(
            wait=wait_fixed(sleep_seconds),
            stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
            retry=retry_if_result(check_status),
            retry_error_callback=_log_exception,
        )
        def wait_for_action_finish() -> bool:
            """
            Keep asking for task status, status_id,
            activity(optional), utill check_status is True

            Returns:
                TaskStatus: TaskStatus instance
            """
            url = f'{action_url}{action_id}'
            action_data = self.session.get_data(url)[0]
            self.status = action_data['status']
            self.status_id = action_data['statusId']
            self.activity = action_data['activity']
            logger.debug(
                f"Statuses of action {action_id} is: "
                f"status: {self.status}, status_id: {self.status_id}, activity: {self.activity} "
            )
            return action_data

        wait_for_action_finish()
        return self
