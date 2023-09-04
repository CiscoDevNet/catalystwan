# mypy: disable-error-code="empty-body"
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, versions
from vmngclient.typed_list import DataSequence


class ProfileType(str, Enum):
    TRANSPORT = "transport"


class SchemaType(str, Enum):
    POST = "post"
    PUT = "put"


class SchemaTypeQuery(BaseModel):
    class Config:
        allow_population_by_field_name = True

    schema_type: SchemaType = Field(alias="schemaType")


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


class GetFeatureProfilesPayload(BaseModel):
    limit: Optional[int]
    offset: Optional[int]


class ConfigurationFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/aaa/schema", resp_json_key="request")
    def get_sdwan_system_aaa_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_sdwan_transport_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_sdwan_transport_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{transport_id}")
    def delete_sdwan_transport_feature_profile(self, transport_id: str) -> None:
        ...
