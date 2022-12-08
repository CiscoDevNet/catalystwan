import logging
from typing import List, Union

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(get_logger_name(__name__))


class TaskStatus:
    """API class to check task status"""

    def __init__(self, session: vManageSession):
        self.session = session
        self.status: str = ''
        self.status_id: str = ''
        self.activity: List[str] = []

    def wait_for_completed(
        self,
        sleep_seconds: int,
        timeout_seconds: int,
        exit_statuses: Union[List[OperationStatus], str],
        exit_statuses_ids: Union[List[OperationStatusId], str],
        action_id: str,
        activity_text: Union[str, None] = None,
        action_url: str = '/dataservice/device/action/status/',
    ) -> bool:
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
            return None

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
                bool: True if condition is met
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

        if self.status == OperationStatus.SUCCESS.value and self.status_id == OperationStatusId.SUCCESS.value:
            if not activity_text or activity_text in self.activity:
                return True
        return False
