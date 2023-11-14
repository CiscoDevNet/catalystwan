# mypy: disable-error-code="empty-body"
from typing import List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.utils.operation_status import OperationStatus


class SubTaskData(BaseModel):
    status: str
    status_id: str = Field(alias="statusId")
    action: Optional[str]
    activity: List[str]
    current_activity: Optional[str] = Field(alias="currentActivity")
    action_config: Optional[str] = Field(alias="actionConfig")
    order: Optional[int]
    uuid: Optional[str]
    hostname: Optional[str] = Field(alias="host-name")
    site_id: Optional[str] = Field(alias="site-id")


class TaskResult(BaseModel):
    result: bool
    sub_tasks_data: List[SubTaskData]


class RunningTaskData(BaseModel):
    details_url: Optional[str] = Field(alias="detailsURL")
    user_session_username: Optional[str] = Field(alias="userSessionUserName")
    rid: Optional[int] = Field(alias="@rid")
    tenant_name: Optional[str] = Field("tenantName")
    process_id: Optional[str] = Field(alias="processId")
    name: Optional[str]
    tenant_id: Optional[str] = Field(alias="tenantId")
    user_session_ip: Optional[str] = Field(alias="userSessionIP")
    action: Optional[str]
    start_time: Optional[int] = Field(alias="startTime")
    end_time: Optional[int] = Field(alias="endTime")
    status: Optional[str]


class Validation(BaseModel):
    status_type: Optional[str] = Field(alias="statusType")
    activity: Optional[List[str]] = Field(alias="activity")
    vmanage_ip: Optional[str] = Field(alias="vmanageIP")
    system_ip: Optional[str] = Field(alias="system-ip")
    device_id: Optional[str] = Field(alias="deviceID")
    uuid: Optional[str] = Field(alias="uuid")
    rid: Optional[int] = Field(alias="@rid")
    status_id: str = Field(alias="statusId")
    process_id: Optional[str] = Field(alias="processId")
    action_config: Optional[str] = Field(alias="actionConfig")
    current_activity: Optional[str] = Field(alias="currentActivity")
    action: Optional[str] = Field(alias="action")
    start_time: Optional[int] = Field(alias="startTime")
    request_status: Optional[str] = Field(alias="requestStatus")
    status: OperationStatus = Field(alias="status")
    order: Optional[int] = Field(alias="order")


class Summary(BaseModel):
    action: Optional[str] = Field(alias="action")
    name: Optional[str] = Field(alias="name")
    details_url: Optional[str] = Field(alias="detailsURL")
    start_time: Optional[str] = Field(alias="startTime")
    end_time: Optional[str] = Field(alias="endTime")
    user_session_user_name: Optional[str] = Field(alias="userSessionUserName")
    user_session_ip: Optional[str] = Field(alias="userSessionIP")
    tenant_name: Optional[str] = Field(alias="tenantName")
    total: Optional[int] = Field(alias="total")
    status: Optional[str] = Field(alias="status")
    count: Optional[dict] = Field(alias="count")


class TaskData(BaseModel):
    data: List[SubTaskData] = Field(default=[])
    validation: Optional[Validation]
    summary: Optional[Summary]
    is_cancel_enabled: Optional[bool] = Field(alias="isCancelEnabled")
    is_parallel_execution_enabled: Optional[bool] = Field(alias="isParallelExecutionEnabled")


class TasksData(BaseModel):
    running_tasks: List[RunningTaskData] = Field(alias="runningTasks")


class ConfigurationDashboardStatus(APIEndpoints):
    @get("/device/action/status/{task_id}")
    def find_status(self, task_id: str) -> TaskData:
        ...

    @get("/device/action/status/tasks")
    def find_running_tasks(self) -> TasksData:
        ...
