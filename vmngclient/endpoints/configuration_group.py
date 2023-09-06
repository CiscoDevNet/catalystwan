# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from vmngclient.endpoints import APIEndpoints, delete, post, put, versions


class Solution(str, Enum):
    MOBILITY = "mobility"
    SDWAN = "sdwan"
    NFVIRTUAL = "nfvirtual"


class ProfileId(BaseModel):
    id: str


# TODO Get mode lfrom schema
class ConfigGroupCreationPayload(BaseModel):
    name: str
    description: str
    solution: Solution
    profiles: Optional[List[ProfileId]]


class ConfigGroupEditPayload(BaseModel):
    name: str
    description: str
    solution: Solution
    profiles: Optional[List[ProfileId]]


class ConfigGroupCreationResponse(BaseModel):
    id: str


class EditedProfileId(BaseModel):
    profileId: str


class ConfigGroupEditResponse(BaseModel):
    id: str
    profiles: List[EditedProfileId]


class ConfigurationGroup(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/config-group")
    def create_config_group(self, payload: ConfigGroupCreationPayload) -> ConfigGroupCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/config-group/{config_group_id}")
    def delete_config_group(self, config_group_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/config-group/{config_group_id}")
    def edit_config_group(self, config_group_id: str, payload: ConfigGroupEditPayload) -> ConfigGroupEditResponse:
        ...
