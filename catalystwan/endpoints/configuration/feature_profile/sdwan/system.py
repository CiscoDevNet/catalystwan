# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    ParcelId,
    SchemaTypeQuery,
)
from catalystwan.typed_list import DataSequence


class SystemFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/aaa/schema", resp_json_key="request")
    def get_sdwan_system_aaa_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
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
    @put("/v1/feature-profile/sdwan/system/{system_id}/aaa/{parcel_id}")
    def edit_aaa_profile_parcel_for_system(self, system_id: str, parcel_id: str, payload: _ParcelBase) -> ParcelId:
        ...
