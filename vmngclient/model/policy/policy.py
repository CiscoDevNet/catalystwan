import datetime
from typing import Any, List, Optional

from pydantic.v1 import BaseModel, Field


class PolicyId(BaseModel):
    policy_id: str = Field(alias="policyId")


class AssemblyItem(BaseModel):
    definition_id: str = Field(alias="definitionId")
    type: str
    entries: Optional[List[Any]] = []


class PolicyDefinition(BaseModel):
    assembly: List[AssemblyItem]


class PolicyCreationPayload(BaseModel):
    policy_name: str = Field(
        alias="policyName",
        regex="^[a-zA-Z0-9_-]{1,127}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 127 characters",
    )
    policy_description: str = Field(alias="policyDescription")
    policy_type: str = Field(alias="policyType")
    policy_definition: PolicyDefinition = Field(alias="policyDefinition")
    is_policy_activated: bool = Field(default=False, alias="isPolicyActivated")


class PolicyEditPayload(PolicyCreationPayload, PolicyId):
    pass


class PolicyInfo(PolicyEditPayload):
    created_by: str = Field(alias="createdBy")
    created_on: datetime.datetime = Field(alias="createdOn")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    last_updated_on: datetime.datetime = Field(alias="lastUpdatedOn")
    policy_version: str = Field(alias="policyVersion")
