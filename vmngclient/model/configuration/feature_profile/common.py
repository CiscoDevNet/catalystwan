from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.model.configuration.common import Solution
from vmngclient.model.profileparcel.traffic_policy import CgFpPpNameDef, UuidDef


class ProfileType(str, Enum):
    TRANSPORT = "transport"
    SYSTEM = "system"
    CLI = "cli"
    SERVICE = "service"


class FeatureProfileInfo(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")
    associated_profile_parcels: List[str] = Field(alias="associatedProfileParcels")
    rid: int = Field(alias="@rid")
    profile_parcel_count: int = Field(alias="profileParcelCount")
    cached_profile: Optional[str] = Field(alias="cachedProfile")


class FromFeatureProfile(BaseModel):
    copy_: UuidDef = Field(alias="copy")


class FeatureProfileCreationPayload(BaseModel):
    name: CgFpPpNameDef
    description: str
    from_feature_profile: Optional[FromFeatureProfile] = Field(alias="fromFeatureProfile", default=None)


class FeatureProfileEditPayload(BaseModel):
    name: CgFpPpNameDef
    description: str


class FeatureProfileCreationResponse(BaseModel):
    id: UuidDef
