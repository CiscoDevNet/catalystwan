# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
)
from catalystwan.models.feature_profile_parcel import FullConfigParcel
from catalystwan.typed_list import DataSequence


class SchemaType(str, Enum):
    POST = "post"
    PUT = "put"


class SchemaTypeQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_type: SchemaType = Field(alias="schemaType")


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
    @get("/v1/feature-profile/sdwan/transport/cellular-controller/schema", resp_json_key="request")
    def get_sdwan_transport_cellular_controller_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
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
    def create_aaa_profile_parcel_for_system(self, system_id: str, payload: _ParcelBase) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{transport_id}/cellular-controller")
    def create_cellular_controller_profile_parcel_for_transport(
        self, transport_id: str, payload: _ParcelBase
    ) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan")
    def get_sdwan_feature_profiles(self) -> DataSequence[FeatureProfileInfo]:
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
