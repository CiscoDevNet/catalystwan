# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    Parcel,
    ParcelId,
)
from catalystwan.typed_list import DataSequence


class OtherFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("​/v1​/feature-profile​/sdwan​/other")
    def get_sdwan_other_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/other")
    def create_sdwan_other_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/other/{profile_id}")
    def delete_sdwan_other_feature_profile(self, profile_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/other/{profile_id}/{parcel_type}")
    def get_all(self, profile_id: UUID, parcel_type: UUID) -> DataSequence[Parcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/other/{profile_id}/{parcel_type}/{parcel_id}")
    def get_by_id(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> Parcel:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/feature-profile/sdwan/other/{profile_id}/{parcel_type}/{parcel_id}")
    def update(self, profile_id: UUID, parcel_type: str, parcel_id: UUID, payload: _ParcelBase) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/other/{profile_id}/{parcel_type}/{parcel_id}")
    def delete(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/other/{profile_id}/{parcel_type}")
    def create(self, profile_id: UUID, parcel_type: str, payload: _ParcelBase) -> ParcelId:
        ...
