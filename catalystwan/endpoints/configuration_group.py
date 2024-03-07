# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.common import Solution
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.typed_list import DataSequence


class ProfileId(BaseModel):
    id: UUID


# TODO Get mode from schema
class ConfigGroupCreationPayload(BaseModel):
    name: str
    description: str
    solution: Solution
    profiles: Optional[List[ProfileId]]


class FeatureProfile(BaseModel):
    id: str
    name: str
    description: Optional[str]
    solution: str
    type: ProfileType
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")


class ConfigGroup(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    solution: Solution
    profiles: Optional[List[FeatureProfile]]
    source: Optional[str] = None
    state: Optional[str] = None
    devices: List = Field(default=[])
    created_by: Optional[str] = Field(alias="createdBy")
    last_updated_by: Optional[str] = Field(alias="lastUpdatedBy")
    created_on: Optional[datetime] = Field(alias="createdOn")
    last_updated_on: Optional[datetime] = Field(alias="lastUpdatedOn")
    version: int
    number_of_devices: int = Field(alias="numberOfDevices")
    number_of_devices_up_to_date: int = Field(alias="numberOfDevicesUpToDate")
    origin: Optional[str]
    topology: Optional[str] = None
    full_config_cli: bool = Field(alias="fullConfigCli")


class ConfigGroupResponsePayload(BaseModel):
    config_groups: List[ConfigGroup]


class ConfigGroupEditPayload(BaseModel):
    name: str
    description: str
    solution: Solution
    profiles: Optional[List[ProfileId]]


class DeviceId(BaseModel):
    id: str


class ConfigGroupAssociatePayload(BaseModel):
    devices: List[DeviceId]


class ConfigGroupVariablesCreatePayload(BaseModel):
    deviceIds: List[str]
    suggestions: bool = True


class VariableData(BaseModel):
    name: str
    value: str


class DeviceVariables(BaseModel):
    device_id: str = Field(alias="device-id")
    variables: List[VariableData]


class GroupVariables(BaseModel):
    name: str
    group_variables: List[VariableData] = Field(alias="group-variables")


class ConfigGroupVariablesCreateResponse(BaseModel):
    family: Solution
    devices: List[DeviceVariables]
    groups: List[GroupVariables]


class ConfigGroupVariablesEditPayload(BaseModel):
    solution: Solution
    devices: List[DeviceVariables]


class ConfigGroupDeployPayload(BaseModel):
    devices: List[DeviceId]


class ConfigGroupDeployResponse(BaseModel):
    parentTaskId: str


class ConfigGroupDisassociateResponse(BaseModel):
    parentTaskId: str


class ConfigGroupCreationResponse(BaseModel):
    id: UUID


class EditedProfileId(BaseModel):
    profileId: str


class ConfigGroupEditResponse(BaseModel):
    id: str
    profiles: List[EditedProfileId]


class ConfigurationGroup(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/config-group/{config_group_id}/device/associate")
    def associate(self, config_group_id: str, payload: ConfigGroupAssociatePayload) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/config-group")
    def create_config_group(self, payload: ConfigGroupCreationPayload) -> ConfigGroupCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/config-group/{config_group_id}/device/variables")
    def create_variables(
        self, config_group_id: str, payload: ConfigGroupVariablesCreatePayload
    ) -> ConfigGroupVariablesCreateResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/config-group/{config_group_id}")
    def delete_config_group(self, config_group_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/config-group/{config_group_id}/device/deploy")
    def deploy(self, config_group_id: str, payload: ConfigGroupDeployPayload) -> ConfigGroupDeployResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/config-group/{config_group_id}/device/associate")
    def disassociate(
        self, config_group_id: str, payload: ConfigGroupAssociatePayload
    ) -> ConfigGroupDisassociateResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/config-group/{config_group_id}")
    def edit_config_group(self, config_group_id: str, payload: ConfigGroupEditPayload) -> ConfigGroupEditResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/config-group")
    def get(self) -> DataSequence[ConfigGroup]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/config-group/{config_group_id}/device/variables")
    def update_variables(self, config_group_id: str, payload: ConfigGroupVariablesEditPayload) -> None:
        ...
