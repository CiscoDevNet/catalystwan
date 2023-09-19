import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyDefinitionId(BaseModel):
    definition_id: str = Field(alias="definitionId")


class PolicyReference(BaseModel):
    id: str
    property: str


class PolicyDefinitionCreationPayload(BaseModel):
    name: str = Field(
        regex="^[a-zA-Z0-9_-]{1,128}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 128 characters",
    )
    description: str
    type: str


class PolicyDefinitionEditPayload(PolicyDefinitionCreationPayload, PolicyDefinitionId):
    pass


class PolicyDefinitionEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class PolicyDefinition(PolicyDefinitionEditPayload, InfoTag):
    last_updated: datetime.datetime = Field(alias="lastUpdated")
    owner: str
    mode: str
    optimized: str
    reference_count: int = Field(alias="referenceCount")
    references: List[PolicyReference]


class PolicyDefinitionPreview(BaseModel):
    preview: str
