from typing import List, Optional

from pydantic import BaseModel, Field

from vmngclient.primitives import APIPrimitiveBase
from vmngclient.utils.operation_status import OperationStatus


class SubTaskData(BaseModel):
    status: str
    status_id: str = Field(alias="statusId")
    action: str
    activity: List[str]
    current_activity: str = Field(alias="currentActivity")
    action_config: Optional[str] = Field(alias="actionConfig")
    order: Optional[int]
    uuid: Optional[str]
    hostname: Optional[str] = Field(alias="host-name")
    site_id: Optional[str] = Field(alias="site-id")


class TaskResult(BaseModel):
    result: bool
    sub_tasks_data: List[SubTaskData]


class RunningTaskData(BaseModel):
    details_url: str = Field(alias="detailsURL")
    user_session_username: str = Field(alias="userSessionUserName")
    rid: int = Field(alias="@rid")
    tenant_name: str = Field("tenantName")
    process_id: str = Field(alias="processId")
    name: str
    tenant_id: str = Field(alias="tenantId")
    user_session_ip: str = Field(alias="userSessionIP")
    action: str
    start_time: int = Field(alias="startTime")
    end_time: int = Field(alias="endTime")
    status: str


class Validation(BaseModel):
    status_type: str = Field(alias="statusType")
    activity: List[str] = Field(alias="activity")
    vmanage_ip: str = Field(alias="vmanageIP")
    system_ip: str = Field(alias="system-ip")
    device_id: str = Field(alias="deviceID")
    uuid: str = Field(alias="uuid")
    rid: int = Field(alias="@rid")
    status_id: str = Field(alias="statusId")
    process_id: str = Field(alias="processId")
    action_config: str = Field(alias="actionConfig")
    current_activity: str = Field(alias="currentActivity")
    action: str = Field(alias="action")
    start_time: int = Field(alias="startTime")
    request_status: str = Field(alias="requestStatus")
    status: OperationStatus = Field(alias="status")
    order: int = Field(alias="order")


class Summary(BaseModel):
    action: str = Field(alias="action")
    name: str = Field(alias="name")
    details_url: str = Field(alias="detailsURL")
    start_time: str = Field(alias="startTime")
    end_time: str = Field(alias="endTime")
    user_session_user_name: str = Field(alias="userSessionUserName")
    user_session_ip: str = Field(alias="userSessionIP")
    tenant_name: str = Field(alias="tenantName")
    total: int = Field(alias="total")
    status: str = Field(alias="status")
    count: dict = Field(alias="count")


class TaskData(BaseModel):
    data: List[SubTaskData]
    validation: Validation
    summary: Summary
    is_cancel_enabled: bool = Field(alias="isCancelEnabled")
    is_parallel_execution_enabled: bool = Field(alias="isParallelExecutionEnabled")


class TasksData(BaseModel):
    running_tasks: List[RunningTaskData] = Field(alias="runningTasks")


class TasksPrimitives(APIPrimitiveBase):
    """
    API class for getting data about tasks
    """

    def get_task_data(self, task_id) -> TaskData:
        """
        Get data about all sub-tasks in task

        Args:
            delay_seconds (int, optional): If vmanage doesn't get data about task, after this time will asks again.
            Defaults to 5.

        Returns:
            List[SubTaskData]: List of all sub-tusks
        """
        url = f"/dataservice/device/action/status/{task_id}"
        task_data = self.session.get_json(url)
        return TaskData.parse_obj(task_data)

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
