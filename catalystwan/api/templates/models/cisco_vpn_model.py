from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.models.cisco_system import ConsoleBaudRate

Role = Literal["primary", "secondary"]


class Dns(BaseModel):
    dns_addr: Optional[str] = Field(
        default=None,
        serialization_alias="dns-addr",
        validation_alias="dns-addr",
        json_schema_extra={"vmanage_key": "dns-addr"},
    )
    role: Role = "primary"
    model_config = ConfigDict(populate_by_name=True)


class DnsIpv6(BaseModel):
    dns_addr: Optional[str] = Field(
        default=None,
        serialization_alias="dns-addr",
        validation_alias="dns-addr",
        json_schema_extra={"vmanage_key": "dns-addr"},
    )
    role: Optional[Role] = "primary"
    model_config = ConfigDict(populate_by_name=True)


class Host(BaseModel):
    hostname: str
    ip: List[str]


SvcType = Literal["FW", "IDS", "IDP", "netsvc1", "netsvc2", "netsvc3", "netsvc4", "TE", "appqoe"]


class Service(BaseModel):
    svc_type: SvcType = Field(
        serialization_alias="svc-type", validation_alias="svc-type", json_schema_extra={"vmanage_key": "svc-type"}
    )
    address: Optional[List[str]] = Field(default=None)
    interface: Optional[str] = Field(default=None)
    track_enable: bool = Field(
        True,
        serialization_alias="track-enable",
        validation_alias="track-enable",
        json_schema_extra={"vmanage_key": "track-enable"},
    )
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("track_enable")
    @classmethod
    def convert_to_string(cls, value):
        return str(value).lower()


ServiceRouteService = Literal["sig"]


class ServiceRoute(BaseModel):
    prefix: str
    vpn: int
    service: ServiceRouteService = "sig"


class NextHop(BaseModel):
    address: Optional[str] = None
    distance: Optional[int] = 1


class NextHopWithTrack(BaseModel):
    address: Optional[str] = None
    distance: Optional[int] = 1
    tracker: str


class Routev4(BaseModel):
    prefix: Optional[str] = None
    next_hop: Optional[List[NextHop]] = Field(
        default=None,
        serialization_alias="next-hop",
        validation_alias="next-hop",
        json_schema_extra={"vmanage_key": "next-hop", "priority_order": ["address", "distance"]},
    )
    next_hop_with_track: Optional[List[NextHopWithTrack]] = Field(
        default=None,
        serialization_alias="next-hop-with-track",
        validation_alias="next-hop-with-track",
        json_schema_extra={"vmanage_key": "next-hop-with-track"},
    )
    null0: Optional[bool] = None
    distance: Optional[int] = None
    vpn: Optional[int] = None
    dhcp: Optional[bool] = None
    model_config = ConfigDict(populate_by_name=True)


class NextHopv6(BaseModel):
    address: str
    distance: Optional[int] = 1


Nat = Literal["NAT64", "NAT66"]


class Routev6(BaseModel):
    prefix: str
    next_hop: Optional[List[NextHopv6]] = Field(
        default=None,
        serialization_alias="next-hop",
        validation_alias="next-hop",
        json_schema_extra={"vmanage_key": "next-hop"},
    )
    null0: Optional[bool] = None
    vpn: Optional[int] = None
    nat: Optional[Nat] = None
    model_config = ConfigDict(populate_by_name=True)


class GreRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[str]] = None


class IpsecRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[str]] = None


AdvertiseProtocol = Literal["bgp", "ospf", "connected", "static", "network", "aggregate", "eigrp", "lisp", "isis"]
AdvertiseProtocolSubType = Literal["external"]
Region = Literal["core", "access"]


class PrefixList(BaseModel):
    prefix_entry: str = Field(
        serialization_alias="prefix-entry",
        validation_alias="prefix-entry",
        json_schema_extra={"vmanage_key": "prefix-entry"},
    )
    aggregate_only: Optional[bool] = Field(
        default=None,
        serialization_alias="aggregate-only",
        validation_alias="aggregate-only",
        json_schema_extra={"vmanage_key": "aggregate-only"},
    )
    region: Optional[Region]
    model_config = ConfigDict(populate_by_name=True)


class Advertise(BaseModel):
    protocol: AdvertiseProtocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    protocol_sub_type: Optional[List[AdvertiseProtocolSubType]] = Field(
        default=None,
        serialization_alias="protocol-sub-type",
        validation_alias="protocol-sub-type",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    prefix_list: Optional[List[PrefixList]] = Field(
        default=None,
        serialization_alias="prefix-list",
        validation_alias="prefix-list",
        json_schema_extra={"vmanage_key": "prefix-list"},
    )
    model_config = ConfigDict(populate_by_name=True)


Ipv6AdvertiseProtocol = Literal["bgp", "ospf", "connected", "static", "network", "aggregate"]
Ipv6AdvertiseProtocolSubType = Literal["external"]


class Ipv6Advertise(BaseModel):
    protocol: Ipv6AdvertiseProtocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    protocol_sub_type: Optional[List[Ipv6AdvertiseProtocolSubType]] = Field(
        default=None,
        serialization_alias="protocol-sub-type",
        validation_alias="protocol-sub-type",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    prefix_list: Optional[List[PrefixList]] = Field(
        default=None,
        serialization_alias="prefix-list",
        validation_alias="prefix-list",
        json_schema_extra={"vmanage_key": "prefix-list"},
    )
    model_config = ConfigDict(populate_by_name=True)


LeakFromGlobalProtocol = Literal["all", "static", "mobile", "connected", "rip", "odr"]


class Pool(BaseModel):
    name: str
    start_address: str = Field(
        serialization_alias="start-address",
        validation_alias="start-address",
        json_schema_extra={"vmanage_key": "start-address"},
    )
    end_address: str = Field(
        serialization_alias="end-address",
        validation_alias="end-address",
        json_schema_extra={"vmanage_key": "end-address"},
    )
    overload: Optional[bool] = None
    leak_from_global: bool
    leak_from_global_protocol: LeakFromGlobalProtocol
    leak_to_global: bool
    model_config = ConfigDict(populate_by_name=True)


Direction = Literal["inside", "outside"]
Overload = Literal["true", "false"]


class Natpool(BaseModel):
    name: int
    prefix_length: Optional[int] = Field(
        default=None,
        serialization_alias="prefix-length",
        validation_alias="prefix-length",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    range_start: Optional[str] = Field(
        default=None,
        serialization_alias="range-start",
        validation_alias="range-start",
        json_schema_extra={"vmanage_key": "range-start"},
    )
    range_end: Optional[str] = Field(
        default=None,
        serialization_alias="range-end",
        validation_alias="range-end",
        json_schema_extra={"vmanage_key": "range-end"},
    )
    overload: Optional[Overload] = "true"
    direction: Direction
    tracker_id: Optional[int] = Field(
        default=None,
        serialization_alias="tracker-id",
        validation_alias="tracker-id",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


StaticNatDirection = Literal["inside", "outside"]


class Static(BaseModel):
    pool_name: Optional[int] = Field(
        default=None,
        serialization_alias="pool-name",
        validation_alias="pool-name",
        json_schema_extra={"vmanage_key": "pool-name"},
    )
    source_ip: Optional[str] = Field(
        default=None,
        serialization_alias="source-ip",
        validation_alias="source-ip",
        json_schema_extra={"vmanage_key": "source-ip"},
    )
    translate_ip: Optional[str] = Field(
        default=None,
        serialization_alias="translate-ip",
        validation_alias="translate-ip",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    static_nat_direction: StaticNatDirection = Field(
        serialization_alias="static-nat-direction",
        validation_alias="static-nat-direction",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    tracker_id: Optional[int] = Field(
        default=None,
        serialization_alias="tracker-id",
        validation_alias="tracker-id",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


class SubnetStatic(BaseModel):
    source_ip_subnet: str = Field(
        serialization_alias="source-ip-subnet",
        validation_alias="source-ip-subnet",
        json_schema_extra={"vmanage_key": "source-ip-subnet"},
    )
    translate_ip_subnet: str = Field(
        serialization_alias="translate-ip-subnet",
        validation_alias="translate-ip-subnet",
        json_schema_extra={"vmanage_key": "translate-ip-subnet"},
    )
    prefix_length: int = Field(
        serialization_alias="prefix-length",
        validation_alias="prefix-length",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    static_nat_direction: StaticNatDirection = Field(
        serialization_alias="static-nat-direction",
        validation_alias="static-nat-direction",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    tracker_id: Optional[int] = Field(
        default=None,
        serialization_alias="tracker-id",
        validation_alias="tracker-id",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


Proto = Literal["tcp", "udp"]


class PortForward(BaseModel):
    pool_name: Optional[int] = Field(
        default=None,
        serialization_alias="pool-name",
        validation_alias="pool-name",
        json_schema_extra={"vmanage_key": "pool-name"},
    )
    source_port: int = Field(
        serialization_alias="source-port",
        validation_alias="source-port",
        json_schema_extra={"vmanage_key": "source-port"},
    )
    translate_port: int = Field(
        serialization_alias="translate-port",
        validation_alias="translate-port",
        json_schema_extra={"vmanage_key": "translate-port"},
    )
    source_ip: str = Field(
        serialization_alias="source-ip", validation_alias="source-ip", json_schema_extra={"vmanage_key": "source-ip"}
    )
    translate_ip: str = Field(
        serialization_alias="translate-ip",
        validation_alias="translate-ip",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    proto: Proto
    model_config = ConfigDict(populate_by_name=True)


RouteImportProtocol = Literal["static", "connected", "bgp", "ospf"]
RouteImportProtocolSubType = Literal["external"]
RouteImportRedistributeProtocol = Literal["bgp", "ospf", "eigrp"]


class RouteImportRedistribute(BaseModel):
    protocol: RouteImportRedistributeProtocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteImport(BaseModel):
    protocol: RouteImportProtocol
    protocol_sub_type: List[RouteImportProtocolSubType] = Field(
        serialization_alias="protocol-sub-type",
        validation_alias="protocol-sub-type",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteImportRedistribute]] = None
    model_config = ConfigDict(populate_by_name=True)


RouteImportFromProtocol = Literal["static", "connected", "bgp", "ospf", "eigrp"]
RouteImportFromProtocolSubType = Literal["external"]
RouteImportFromRedistributeProtocol = Literal["bgp", "ospf", "eigrp"]


class RouteImportFromRedistribute(BaseModel):
    protocol: RouteImportFromRedistributeProtocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteImportFrom(BaseModel):
    source_vpn: int = Field(
        serialization_alias="source_vpn", validation_alias="source_vpn", json_schema_extra={"vmanage_key": "source-vpn"}
    )
    protocol: RouteImportFromProtocol
    protocol_sub_type: List[RouteImportFromProtocolSubType] = Field(
        serialization_alias="protocol-sub-type",
        validation_alias="protocol-sub-type",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteImportFromRedistribute]] = None
    model_config = ConfigDict(populate_by_name=True)


RouteExportProtocol = Literal["static", "connected", "bgp", "ospf", "eigrp"]
RouteExportProtocolSubType = Literal["external"]
RouteExportRedistributeProtocol = Literal["bgp", "ospf"]


class RouteExportRedistribute(BaseModel):
    protocol: RouteExportRedistributeProtocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteExport(BaseModel):
    protocol: RouteExportProtocol
    protocol_sub_type: List[RouteExportProtocolSubType] = Field(
        serialization_alias="protocol-sub-type",
        validation_alias="protocol-sub-type",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteExportRedistribute]]
    model_config = ConfigDict(populate_by_name=True)


class CiscoVPNModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn_id: int = Field(
        default=0, serialization_alias="vpn-id", validation_alias="vpn-id", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    vpn_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "name"})
    tenant_vpn_id: Optional[int] = Field(
        default=None,
        serialization_alias="tenant-vpn-id",
        validation_alias="tenant-vpn-id",
        json_schema_extra={"vmanage_key": "tenant-vpn-id"},
    )
    org_name: Optional[str] = Field(
        default=None,
        serialization_alias="org-name",
        validation_alias="org-name",
        json_schema_extra={"vmanage_key": "org-name"},
    )
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None,
        serialization_alias="omp-admin-distance-ipv4",
        validation_alias="omp-admin-distance-ipv4",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"},
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None,
        serialization_alias="omp-admin-distance-ipv6",
        validation_alias="omp-admin-distance-ipv6",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"},
    )
    dns: Optional[List[Dns]] = None
    dns_ipv6: Optional[List[DnsIpv6]] = Field(
        default=None,
        serialization_alias="dns-ipv6",
        validation_alias="dns-ipv6",
        json_schema_extra={"vmanage_key": "dns-ipv6"},
    )
    layer4: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["ecmp-hash-key"]})
    host: Optional[List[Host]] = Field(default=None, json_schema_extra={"priority_order": ["hostname", "ip"]})
    service: Optional[List[Service]] = None
    service_route: Optional[List[ServiceRoute]] = Field(
        default=None,
        serialization_alias="service-route",
        validation_alias="service-route",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "service-route"},
    )
    route_v4: Optional[List[Routev4]] = Field(
        default=None,
        serialization_alias="route",
        validation_alias="route",
        json_schema_extra={
            "data_path": ["ip"],
            "vmanage_key": "route",
            "priority_order": ["prefix", "next-hop", "next-hop-with-track"],
        },
    )
    route_v6: Optional[List[Routev6]] = Field(
        default=None, json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "route"}
    )
    gre_route: Optional[List[GreRoute]] = Field(
        default=None,
        serialization_alias="gre-route",
        validation_alias="gre-route",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "gre-route"},
    )
    ipsec_route: Optional[List[IpsecRoute]] = Field(
        default=None,
        serialization_alias="ipsec-route",
        validation_alias="ipsec-route",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "ipsec-route"},
    )
    advertise: Optional[List[Advertise]] = Field(default=None, json_schema_extra={"data_path": ["omp"]})
    ipv6_advertise: Optional[List[Ipv6Advertise]] = Field(
        default=None,
        serialization_alias="ipv6-advertise",
        validation_alias="ipv6-advertise",
        json_schema_extra={"data_path": ["omp"], "vmanage_key": "ipv6-advertise"},
    )
    pool: Optional[List[Pool]] = Field(default=None, json_schema_extra={"data_path": ["nat64", "v4"]})
    natpool: Optional[List[Natpool]] = Field(default=None, json_schema_extra={"data_path": ["nat"]})
    static: Optional[List[Static]] = Field(default=None, json_schema_extra={"data_path": ["nat"]})
    subnet_static: Optional[List[SubnetStatic]] = Field(
        default=None,
        serialization_alias="subnet-static",
        validation_alias="subnet-static",
        json_schema_extra={"data_path": ["nat"], "vmanage_key": "subnet-static"},
    )
    port_forward: Optional[List[PortForward]] = Field(
        default=None,
        serialization_alias="port-forward",
        validation_alias="port-forward",
        json_schema_extra={"data_path": ["nat"], "vmanage_key": "port-forward"},
    )
    route_import: Optional[List[RouteImport]] = Field(
        default=None,
        serialization_alias="route-import",
        validation_alias="route-import",
        json_schema_extra={"vmanage_key": "route-import"},
    )
    route_import_from: Optional[List[RouteImportFrom]] = Field(
        default=None,
        serialization_alias="route-import-from",
        validation_alias="route-import-from",
        json_schema_extra={"vmanage_key": "route-import-from"},
    )
    route_export: Optional[List[RouteExport]] = Field(
        default=None,
        serialization_alias="route-export",
        validation_alias="route-export",
        json_schema_extra={"vmanage_key": "route-export"},
    )
    tunnels_bandwidth: Optional[int] = Field(
        default=None,
        serialization_alias="tunnels-bandwidth",
        validation_alias="tunnels-bandwidth",
        json_schema_extra={"vmanage_key": "tunnels-bandwidth"},
    )
    console_baud_rate: Optional[ConsoleBaudRate] = Field(
        default=None,
        serialization_alias="console-baud-rate",
        validation_alias="console-baud-rate",
        json_schema_extra={"vmanage_key": "console-baud-rate"},
    )
    control_connections: Optional[bool] = Field(
        default=None,
        serialization_alias="control-connections",
        validation_alias="control-connections",
        json_schema_extra={"vmanage_key": "control-connections", "data_path": ["tunnel-interface"]},
    )
    vmanage_connection_preference: Optional[int] = Field(
        default=None,
        validation_alias="vmanage-connection-preference",
        serialization_alias="vmanage-connection-preference",
        json_schema_extra={"vmanage_key": "vmanage-connection-preference", "data_path": ["tunnel-interface"]},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn"

    def generate_vpn_id(self, session):
        if self.vpn_id not in [0, 512]:
            payload = {"resourcePoolDataType": "vpn", "tenantId": self.org_name, "tenantVpn": self.vpn_id}
            url = "/dataservice/resourcepool/resource/vpn"
            response = session.put(url=url, json=payload).json()
            self.vpn_id = response["deviceVpn"]
