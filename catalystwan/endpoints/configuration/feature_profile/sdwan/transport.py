# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    GetFeatureProfilesPayload,
    ParcelCreationResponse,
    ParcelId,
    SchemaTypeQuery,
)
from catalystwan.models.configuration.feature_profile.sdwan.management.vpn import ManagementVPN
from catalystwan.models.configuration.feature_profile.sdwan.transport import CellularControllerParcel
from catalystwan.typed_list import DataSequence


class TransportFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_transport_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_transport_feature_profiles(self, params: GetFeatureProfilesPayload) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}")
    def get_transport_feature_profile(self, profile_id: str, params: GetFeatureProfilesPayload) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/transport/{profile_id}")
    def edit_transport_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{profile_id}")
    def delete_transport_feature_profile(self, profile_id: str) -> None:
        ...

    #
    # ManagementVPN parcel
    #
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn")
    def create_management_vpn_parcel(self, profile_id: str, payload: _ParcelBase) -> ParcelCreationResponse:
        ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn")
    # def get_management_vpn_parcels(self, profile_id: str) -> ParcelSequence[ManagementVPN]:
    #     ...

    # @versions(supported_versions=(">=20.13"), raises=False)
    # @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    # def get_management_vpn_parcel(self, profile_id: str, parcel_id: str) -> Parcel[ManagementVPN]:
    #     ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def edit_management_vpn_parcel(
        self, profile_id: str, parcel_id: str, payload: ManagementVPN
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def delete_management_vpn_parcel(self, profile_id: str, parcel_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_sdwan_transport_feature_profiles(
        self, payload: Optional[GetFeatureProfilesPayload]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/cellular-controller/schema", resp_json_key="request")
    def get_sdwan_transport_cellular_controller_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
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
    @post("/v1/feature-profile/sdwan/transport/{transport_id}/cellular-controller")
    def create_cellular_controller_profile_parcel_for_transport(
        self, transport_id: str, payload: CellularControllerParcel
    ) -> ParcelId:
        ...
