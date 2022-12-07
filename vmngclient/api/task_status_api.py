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
            status = str(action_data['status'])
            status_id = str(action_data['statusId'])
            activity = str(action_data['activity'])

            if (status in exit_statuses) and (status_id in exit_statuses_ids):
                if activity_text:
                    if activity_text in activity:
                        return False
                    else:
                        return True
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
            status = str(action_data['status'])
            status_id = str(action_data['statusId'])
            activity = str(action_data['activity'])
            logger.debug(
                f"Statuses of action {action_id} is: "
                f"status: {status}, status_id: {status_id}, activity: {activity} "
            )
            print(
                f"Statuses of action {action_id} is: " 
                f"status: {status}, status_id: {status_id}, activity: {activity} "
            )
            return action_data
        
        wait_for_action = wait_for_action_finish() 
        
        if wait_for_action['status'] == OperationStatus.SUCCESS.value \
        and wait_for_action['statusId'] == OperationStatusId.SUCCESS.value:
            if activity_text:
                if activity_text in wait_for_action['activity']:
                    return True
                else:
                    return False
            return True
        else:
            return False

                

