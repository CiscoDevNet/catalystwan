from __future__ import annotations

import logging
from time import sleep
from typing import TYPE_CHECKING, List, Tuple, cast

from attr import define, field  # type: ignore
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from vmngclient.dataclasses import DataclassBase  # type: ignore

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.exceptions import EmptyTaskResponseError, TaskNotRegisteredError
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import FIELD_NAME, create_dataclass
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(__name__)


@define
class SubTaskData(DataclassBase):
    status: str
    status_id: str = field(metadata={FIELD_NAME: "statusId"})
    action: str
    activity: List[str]
    current_activity: str = field(metadata={FIELD_NAME: "currentActivity"})
    action_config: str = field(metadata={FIELD_NAME: "actionConfig"})
    order: int
    uuid: str
    hostname: str = field(metadata={FIELD_NAME: "host-name"})
    site_id: str = field(metadata={FIELD_NAME: "site-id"})


class TaskAPI:
    """
    API class for getting data about task/sub-tasks
    """

    def __init__(self, session: vManageSession, task_id: str):
        self.session = session
        self.task_id = task_id
        self.url = f"/dataservice/device/action/status/{self.task_id}"
        self.task_data: DataSequence[SubTaskData]

    def wait_for_completed(
        self,
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
    ) -> Tuple[bool, DataSequence[SubTaskData]]:
        """
        Method to check subtasks statuses

        Example:
            session = create_vManageSession(ip_address,admin_username,password,port=port)
            devices = DevicesAPI(session).devices
            vsmart_device = [dev for dev in devices if dev.personality == Personality.VSMART][0]

            reboot_action = RebootAction(session,devices)
            reboot_action.execute()

            # Keep asking for reboot status until it's not in exit_statuses (Failure or Success)
            or timeout is not achieved (3000s)
            task = TaskAPI(session,reboot_action.task_id).wait_for_completed()
            if task[0]:
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
            Tuple[bool, DataSequence[SubTaskData]]: returns True if all subtasks are success
             or returns False if at least one is failed
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

        def check_status(task_data: DataSequence[SubTaskData]) -> bool:
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
        def wait_for_action_finish() -> DataSequence[SubTaskData]:
            """
            Keep asking for task status, status_id,
            activity(optional), untill check_status is True

            Returns:
                DataSequence[SubTaskData]
            """

            self.task_data = self.get_task_data(delay_seconds)
            task_statuses = [task.status for task in self.task_data]
            task_statuses_id = [task.status_id for task in self.task_data]
            task_activities = [task.activity for task in self.task_data]
            logger.info(
                f"Sub-tasks data for task {self.task_id}: \n "
                f"statuses: {task_statuses}, status_ids: {task_statuses_id}, activities: {task_activities}."
            )
            return self.task_data

        wait_for_action_finish()
        result = all([sub_task.status in success_statuses for sub_task in self.task_data])
        if result:
            logger.info("Task polling finished, because all subtasks successfully finished.")
        else:
            logger.info("Task polling finished, because at least one subtask failed.")
        return result, self.task_data

    def get_task_data(self, delay_seconds: int = 5) -> DataSequence[SubTaskData]:
        self.task_data = self.session.get_data(self.url)
        self.__check_if_data_is_available(delay_seconds)

        return DataSequence(
            SubTaskData,
            [create_dataclass(SubTaskData, subtask_data) for subtask_data in self.task_data],  # type: ignore
        )

    def __check_if_data_is_available(self, delay_seconds):

        if not self.task_data:
            all_tasks_ids = self.__get_all_tasks()
            if self.task_id in all_tasks_ids:
                sleep(delay_seconds)
                self.task_data = self.session.get_data(self.url)
                if not self.task_data:
                    raise EmptyTaskResponseError(
                        f"Task id {self.task_id} registered by vManage in all tasks list, "
                        f"but response about it's status didn't contain any information."
                    )
            else:
                raise TaskNotRegisteredError(f"Task id {self.task_id} is not registered by vManage.")

    def __get_all_tasks(self) -> List[str]:
        """
        Get list of active tasks id's in vmanage

        Args:
            session (vManageSession): session

        Returns:
        List[str]: active tasks id's
        """
        url = "dataservice/device/action/status/tasks"
        tasks = self.session.get_json(url)
        return [process["processId"] for process in tasks["runningTasks"]]
