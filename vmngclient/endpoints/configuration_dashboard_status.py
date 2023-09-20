# mypy: disable-error-code="empty-body"
from typing import List, Optional

from pydantic import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.utils.operation_status import OperationStatus


class SubTaskData(BaseModel):
    status: str
    status_id: str = Field(alias="statusId")
    action: Optional[str] = None
    activity: List[str]
    current_activity: Optional[str] = Field(None, alias="currentActivity")
    action_config: Optional[str] = Field(None, alias="actionConfig")
    order: Optional[int] = None
    uuid: Optional[str] = None
    hostname: Optional[str] = Field(None, alias="host-name")
    site_id: Optional[str] = Field(None, alias="site-id")


class TaskResult(BaseModel):
    result: bool
    sub_tasks_data: List[SubTaskData]


class RunningTaskData(BaseModel):
    details_url: Optional[str] = Field(None, alias="detailsURL")
    user_session_username: Optional[str] = Field(None, alias="userSessionUserName")
    rid: Optional[int] = Field(None, alias="@rid")
    tenant_name: Optional[str] = Field("tenantName")
    process_id: Optional[str] = Field(None, alias="processId")
    name: Optional[str] = None
    tenant_id: Optional[str] = Field(None, alias="tenantId")
    user_session_ip: Optional[str] = Field(None, alias="userSessionIP")
    action: Optional[str] = None
    start_time: Optional[int] = Field(None, alias="startTime")
    end_time: Optional[int] = Field(None, alias="endTime")
    status: Optional[str] = None


class Validation(BaseModel):
    status_type: Optional[str] = Field(None, alias="statusType")
    activity: Optional[List[str]] = Field(None, alias="activity")
    vmanage_ip: Optional[str] = Field(None, alias="vmanageIP")
    system_ip: Optional[str] = Field(None, alias="system-ip")
    device_id: Optional[str] = Field(None, alias="deviceID")
    uuid: Optional[str] = Field(None, alias="uuid")
    rid: Optional[int] = Field(None, alias="@rid")
    status_id: str = Field(alias="statusId")
    process_id: Optional[str] = Field(None, alias="processId")
    action_config: Optional[str] = Field(None, alias="actionConfig")
    current_activity: Optional[str] = Field(None, alias="currentActivity")
    action: Optional[str] = Field(None, alias="action")
    start_time: Optional[int] = Field(None, alias="startTime")
    request_status: Optional[str] = Field(None, alias="requestStatus")
    status: OperationStatus = Field(alias="status")
    order: Optional[int] = Field(None, alias="order")


class Summary(BaseModel):
    action: Optional[str] = Field(None, alias="action")
    name: Optional[str] = Field(None, alias="name")
    details_url: Optional[str] = Field(None, alias="detailsURL")
    start_time: Optional[str] = Field(None, alias="startTime")
    end_time: Optional[str] = Field(None, alias="endTime")
    user_session_user_name: Optional[str] = Field(None, alias="userSessionUserName")
    user_session_ip: Optional[str] = Field(None, alias="userSessionIP")
    tenant_name: Optional[str] = Field(None, alias="tenantName")
    total: Optional[int] = Field(None, alias="total")
    status: Optional[str] = Field(None, alias="status")
    count: Optional[dict] = Field(None, alias="count")


class TaskData(BaseModel):
    data: List[SubTaskData] = Field(default=[])
    validation: Optional[Validation] = None
    summary: Optional[Summary] = None
    is_cancel_enabled: Optional[bool] = Field(None, alias="isCancelEnabled")
    is_parallel_execution_enabled: Optional[bool] = Field(None, alias="isParallelExecutionEnabled")


class TasksData(BaseModel):
    running_tasks: List[RunningTaskData] = Field(alias="runningTasks")


class ConfigurationDashboardStatus(APIEndpoints):
    @get("/device/action/status/{task_id}")
    def find_status(self, task_id: str) -> TaskData:
        ...

    @get("/device/action/status/tasks")
    def find_running_tasks(self) -> TasksData:
        ...
