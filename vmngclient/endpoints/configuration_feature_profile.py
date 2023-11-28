# mypy: disable-error-code="empty-body"
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.api.configuration_groups.parcel import MainParcel
from vmngclient.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from vmngclient.model.feature_profile_parcel import FullConfigParcel
from vmngclient.typed_list import DataSequence


class Solution(str, Enum):
    MOBILITY = "mobility"
    SDWAN = "sdwan"
    NFVIRTUAL = "nfvirtual"
    SDROUTING = "sd-routing"


class ProfileType(str, Enum):
    TRANSPORT = "transport"
    SYSTEM = "system"
    CLI = "cli"
    SERVICE = "service"


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


class ParcelId(BaseModel):
    id: str = Field(alias="parcelId")


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

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system")
    def get_sdwan_system_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system")
    def create_sdwan_system_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/system/{system_id}")
    def delete_sdwan_system_feature_profile(self, system_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system/{system_id}/aaa")
    def create_aaa_profile_parcel_for_system(self, system_id: str, payload: MainParcel) -> ParcelId:
        ...


class SDRoutingConfigurationFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sd-routing/cli")
    def create_cli_feature_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sd-routing/cli/{cli_fp_id}/full-config")
    def create_cli_full_config_parcel(self, cli_fp_id: str, payload: FullConfigParcel) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sd-routing/cli/{cli_fp_id}")
    def delete_cli_feature_profile(self, cli_fp_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sd-routing/cli/{cli_fp_id}/full-config/{parcel_id}")
    def delete_cli_full_config_parcel(self, cli_fp_id: str, parcel_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sd-routing/cli/{cli_fp_id}/full-config/{parcel_id}")
    def edit_cli_full_config_parcel(self, cli_fp_id: str, parcel_id: str, payload: FullConfigParcel) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sd-routing/cli")
    def get_cli_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...
