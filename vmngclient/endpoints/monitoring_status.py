# mypy: disable-error-code="empty-body"
from enum import Enum
from ipaddress import IPv4Address
from typing import List

from pydantic.v1 import BaseModel, Field

from vmngclient.endpoints import APIEndpoints, get, put
from vmngclient.typed_list import DataSequence


class StatusEnum(str, Enum):
    enable = "enable"
    disable = "disable"
    bypass = "bypass"
    custom = "custom"


index_name_field = Field(..., alias="indexName", regex="^[a-z]+$")


class Status(BaseModel):
    index_name: str = index_name_field
    status: StatusEnum
    display_name: str = Field(alias="displayName")


class UpdateStatus(BaseModel):
    index_name: str = index_name_field
    status: StatusEnum


class EnabledIndex(BaseModel):
    index_name: str = index_name_field


class DisabledDevice(BaseModel):
    ip_address: IPv4Address


class MonitoringStatus(APIEndpoints):
    def get_disabled_device_list(self):
        # GET /statistics/settings/disable/devicelist/{indexName}
        ...

    def update_statistics_device_list(self):
        # PUT /statistics/settings/disable/devicelist/{indexName}
        ...

    @get("/statistics/settings/status")
    def get_statistics_settings(self) -> DataSequence[Status]:
        ...

    @put("/statistics/settings/status")
    def update_statistics_settings(self, payload: List[UpdateStatus]) -> DataSequence[Status]:
        ...

    def get_enabled_index_for_device(self):
        # GET /statistics/settings/status/device
        ...
