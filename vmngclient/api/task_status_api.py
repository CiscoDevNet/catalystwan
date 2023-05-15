from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional, cast

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore
from vmngclient.utils.operation_status import OperationStatus
from time import sleep
from vmngclient.exceptions import TaskValidationError
if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.primitives.task_status_api import SubTaskData, TaskResult, TaskData, TasksData

from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(__name__)

class TasksAPI:
    """
    API class for getting data about tasks
    """

    def __init__(self, session: vManageSession, task_id: str):
        self.session = session
        self.task_id = task_id
        self.url = f"/dataservice/device/action/status/{self.task_id}"

    def get_all_tasks(self) -> TasksData:
        """
        Get list of active tasks id's in vmanage

        Args:
            session (vManageSession): session

        Returns:
        TasksData: Data about all tasks in vmanage
        """
        url = "dataservice/device/action/status/tasks"
        json = self.session.get_json(url)
        return TasksData.parse_obj(json)

    def get_task_data(self) -> List[SubTaskData]:
        """
        Get data about all sub-tasks in task

        Args:
            delay_seconds (int, optional): If vmanage doesn't get data about task, after this time will asks again.
            Defaults to 5.

        Returns:
            List[SubTaskData]: List of all sub-tusks
        """
        self.__validate_task()
        task_data = self.session.get_data(self.url)
        return [SubTaskData.parse_obj(subtask_data) for subtask_data in task_data]
    
    def __validate_task(self) -> bool:
        WAIT_SECONDS = 10
        REPEATS_NUMBER = 2
        for _ in range(REPEATS_NUMBER):
            json = self.session.get_json(self.url)
            task_data = TaskData.parse_obj(json)
            if task_data.validation.status == OperationStatus.VALIDATION_SUCCESS:
                return True
            logger.warning(
                f"Task not validated properly yet, sleep {WAIT_SECONDS} seconds until next call")
            sleep(WAIT_SECONDS)
        
        raise TaskValidationError(
            f"After {REPEATS_NUMBER} task API calls, proper task validation status has not been received")
        
class Task:
    """
    API class for getting data about task/sub-tasks
    """

    def __init__(self, session: vManageSession, task_id: str):
        self.session = session
        self.task_id = task_id
        self.url = f"/dataservice/device/action/status/{self.task_id}"
        self.task_data: List[SubTaskData]

    def wait_for_completed(
        self,
        timeout_seconds: int = 300,
        interval_seconds: int = 5,
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
    ) -> TaskResult:
        """
        Method to check subtasks statuses of the task

        Example:
            # create session
            session = create_vManageSession(ip_address,admin_username,password,port=port)
            devices = DevicesAPI(session).get()
            vsmart = devices.filter(personality= Personality.VSMART]).single_or_default()

            # Prepare some action, and get it's id
            upgrade_id = SoftwareAction().upgrade_software()

            # Keep asking for reboot status until it's not in exit_statuses (Failure or Success)
            or timeout is not achieved (3000s)
            task = Task(session,upgrade_id).wait_for_completed()
            if task.result:
                #do something
            else:
                #do something else

        Args:


            timeout_seconds (int): After this time, function will stop requesting action status
            interval_seconds (int): interval between action status requests
            delay_seconds (int): if Vmanage didn't report task status, after this time api call would be repeated
            success_statuses (Union[List[OperationStatus], str]): list of positive sub-tasks statuses
            success_statuses_ids (Union[List[OperationStatus], str]): list of positive sub-tasks statuses id's
            fails_statuses_id (Union[List[OperationStatusId], str]): list of negative sub-tasks statuses
            fails_statuses_ids (Union[List[OperationStatusId], str]): list of negative sub-tasks statuses id's
            activity_text (str): activity text

        Returns:
            TaskResult(): result attr is True if all subtasks are success
             or is False if at least one is failed
        """
        success_statuses = [cast(OperationStatus, exit_status.value) for exit_status in success_statuses]
        failure_statuses = [cast(OperationStatus, exit_status.value) for exit_status in failure_statuses]
        success_statuses_ids = [
            cast(OperationStatusId, exit_status_id.value) for exit_status_id in success_statuses_ids
        ]
        failure_statuses_ids = [
            cast(OperationStatusId, exit_status_id.value) for exit_status_id in failure_statuses_ids
        ]
        activity_text = activity_text

        def check_status(task_data: List[SubTaskData]) -> bool:
            """
            Function checks if condition is met. If so,
            wait_for_completed stops asking for task status

            Args:
                task_data (List[SubTaskData]): list of all sub_tasks

            Returns:
                bool: False if condition is met
            """

            task_statuses_success = [task.status in success_statuses for task in task_data]
            task_statuses_failure = [task.status in failure_statuses for task in task_data]
            task_statuses_id_success = [task.status_id in success_statuses_ids for task in task_data]
            task_statuses_id_failure = [task.status_id in failure_statuses_ids for task in task_data]
            task_activities = [activity_text in task.activity for task in task_data]

            if all(task_statuses_success + task_statuses_id_success) or any(
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
        def wait_for_action_finish() -> List[SubTaskData]:
            """
            Keep asking for task status, status_id,
            activity(optional), untill check_status is True

            Returns:
                List[SubTaskData]
            """

            self.task_data = TasksAPI(self.session, self.task_id).get_task_data()
            sub_task_statuses = [task.status for task in self.task_data]
            sub_task_statuses_id = [task.status_id for task in self.task_data]
            sub_task_activities = [task.activity for task in self.task_data]
            logger.info(
                f"Sub-tasks data for task {self.task_id}: \n "
                f"statuses: {sub_task_statuses}, status_ids: {sub_task_statuses_id}, activities: {sub_task_activities}."
            )
            return self.task_data

        wait_for_action_finish()
        result = all([sub_task.status in success_statuses for sub_task in self.task_data])
        if result:
            logger.info("Task polling finished, because all subtasks successfully finished.")
        else:
            logger.info("Task polling finished, because at least one subtask failed or task is timeout.")
        return TaskResult(result=result, sub_tasks_data=self.task_data)
