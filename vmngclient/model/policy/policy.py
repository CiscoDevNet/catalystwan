import datetime
from typing import Optional, Sequence

from pydantic import BaseModel, Field


class PolicyId(BaseModel):
    policy_id: str = Field(alias="policyId")


class AssemblyItem(BaseModel):
    definition_id: str = Field(alias="definitionId")
    type: str

    class Config:
        allow_population_by_field_name = True


class PolicyDefinition(BaseModel):
    assembly: Sequence[AssemblyItem]


class PolicyCreationPayload(BaseModel):
    policy_name: str = Field(
        alias="policyName",
        regex="^[a-zA-Z0-9_-]{1,127}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 127 characters",
    )
    policy_description: str = Field("Default description", alias="policyDescription")
    policy_type: str = Field(alias="policyType")
    policy_definition: PolicyDefinition = Field(alias="policyDefinition")
    is_policy_activated: bool = Field(default=False, alias="isPolicyActivated")

    class Config:
        allow_population_by_field_name = True


class PolicyEditPayload(PolicyCreationPayload, PolicyId):
    pass


class PolicyInfo(PolicyEditPayload):
    created_by: str = Field(alias="createdBy")
    created_on: datetime.datetime = Field(alias="createdOn")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    last_updated_on: datetime.datetime = Field(alias="lastUpdatedOn")
    policy_version: Optional[str] = Field(None, alias="policyVersion")
