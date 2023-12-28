# mypy: disable-error-code="empty-body"

from vmngclient.endpoints import APIEndpoints, delete, get, post, put, versions
from vmngclient.model.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    Parcel,
    ParcelCreationResponse,
    ParcelInfo,
)
from vmngclient.model.configuration.feature_profile.sdwan.service import (
    GetServiceFeatureProfileQuery,
    GetServiceFeatureProfilesQuery,
)
from vmngclient.model.configuration.feature_profile.sdwan.service.appqoe import AppqoeParcelCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnCreationPayload
from vmngclient.typed_list import DataSequence


class ServiceFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service")
    def get_service_feature_profiles(self, params: GetServiceFeatureProfilesQuery) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service")
    def create_service_feature_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}")
    def get_service_feature_profile(
        self, service_id: str, params: GetServiceFeatureProfileQuery
    ) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}")
    def edit_service_feature_profile(
        self, service_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}")
    def delete_service_feature_profile(self, service_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/appqoe")
    def get_appqoe_parcels(self, service_id: str) -> ParcelInfo[AppqoeParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/appqoe")
    def create_appqoe_parcel(self, service_id: str, payload: AppqoeParcelCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/appqoe/{appqoe_id}")
    def get_appqoe_parcel(self, service_id: str, appqoe_id: str) -> Parcel[AppqoeParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/appqoe/{appqoe_id}")
    def edit_appqoe_parcel(
        self, service_id: str, appqoe_id: str, payload: AppqoeParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/appqoe/{appqoe_id}")
    def delete_appqoe_parcel(self, service_id: str, appqoe_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn")
    def get_lan_vpn_parcels(self, service_id: str) -> ParcelInfo[LanVpnCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn")
    def create_lan_vpn_parcel(self, service_id: str, payload: LanVpnCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}")
    def get_lan_vpn_parcel(self, service_id: str, lan_vpn_id: str) -> Parcel[LanVpnCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}")
    def edit_lan_vpn_parcel(
        self, service_id: str, lan_vpn_id: str, payload: LanVpnCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}")
    def delete_lan_vpn_parcel(self, service_id: str, lan_vpn_id: str) -> None:
        ...
