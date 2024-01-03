# mypy: disable-error-code="empty-body"

from vmngclient.endpoints import APIEndpoints, delete, get, post, put, versions
from vmngclient.model.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    Parcel,
    ParcelAssociationPayload,
    ParcelCreationResponse,
    ParcelInfo,
)
from vmngclient.model.configuration.feature_profile.sdwan.service import (
    GetServiceFeatureProfileQuery,
    GetServiceFeatureProfilesQuery,
)
from vmngclient.model.configuration.feature_profile.sdwan.service.appqoe import AppqoeParcelCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.bgp import BgpCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.dhcp_server import DhcpSeverParcelCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.eigrp import EigrpCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.gre import InterfaceGreCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.multicast import MulticastCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.ospf import OspfCreationPayload
from vmngclient.model.configuration.feature_profile.sdwan.service.ospfv3 import (
    Ospfv3IPv4CreationPayload,
    Ospfv3IPv6CreationPayload,
)
from vmngclient.model.configuration.feature_profile.sdwan.service.tracker import (
    TrackerGroupParcelCreationPayload,
    TrackerParcelCreationPayload,
)
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

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/svi")
    def get_lan_vpn_interface_svi_parcels(
        self, service_id: str, lan_vpn_id: str
    ) -> ParcelInfo[InterfaceSviCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/svi")
    def create_lan_vpn_interface_svi_parcel(
        self, service_id: str, lan_vpn_id: str, payload: InterfaceSviCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/svi/{interface_svi_id}")
    def get_lan_vpn_interface_svi_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str
    ) -> Parcel[InterfaceSviCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/svi/{interface_svi_id}")
    def edit_lan_vpn_interface_svi_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str, payload: InterfaceSviCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/interface/svi/{interface_svi_id}")
    def delete_lan_vpn_interface_svi_parcel(self, service_id: str, lan_vpn_id: str, interface_svi_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/dhcp-server")
    def get_dhcp_server_parcels(self, service_id: str) -> ParcelInfo[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/dhcp-server")
    def create_dhcp_server_parcel(
        self, service_id: str, payload: DhcpSeverParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/dhcp-server/{dhcp_server_id}")
    def get_dhcp_server_parcel(self, service_id: str, dhcp_server_id: str) -> Parcel[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/dhcp-server/{dhcp_server_id}")
    def edit_dhcp_server_parcel(
        self, service_id: str, dhcp_server_id: str, payload: DhcpSeverParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/dhcp-server/{dhcp_server_id}")
    def delete_dhcp_server_parcel(self, service_id: str, dhcp_server_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ethernet/{interface_ethernet_id}/dhcp-server"
    )
    def get_dhcp_server_parcels_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str
    ) -> ParcelInfo[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/dhcp-server"
    )
    def associate_lan_vpn_interface_ethernet_parcel_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/dhcp-server/{dhcp_server_id}"
    )
    def get_dhcp_server_parcel_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, dhcp_server_id: str
    ) -> Parcel[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/dhcp-server/{dhcp_server_id}"
    )
    def edit_lan_vpn_interface_ethernet_parcel_association_with_dhcp_server_parcel(
        self,
        service_id: str,
        lan_vpn_id: str,
        interface_ethernet_id: str,
        dhcp_server_id: str,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/dhcp-server/{dhcp_server_id}"
    )
    def delete_lan_vpn_interface_ethernet_parcel_association_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, dhcp_server_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ipsec/{interface_ipsec_id}/dhcp-server"
    )
    def get_dhcp_server_parcels_associated_with_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str
    ) -> ParcelInfo[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ipsec/{interface_ipsec_id}/dhcp-server"
    )
    def associate_lan_vpn_interface_ipsec_parcel_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ipsec/{interface_ipsec_id}/dhcp-server/{dhcp_server_id}"
    )
    def get_dhcp_server_parcel_associated_with_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str, dhcp_server_id: str
    ) -> Parcel[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ipsec/{interface_ipsec_id}/dhcp-server/{dhcp_server_id}"
    )
    def edit_lan_vpn_interface_ipsec_parcel_association_with_dhcp_server_parcel(
        self,
        service_id: str,
        lan_vpn_id: str,
        interface_ipsec_id: str,
        dhcp_server_id: str,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ipsec/{interface_ipsec_id}/dhcp-server/{dhcp_server_id}"
    )
    def delete_lan_vpn_interface_ipsec_parcel_association_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str, dhcp_server_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/svi/{interface_svi_id}/dhcp-server"
    )
    def get_dhcp_server_parcels_associated_with_lan_vpn_interface_svi_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str
    ) -> ParcelInfo[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/svi/{interface_svi_id}/dhcp-server"
    )
    def associate_lan_vpn_interface_svi_parcel_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/svi/{interface_svi_id}/dhcp-server/{dhcp_server_id}"
    )
    def get_dhcp_server_parcel_associated_with_lan_vpn_interface_svi_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str, dhcp_server_id: str
    ) -> Parcel[DhcpSeverParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/svi/{interface_svi_id}/dhcp-server/{dhcp_server_id}"
    )
    def edit_lan_vpn_interface_svi_parcel_association_with_dhcp_server_parcel(
        self,
        service_id: str,
        lan_vpn_id: str,
        interface_svi_id: str,
        dhcp_server_id: str,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/svi/{interface_svi_id}/dhcp-server/{dhcp_server_id}"
    )
    def delete_lan_vpn_interface_svi_parcel_association_with_dhcp_server_parcel(
        self, service_id: str, lan_vpn_id: str, interface_svi_id: str, dhcp_server_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/tracker")
    def get_tracker_parcels(self, service_id: str) -> ParcelInfo[TrackerParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/tracker")
    def create_tracker_parcel(self, service_id: str, payload: TrackerParcelCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/tracker/{tracker_id}")
    def get_tracker_parcel(self, service_id: str, tracker_id: str) -> Parcel[TrackerParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/tracker/{tracker_id}")
    def edit_tracker_parcel(
        self, service_id: str, tracker_id: str, payload: TrackerParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/tracker/{tracker_id}")
    def delete_tracker_parcel(self, service_id: str, tracker_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/trackergroup")
    def get_tracker_group_parcels(self, service_id: str) -> ParcelInfo[TrackerGroupParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/trackergroup")
    def create_tracker_group_parcel(
        self, service_id: str, payload: TrackerGroupParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/trackergroup/{tracker_group_id}")
    def get_tracker_group_parcel(
        self, service_id: str, tracker_group_id: str
    ) -> Parcel[TrackerGroupParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/trackergroup/{tracker_group_id}")
    def edit_tracker_group_parcel(
        self, service_id: str, tracker_group_id: str, payload: TrackerGroupParcelCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/trackergroup/{tracker_group_id}")
    def delete_tracker_group_parcel(self, service_id: str, tracker_group_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ethernet/{interface_ethernet_id}/tracker"
    )
    def get_tracker_parcels_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str
    ) -> ParcelInfo[TrackerParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/tracker"
    )
    def associate_lan_vpn_interface_ethernet_parcel_with_tracker_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/tracker/{tracker_id}"
    )
    def get_tracker_parcel_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, tracker_id: str
    ) -> Parcel[TrackerParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/tracker/{tracker_id}"
    )
    def edit_lan_vpn_interface_ethernet_parcel_association_with_tracker_parcel(
        self,
        service_id: str,
        lan_vpn_id: str,
        interface_ethernet_id: str,
        tracker_id: str,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/tracker/{tracker_id}"
    )
    def delete_lan_vpn_interface_ethernet_parcel_association_with_tracker_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, tracker_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ipsec/{interface_ipsec_id}/tracker"
    )
    def get_tracker_parcels_associated_with_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str
    ) -> ParcelInfo[TrackerParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ethernet/{interface_ethernet_id}/trackergroup"
    )
    def get_tracker_group_parcels_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str
    ) -> ParcelInfo[TrackerGroupParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/trackergroup"
    )
    def associate_lan_vpn_interface_ethernet_parcel_with_tracker_group_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/trackergroup/{tracker_group_id}"
    )
    def get_tracker_group_parcel_associated_with_lan_vpn_interface_ethernet_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, tracker_group_id: str
    ) -> Parcel[TrackerGroupParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/trackergroup/{tracker_group_id}"
    )
    def edit_lan_vpn_interface_ethernet_parcel_association_with_tracker_group_parcel(
        self,
        service_id: str,
        lan_vpn_id: str,
        interface_ethernet_id: str,
        tracker_group_id: str,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}/"
        "interface/ethernet/{interface_ethernet_id}/trackergroup/{tracker_group_id}"
    )
    def delete_lan_vpn_interface_ethernet_parcel_association_with_tracker_group_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ethernet_id: str, tracker_group_id: str
    ) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/service/{service_id}/lan/vpn/{lan_vpn_id}"
        "/interface/ipsec/{interface_ipsec_id}/trackergroup"
    )
    def get_tracker_group_parcels_associated_with_lan_vpn_interface_ipsec_parcel(
        self, service_id: str, lan_vpn_id: str, interface_ipsec_id: str
    ) -> ParcelInfo[TrackerGroupParcelCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/bgp")
    def get_routing_bgp_parcels(self, service_id: str) -> ParcelInfo[BgpCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/bgp")
    def create_routing_bgp_parcel(self, service_id: str, payload: BgpCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/bgp/{routing_bgp_id}")
    def get_routing_bgp_parcel(self, service_id: str, routing_bgp_id: str) -> Parcel[BgpCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/bgp/{routing_bgp_id}")
    def edit_routing_bgp_parcel(
        self, service_id: str, routing_bgp_id: str, payload: BgpCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/bgp/{routing_bgp_id}")
    def delete_routing_bgp_parcel(self, service_id: str, routing_bgp_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/eigrp")
    def get_routing_eigrp_parcels(self, service_id: str) -> ParcelInfo[EigrpCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/eigrp")
    def create_routing_eigrp_parcel(self, service_id: str, payload: EigrpCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/eigrp/{routing_eigrp_id}")
    def get_routing_eigrp_parcel(self, service_id: str, routing_eigrp_id: str) -> Parcel[EigrpCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/eigrp/{routing_eigrp_id}")
    def edit_routing_eigrp_parcel(
        self, service_id: str, routing_eigrp_id: str, payload: EigrpCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/eigrp/{routing_eigrp_id}")
    def delete_routing_eigrp_parcel(self, service_id: str, routing_eigrp_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/multicast")
    def get_routing_multicast_parcels(self, service_id: str) -> ParcelInfo[MulticastCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/multicast")
    def create_routing_multicast_parcel(
        self, service_id: str, payload: MulticastCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/multicast/{routing_multicast_id}")
    def get_routing_multicast_parcel(
        self, service_id: str, routing_multicast_id: str
    ) -> Parcel[MulticastCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/multicast/{routing_multicast_id}")
    def edit_routing_multicast_parcel(
        self, service_id: str, routing_multicast_id: str, payload: MulticastCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/multicast/{routing_multicast_id}")
    def delete_routing_multicast_parcel(self, service_id: str, routing_multicast_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospf")
    def get_routing_ospf_parcels(self, service_id: str) -> ParcelInfo[OspfCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/ospf")
    def create_routing_ospf_parcel(self, service_id: str, payload: OspfCreationPayload) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospf/{routing_ospf_id}")
    def get_routing_ospf_parcel(self, service_id: str, routing_ospf_id: str) -> Parcel[OspfCreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/ospf/{routing_ospf_id}")
    def edit_routing_ospf_parcel(
        self, service_id: str, routing_ospf_id: str, payload: OspfCreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/ospf/{routing_ospf_id}")
    def delete_routing_ospf_parcel(self, service_id: str, routing_ospf_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv4")
    def get_routing_ospfv3_ipv4_parcels(self, service_id: str) -> ParcelInfo[Ospfv3IPv4CreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv4")
    def create_routing_ospfv3_ipv4_parcel(
        self, service_id: str, payload: Ospfv3IPv4CreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv4/{routing_ospf_id}")
    def get_routing_ospfv3_ipv4_parcel(
        self, service_id: str, routing_ospf_id: str
    ) -> Parcel[Ospfv3IPv4CreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv4/{routing_ospf_id}")
    def edit_routing_ospfv3_ipv4_parcel(
        self, service_id: str, routing_ospf_id: str, payload: Ospfv3IPv4CreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv4/{routing_ospf_id}")
    def delete_routing_ospfv3_ipv4_parcel(self, service_id: str, routing_ospf_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv6")
    def get_routing_ospfv3_ipv6_parcels(self, service_id: str) -> ParcelInfo[Ospfv3IPv6CreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv6")
    def create_routing_ospfv3_ipv6_parcel(
        self, service_id: str, payload: Ospfv3IPv6CreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv6/{routing_ospf_id}")
    def get_routing_ospfv3_ipv6_parcel(
        self, service_id: str, routing_ospf_id: str
    ) -> Parcel[Ospfv3IPv6CreationPayload]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv6/{routing_ospf_id}")
    def edit_routing_ospfv3_ipv6_parcel(
        self, service_id: str, routing_ospf_id: str, payload: Ospfv3IPv6CreationPayload
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{service_id}/routing/ospfv3/ipv6/{routing_ospf_id}")
    def delete_routing_ospfv3_ipv6_parcel(self, service_id: str, routing_ospf_id: str) -> None:
        ...
