import logging
from typing import Union,List
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import get_logger_name
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId


logger = logging.getLogger(get_logger_name(__name__))

class TaskStatus():
    """API class to check task status"""

    def __init__(self, session: vManageSession):
        self.session = session

    def wait_for_completed(self, 
        sleep_seconds: int,
        timeout_seconds: int,
        exit_statuses : Union[List(OperationStatus),str],
        exit_statuses_ids : Union[List(OperationStatusId),str],
        action_id : str,
        activity_text : str = None,
        action_url: str = '/dataservice/device/action/status/',
        
         ) -> bool:
        
        def check_status(status: str, status_id: str, activity: str) -> bool:
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
            if (status in exit_statuses) and (status_id in exit_statuses_ids):
                if activity_text:
                    if activity_text == activity:
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
            activity(optional), till check_status is True

            Returns:
                bool: True if condition is met
            """
            url = f'{action_url}{action_id}'
            action_data = self.session.get_data(url)[0]
            status = action_data['status']
            status_id = action_data['statusId']
            activity = action_data['activity']
            logger.debug(f"Statuses of action {action_id} is: \
                    status: {status}, status_id: {status_id}, activity: {activity} ")

            if status in exit_statuses and status_id in exit_statuses_ids:
                if activity_text:
                    if activity_text == activity:
                        return True
                    else:
                        return False
                return True
            return False

        return wait_for_action_finish()