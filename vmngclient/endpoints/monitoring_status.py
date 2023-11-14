# mypy: disable-error-code="empty-body"
from enum import Enum

from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get
from vmngclient.typed_list import DataSequence


class StatusEnum(str, Enum):
    enable = "enable"
    disable = "disable"
    bypass = "bypass"
    custom = "custom"


class Status(BaseModel):
    index_name: str = Field(alias="indexName")
    status: StatusEnum
    display_name: str = Field(alias="displayName")


class MonitoringStatus(APIEndpoints):
    def get_disabled_device_list(self):
        # GET /statistics/settings/disable/devicelist/{indexName}
        ...

    def get_enabled_index_for_device(self):
        # GET /statistics/settings/status/device
        ...

    @get("/statistics/settings/status")
    def get_statistics_settings(self) -> DataSequence[Status]:
        ...

    def update_statistics_device_list(self):
        # PUT /statistics/settings/disable/devicelist/{indexName}
        ...

    def update_statistics_settings(self):
        # PUT /statistics/settings/status
        ...
