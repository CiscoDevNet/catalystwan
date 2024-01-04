# mypy: disable-error-code="empty-body"
from typing import Any
from vmngclient.endpoints import APIEndpoints, delete, get, post, put, versions
from vmngclient.model.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    GetFeatureProfileQuery,
    GetFeatureProfilesQuery,
    ParcelCreationResponse,
    ParcelDetails,
    ParcelSequence

)
from vmngclient.typed_list import DataSequence

from vmngclient.api.configuration_groups.parcel import MainParcel
from vmngclient.model.configuration.feature_profile.sdwan.transport.management.vpn import ManagementVPN

class TransportFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_transport_feature_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_transport_feature_profiles(self, params: GetFeatureProfilesQuery) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}")
    def get_transport_feature_profile(
        self, profile_id: str, params: GetFeatureProfileQuery
    ) -> FeatureProfileDetail:
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
    def create_management_vpn_parcel(self, profile_id: str, payload: MainParcel) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn")
    def get_management_vpn_parcels(self, profile_id: str) -> ParcelSequence[ManagementVPN]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def get_management_vpn_parcel(
        self, profile_id: str, parcel_id:str
    ) -> ParcelDetails[ManagementVPN]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def edit_management_vpn_parcel(
        self, profile_id: str, parcel_id:str, payload: MainParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def delete_management_vpn_parcel(self, profile_id: str,  parcel_id:str) -> None:
        ...