from __future__ import annotations

import logging
from time import sleep
from typing import TYPE_CHECKING, List, cast

from attr import define, field  # type: ignore
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from vmngclient.dataclasses import DataclassBase  # type: ignore

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.exceptions import EmptyTaskResponseError, TaskNotRegisteredError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(__name__)


@define
class TaskStatus:
    status: str
    status_id: str = field(metadata={FIELD_NAME: "statusId"})
    activity: List[str]

@define
class TaskData(DataclassBase):
    status: str
    status_id: str = field(metadata={FIELD_NAME: "statusId"})
    action: str
    activity: List[str]
    current_activity: str = field(metadata={FIELD_NAME: "currentActivity"})
    action_config: str = field(metadata={FIELD_NAME: "actionConfig"})
    order: int
    uuid: str
    site_id: str = field(metadata={FIELD_NAME: "site-id"})


def get_all_tasks(session: vManageSession) -> List[str]:
    """
    Get list of active tasks id's in vmanage

    Args:
        session (vManageSession): session

    Returns:
       List[str]: active tasks id's
    """
    url = "dataservice/device/action/status/tasks"
    tasks = session.get_json(url)
    return [process["processId"] for process in tasks["runningTasks"]]


def wait_for_completed(
    session: vManageSession,
    task_id: str,
    timeout_seconds: int = 300,
    interval_seconds: int = 5,
    delay_seconds: int = 10,
    success_statuses: List[OperationStatus] = [
        OperationStatus.SUCCESS,
    ],
    failure_statuses: List[OperationStatus] = [
        OperationStatus.FAILURE,
    ],
    success_statuses_ids: List[OperationStatusId] = [
        OperationStatusId.SUCCESS,
    ],
    failure_statuses_ids: List[OperationStatusId] = [
        OperationStatusId.FAILURE,
    ],
    activity_text: str = "",
) -> DataSequence[TaskStatus]:
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
        task = wait_for_completed(session,reboot_action.task_id,3000)
        if task.status == OperationStatus.SUCCESS.value:
            #do something
        else:
            #do something else

    Args:
        session (vManageSession): session
        task_id (str): inspected action id
        timeout_seconds (int): After this time, function will stop requesting action status
        interval_seconds (int): interval between action status requests
        delay_seconds (int): if Vmanage didn't report task status, after this time api call would be repeated
        exit_statuses (Union[List[OperationStatus], str]): actions statuses that cause stop requesting action status
        exit_statuses_ids (Union[List[OperationStatusId], str]): actions statuses ids
            that cause stop requesting action status id
        activity_text (str): activity text

    Returns:
        task (TaskStatus):
    """
    success_statuses = [cast(OperationStatus, exit_status.value) for exit_status in success_statuses]
    failure_statuses = [cast(OperationStatus, exit_status.value) for exit_status in failure_statuses]
    success_statuses_ids = [cast(OperationStatusId, exit_status_id.value) for exit_status_id in success_statuses_ids]
    failure_statuses_ids = [cast(OperationStatusId, exit_status_id.value) for exit_status_id in failure_statuses_ids]

    def check_status(task_data: DataSequence[TaskData]) -> bool:
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

        task_statuses_success = [task.status in success_statuses for task in task_data]
        task_statuses_failure = [task.status in failure_statuses for task in task_data]
        task_statuses_id_success = [task.status_id in success_statuses_ids for task in task_data]
        task_statuses_id_failure = [task.status_id in failure_statuses_ids for task in task_data]
        task_activities = [activity_text in task.activity for task in task_data]

        if all(task_statuses_success + task_statuses_id_success) and not any(
            task_statuses_failure + task_statuses_id_failure
        ):
            if not activity_text or all(task_activities):
                return False
        return True

    def log_exception(self) -> None:
        logger.error("Operation status not achieved in given time")

    @retry(
        wait=wait_fixed(interval_seconds),
        stop=stop_after_attempt(int(timeout_seconds / interval_seconds)),
        retry=retry_if_result(check_status),
        retry_error_callback=log_exception,
    )
    def wait_for_action_finish() -> DataSequence[TaskData]:
        """
        Keep asking for task status, status_id,
        activity(optional), utill check_status is True

        Returns:
            TaskStatus: TaskStatus instance
        """
        task_data = get_task_data(session, task_id, delay_seconds)
        task_statuses = [task.status for task in task_data]
        task_statuses_id = [task.status_id for task in task_data]
        task_activities = [task.activity for task in task_data]
        logger.info(
            f"Statuses of action {task_id} is: "
            f"status: {task_statuses}, status_id: {task_statuses_id}, activity: {task_activities}."
        )
        return task_data

    return wait_for_action_finish()

def get_task_data(session: vManageSession, task_id: str, delay_seconds: int = 10) -> DataSequence[TaskData]:
    url = f"/dataservice/device/action/status/{task_id}"
    task_data = session.get_data(url)
    check_if_data_is_available(session = session,
    task_data = task_data, task_id = task_id, url=url, delay_seconds=delay_seconds)
    return DataSequence(TaskData, [create_dataclass(TaskData, subtask_data) for subtask_data in task_data])

def check_if_data_is_available(session: vManageSession, task_data: list, task_id: str, delay_seconds: int, url: str):
    
    if not task_data:
        all_tasks_ids = get_all_tasks(session)
        if task_id in all_tasks_ids:
            sleep(delay_seconds)
            task_data = session.get_data(url)
            if not task_data:
                raise EmptyTaskResponseError(
                    f"Task id {task_id} registered by vManage in all tasks list, "
                    f"but response about it's status didn't contain any information."
                )
        else:
            raise TaskNotRegisteredError(f"Task id {task_id} is not registered by vManage.")

