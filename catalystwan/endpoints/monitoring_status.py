# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, RootModel

from catalystwan.endpoints import APIEndpoints, get, put
from catalystwan.typed_list import DataSequence


class StatusEnum(str, Enum):
    enable = "enable"
    disable = "disable"
    bypass = "bypass"
    custom = "custom"


index_name_field = Field(..., alias="indexName", pattern="^[a-z]+$")


class Status(BaseModel):
    index_name: str = index_name_field
    status: StatusEnum
    display_name: str = Field(alias="displayName")


class UpdateStatus(BaseModel):
    index_name: str = index_name_field
    status: StatusEnum


class EnabledIndex(BaseModel):
    index_name: str = index_name_field


SingleList = RootModel[List[str]]  # trick to make endpoint return list of strings


class DisabledDeviceList(SingleList):
    pass


class DisabledDeviceListResponse(SingleList):
    pass


class UpdateIndexResponse(BaseModel):
    response: bool


class EnabledIndexDeviceListResponse(SingleList):
    pass


class MonitoringStatus(APIEndpoints):
    @get("/statistics/settings/disable/devicelist/{indexName}")
    def get_disabled_device_list(self, indexName: str) -> DisabledDeviceListResponse:
        ...

    @put("/statistics/settings/disable/devicelist/{indexName}", "response")
    def update_statistics_device_list(self, indexName: str, payload: DisabledDeviceList) -> UpdateIndexResponse:
        ...

    @get("/statistics/settings/status")
    def get_statistics_settings(self) -> DataSequence[Status]:
        ...

    @put("/statistics/settings/status")
    def update_statistics_settings(self, payload: List[UpdateStatus]) -> DataSequence[Status]:
        ...

    @get("/statistics/settings/status/device")
    def get_enabled_index_for_device(self, params: dict) -> EnabledIndexDeviceListResponse:
        ...
