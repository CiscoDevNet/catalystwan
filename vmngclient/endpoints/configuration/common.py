from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from vmngclient.model.configuration.feature_profile.common import ProfileType


class SchemaType(str, Enum):
    POST = "post"
    PUT = "put"


class SchemaTypeQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_type: SchemaType = Field(alias="schemaType")


class Solution(str, Enum):
    MOBILITY = "mobility"
    SDWAN = "sdwan"
    NFVIRTUAL = "nfvirtual"
    SDROUTING = "sd-routing"


class FeatureProfileInfo(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: str
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")


class FeatureProfileCreationPayload(BaseModel):
    name: str
    description: str


class FeatureProfileCreationResponse(BaseModel):
    id: str


class ParcelId(BaseModel):
    id: str = Field(alias="parcelId")


class GetFeatureProfilesPayload(BaseModel):
    limit: Optional[int]
    offset: Optional[int]
