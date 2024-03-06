# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, cast

from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed  # type: ignore

from catalystwan.exceptions import TaskValidationError

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.endpoints.configuration_dashboard_status import (
    ConfigurationDashboardStatus,
    SubTaskData,
    TaskData,
    TaskResult,
)
from catalystwan.utils.operation_status import OperationStatus, OperationStatusId

logger = logging.getLogger(__name__)


class Task:
    """
    API class for getting data about task/sub-tasks
    """

    def __init__(self, session: ManagerSession, task_id: str):
        self.session = session
        self.task_id = task_id
        self.url = f"/dataservice/device/action/status/{self.task_id}"
        self.task_data: List[SubTaskData]

    def __check_validation_status(self, task: TaskData):
        if not task.validation:
            return None
        if task.validation.status in (OperationStatus.FAILURE, OperationStatus.VALIDATION_FAILURE):
            raise TaskValidationError(f"Task status validation failed, validation status is: {task.validation.status}")

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
    ) -> TaskResult:
        """
        Method to check subtasks statuses of the task

        Example:
            # create session
            session = create_manager_session(ip_address,admin_username,password,port=port)
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
            validation_timeout_seconds (int): After this time, task validation call will be send
            delay_seconds (int): if Vmanage didn't report task status, after this time api call would be repeated
            success_statuses (Union[List[OperationStatus], str]): list of positive sub-tasks statuses
            success_statuses_ids (Union[List[OperationStatus], str]): list of positive sub-tasks statuses id's
            fails_statuses_id (Union[List[OperationStatusId], str]): list of negative sub-tasks statuses
            fails_statuses_ids (Union[List[OperationStatusId], str]): list of negative sub-tasks statuses id's

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

        def check_status(task_data: List[SubTaskData]) -> bool:
            """
            Function checks if condition is met. If so,
            wait_for_completed stops asking for task status

            Args:
                task_data (List[SubTaskData]): list of all sub_tasks

            Returns:
                bool: False if condition is met
            """
            if not task_data:
                return True
            task_statuses_success = [task.status in success_statuses for task in task_data]
            task_statuses_failure = [task.status in failure_statuses for task in task_data]
            task_statuses_id_success = [task.status_id in success_statuses_ids for task in task_data]
            task_statuses_id_failure = [task.status_id in failure_statuses_ids for task in task_data]

            all_subtasks_completed_status: List[bool] = [
                any(task_status) for task_status in zip(task_statuses_success, task_statuses_failure)
            ]
            all_subtasks_completed_status_id: List[bool] = [
                any(task_status_id) for task_status_id in zip(task_statuses_id_success, task_statuses_id_failure)
            ]
            if all(all_subtasks_completed_status) or all(all_subtasks_completed_status_id):
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
            task = ConfigurationDashboardStatus(self.session).find_status(self.task_id)
            self.__check_validation_status(task)
            self.task_data = task.data
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
