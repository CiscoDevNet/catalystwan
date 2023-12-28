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
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.gre import InterfaceGreCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecCreationPayload
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

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ethernet")
    def get_lan_vpn_interface_ethernet_parcels(
        self, service_id: str, lan_vpn_id: str
    ) -> ParcelInfo[InterfaceEthernetCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ethernet")
    def create_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, payload: InterfaceEthernetCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ethernet/{interface_ethernet_id}"
    )
    def get_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str
    ) -> Parcel[InterfaceEthernetCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ethernet/{interface_ethernet_id}"
    )
    def edit_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, payload: InterfaceEthernetCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ethernet/{interface_ethernet_id}"
    )
    def delete_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/gre")
    def get_lan_vpn_interface_gre_parcels(
        self, service_id: str, lan_vpn_id: str
    ) -> ParcelInfo[InterfaceGreCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/gre")
    def create_lan_vpn_interface_gre_parcel(
        self, service_id: str, lan_vpn_id: str, payload: InterfaceGreCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/gre/{interface_gre_id}")
    def get_lan_vpn_interface_gre_parcel(
        self, service_id: str, lan_vpn_id: str, interface_gre_id: str
    ) -> Parcel[InterfaceGreCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/gre/{interface_gre_id}")
    def edit_lan_vpn_interface_gre_parcel(
        self, service_id: str, lan_vpn_id: str, interface_gre_id: str, payload: InterfaceGreCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/gre/{interface_gre_id}")
    def delete_lan_vpn_interface_gre_parcel(self, service_id: str, lan_vpn_id: str, interface_gre_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ipsec")
    def get_lan_vpn_interface_ipsec_parcels(
        self, service_id: str, lan_vpn_id: str
    ) -> ParcelInfo[InterfaceIpsecCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ipsec")
    def create_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, payload: InterfaceIpsecCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ipsec/{interface_ipsec_id}")
    def get_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str
    ) -> Parcel[InterfaceIpsecCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ipsec/{interface_ipsec_id}")
    def edit_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str, payload: InterfaceIpsecCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/ipsec/{interface_ipsec_id}")
    def delete_lan_vpn_interface_ipsec_parcel(self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str) -> None:
        ...
