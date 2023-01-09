import logging
from typing import List, cast

from attr import define, field  # type: ignore
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(__name__)


@define
class TaskStatus:
    status: str
    status_id: str = field(metadata={FIELD_NAME: "statusId"})
    activity: List[str]


def wait_for_completed(
    session: vManageSession,
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
    activity_text: str = "",
) -> TaskStatus:
    """
    Method to check action status

    Example:
        session = create_vManageSession(ip_address,admin_username,password,port=port)
        devices = DevicesAPI(session).devices
        vsmart_device = [dev for dev in devices if dev.personality == Personality.VSMART][0]

        reboot_action = RebootAction(session,devices)
        reboot_action.execute()

        # Keep asking for reboot status until it's not in exit_statuses (Failure or Success)
          or timeout is not achieved (3000s)
        task = wait_for_completed(session,reboot_action.action_id,3000)
        if task.status == OperationStatus.SUCCESS.value:
            #do something
        else:
            #do something else

    Args:
        session (vManageSession): session
        action_id (str): inspected action id
        timeout_seconds (int): After this time, function will stop requesting action status
        sleep_seconds (int): interval between action status requests
        exit_statuses (Union[List[OperationStatus], str]): actions statuses that cause stop requesting action status
        exit_statuses_ids (Union[List[OperationStatusId], str]): actions statuses ids
            that cause stop requesting action status id
        activity_text (str): activity text

    Returns:
        task (TaskStatus):
    """
    action_url = "/dataservice/device/action/status/"
    exit_statuses = [cast(OperationStatus, exit_status.value) for exit_status in exit_statuses]
    exit_statuses_ids = [cast(OperationStatusId, exit_status_id.value) for exit_status_id in exit_statuses_ids]

    def check_status(task: TaskStatus) -> bool:
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

        if (task.status in exit_statuses) and (task.status_id in exit_statuses_ids):
            if not activity_text or activity_text in task.activity:
                return False
        return True

    def log_exception(self) -> None:
        logger.error("Operation status not achieved in given time")

    @retry(
        wait=wait_fixed(sleep_seconds),
        stop=stop_after_attempt(int(timeout_seconds / sleep_seconds)),
        retry=retry_if_result(check_status),
        retry_error_callback=log_exception,
    )
    def wait_for_action_finish() -> TaskStatus:
        """
        Keep asking for task status, status_id,
        activity(optional), utill check_status is True

        Returns:
            TaskStatus: TaskStatus instance
        """
        url = f"{action_url}{action_id}"
        action_data = session.get_data(url)[0]
        task = create_dataclass(TaskStatus, action_data)
        logger.debug(
            f"Statuses of action {action_id} is: "
            f"status: {task.status}, status_id: {task.status_id}, activity: {task.activity}."
        )
        return task

    return wait_for_action_finish()
