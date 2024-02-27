# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.typed_list import DataSequence


class RebootEntry(BaseModel):
    model_config = ConfigDict(extra="allow")
    reason: Optional[str] = Field(default=None, validation_alias=AliasChoices("reboot_reason", "reload-desc"))
    severity: Optional[str] = Field(default=None, validation_alias="reload-severity", description=">=17.13 only")
    category: Optional[str] = Field(default=None, validation_alias="reload-category", description=">=17.13 only")
    date_time: datetime = Field(validation_alias=AliasChoices("reboot_date_time-date", "reload-time-date"))
    last_updated: datetime = Field(validation_alias="lastupdated")
    vdevice_name: str = Field(validation_alias="vdevice-name")
    vdevice_host_name: str = Field(validation_alias="vdevice-host-name")


class RealTimeMonitoringRebootHistory(APIEndpoints):
    @get("/device/reboothistory", "data")
    def create_reboot_history_list(self, params: dict) -> DataSequence[RebootEntry]:
        ...

    def create_synced_reboot_history_list(self):
        # GET /device/reboothistory/synced
        ...

    def get_reboot_history_details(self):
        # GET /device/reboothistory/details
        ...
