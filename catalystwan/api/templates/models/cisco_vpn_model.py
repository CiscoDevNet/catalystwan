# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field, field_validator

from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class Role(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Dns(FeatureTemplateValidator):
    dns_addr: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "dns-addr"})
    role: Role = Role.PRIMARY
    model_config = ConfigDict(populate_by_name=True)


class DnsIpv6(FeatureTemplateValidator):
    dns_addr: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "dns-addr"})
    role: Optional[Role] = Role.PRIMARY
    model_config = ConfigDict(populate_by_name=True)


class Host(FeatureTemplateValidator):
    hostname: str
    ip: List[str]


class SvcType(str, Enum):
    FW = "FW"
    IDS = "IDS"
    IDP = "IDP"
    NETSVC1 = "netsvc1"
    NETSVC2 = "netsvc2"
    NETSVC3 = "netsvc3"
    NETSVC4 = "netsvc4"
    TE = "TE"
    APPQOE = "appqoe"


class Service(FeatureTemplateValidator):
    svc_type: SvcType = Field(json_schema_extra={"vmanage_key": "svc-type"})
    address: Optional[List[str]] = None
    interface: Optional[str] = None
    track_enable: bool = Field(True, json_schema_extra={"vmanage_key": "track-enable"})
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("track_enable")
    @classmethod
    def convert_to_string(cls, value):
        return str(value).lower()


class ServiceRouteService(str, Enum):
    SIG = "sig"


class ServiceRoute(FeatureTemplateValidator):
    prefix: str
    vpn: int
    service: ServiceRouteService = ServiceRouteService.SIG


class NextHop(FeatureTemplateValidator):
    address: Optional[str] = None
    distance: Optional[int] = 1


class NextHopWithTrack(FeatureTemplateValidator):
    address: Optional[str] = None
    distance: Optional[int] = 1
    tracker: str


class Routev4(FeatureTemplateValidator):
    prefix: Optional[str] = None
    next_hop: Optional[List[NextHop]] = Field(
        default=None, json_schema_extra={"vmanage_key": "next-hop", "priority_order": ["address", "distance"]}
    )
    next_hop_with_track: Optional[List[NextHopWithTrack]] = Field(
        default=None, json_schema_extra={"vmanage_key": "next-hop-with-track"}
    )
    null0: Optional[bool] = None
    distance: Optional[int] = None
    vpn: Optional[int] = None
    dhcp: Optional[bool] = None
    model_config = ConfigDict(populate_by_name=True)


class NextHopv6(FeatureTemplateValidator):
    address: str
    distance: Optional[int] = 1


class Nat(str, Enum):
    NAT64 = "NAT64"
    NAT66 = "NAT66"


class Routev6(FeatureTemplateValidator):
    prefix: str
    next_hop: Optional[List[NextHopv6]] = Field(default=None, json_schema_extra={"vmanage_key": "next-hop"})
    null0: Optional[bool] = None
    vpn: Optional[int] = None
    nat: Optional[Nat] = None
    model_config = ConfigDict(populate_by_name=True)


class GreRoute(FeatureTemplateValidator):
    prefix: str
    vpn: int
    interface: Optional[List[str]] = None


class IpsecRoute(FeatureTemplateValidator):
    prefix: str
    vpn: int
    interface: Optional[List[str]] = None


class AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    OSPFV3 = "ospfv3"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"
    EIGRP = "eigrp"
    LISP = "lisp"
    ISIS = "isis"


class AdvertiseProtocolSubType(str, Enum):
    EXTERNAL = "external"


class Region(str, Enum):
    CORE = "core"
    ACCESS = "access"


class PrefixList(FeatureTemplateValidator):
    prefix_entry: str = Field(json_schema_extra={"vmanage_key": "prefix-entry"})
    aggregate_only: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "aggregate-only"})
    region: Optional[Region]
    model_config = ConfigDict(populate_by_name=True)


class Advertise(FeatureTemplateValidator):
    protocol: AdvertiseProtocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    protocol_sub_type: Optional[List[AdvertiseProtocolSubType]] = Field(
        default=None, json_schema_extra={"vmanage_key": "protocol-sub-type"}
    )
    prefix_list: Optional[List[PrefixList]] = Field(default=None, json_schema_extra={"vmanage_key": "prefix-list"})
    model_config = ConfigDict(populate_by_name=True)


class Ipv6AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"


class Ipv6AdvertiseProtocolSubType(str, Enum):
    EXTERNAL = "external"


class Ipv6Advertise(FeatureTemplateValidator):
    protocol: Ipv6AdvertiseProtocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    protocol_sub_type: Optional[List[Ipv6AdvertiseProtocolSubType]] = Field(
        default=None, json_schema_extra={"vmanage_key": "protocol-sub-type"}
    )
    prefix_list: Optional[List[PrefixList]] = Field(default=None, json_schema_extra={"vmanage_key": "prefix-list"})
    model_config = ConfigDict(populate_by_name=True)


class LeakFromGlobalProtocol(str, Enum):
    ALL = "all"
    STATIC = "static"
    MOBILE = "mobile"
    CONNECTED = "connected"
    RIP = "rip"
    ODR = "odr"


class Pool(FeatureTemplateValidator):
    name: str
    start_address: str = Field(json_schema_extra={"vmanage_key": "start-address"})
    end_address: str = Field(json_schema_extra={"vmanage_key": "end-address"})
    overload: Optional[bool] = None
    leak_from_global: bool
    leak_from_global_protocol: LeakFromGlobalProtocol
    leak_to_global: bool
    model_config = ConfigDict(populate_by_name=True)


class Direction(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Overload(str, Enum):
    TRUE = "true"
    FALSE = "false"


class Natpool(FeatureTemplateValidator):
    name: int
    prefix_length: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "prefix-length"})
    range_start: str = Field(default=None, json_schema_extra={"vmanage_key": "range-start"})
    range_end: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "range-end"})
    overload: Overload = Overload.TRUE
    direction: Direction
    tracker_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tracker-id"})
    model_config = ConfigDict(populate_by_name=True)


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Static(FeatureTemplateValidator):
    pool_name: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "pool-name"})
    source_ip: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "source-ip"})
    translate_ip: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "translate-ip"})
    static_nat_direction: StaticNatDirection = Field(json_schema_extra={"vmanage_key": "static-nat-direction"})
    tracker_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tracker-id"})
    model_config = ConfigDict(populate_by_name=True)


class SubnetStatic(FeatureTemplateValidator):
    source_ip_subnet: str = Field(json_schema_extra={"vmanage_key": "source-ip-subnet"})
    translate_ip_subnet: str = Field(json_schema_extra={"vmanage_key": "translate-ip-subnet"})
    prefix_length: int = Field(json_schema_extra={"vmanage_key": "prefix-length"})
    static_nat_direction: StaticNatDirection = Field(json_schema_extra={"vmanage_key": "static-nat-direction"})
    tracker_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tracker-id"})
    model_config = ConfigDict(populate_by_name=True)


class Proto(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class PortForward(FeatureTemplateValidator):
    pool_name: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "pool-name"})
    source_port: int = Field(json_schema_extra={"vmanage_key": "source-port"})
    translate_port: int = Field(json_schema_extra={"vmanage_key": "translate-port"})
    source_ip: str = Field(json_schema_extra={"vmanage_key": "source-ip"})
    translate_ip: str = Field(json_schema_extra={"vmanage_key": "translate-ip"})
    proto: Proto
    model_config = ConfigDict(populate_by_name=True)


class RouteImportProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"


class RouteImportProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RouteImportRedistributeProtocol(str, Enum):
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class RouteImportRedistribute(FeatureTemplateValidator):
    protocol: RouteImportRedistributeProtocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class RouteImport(FeatureTemplateValidator):
    protocol: RouteImportProtocol
    protocol_sub_type: List[RouteImportProtocolSubType] = Field(json_schema_extra={"vmanage_key": "protocol-sub-type"})
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    redistribute: Optional[List[RouteImportRedistribute]] = None
    model_config = ConfigDict(populate_by_name=True)


class RouteImportFromProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"
    EIGRP = "eigrp"


class RouteImportFromProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RouteImportFromRedistributeProtocol(str, Enum):
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class RouteImportFromRedistribute(FeatureTemplateValidator):
    protocol: RouteImportFromRedistributeProtocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class RouteImportFrom(FeatureTemplateValidator):
    source_vpn: int = Field(json_schema_extra={"vmanage_key": "source-vpn"})
    protocol: RouteImportFromProtocol
    protocol_sub_type: List[RouteImportFromProtocolSubType] = Field(
        json_schema_extra={"vmanage_key": "protocol-sub-type"}
    )
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    redistribute: Optional[List[RouteImportFromRedistribute]] = None
    model_config = ConfigDict(populate_by_name=True)


class RouteExportProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class RouteExportProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RouteExportRedistributeProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"


class RouteExportRedistribute(FeatureTemplateValidator):
    protocol: RouteExportRedistributeProtocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class RouteExport(FeatureTemplateValidator):
    protocol: RouteExportProtocol
    protocol_sub_type: List[RouteExportProtocolSubType] = Field(json_schema_extra={"vmanage_key": "protocol-sub-type"})
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    redistribute: Optional[List[RouteExportRedistribute]]
    model_config = ConfigDict(populate_by_name=True)


class CiscoVPNModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn_id: int = Field(default=0, json_schema_extra={"vmanage_key": "vpn-id"})
    vpn_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "name"})
    tenant_vpn_id: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tenant-vpn-id"})
    org_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "org-name"})
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"}
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"}
    )
    dns: Optional[List[Dns]] = None
    dns_ipv6: Optional[List[DnsIpv6]] = Field(default=None, json_schema_extra={"vmanage_key": "dns-ipv6"})
    layer4: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["ecmp-hash-key"]})
    host: Optional[List[Host]] = Field(default=None, json_schema_extra={"priority_order": ["hostname", "ip"]})
    service: Optional[List[Service]] = None
    service_route: Optional[List[ServiceRoute]] = Field(
        default=None, json_schema_extra={"data_path": ["ip"], "vmanage_key": "service-route"}
    )
    route_v4: Optional[List[Routev4]] = Field(
        default=None,
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
        default=None, json_schema_extra={"data_path": ["ip"], "vmanage_key": "gre-route"}
    )
    ipsec_route: Optional[List[IpsecRoute]] = Field(
        default=None, json_schema_extra={"data_path": ["ip"], "vmanage_key": "ipsec-route"}
    )
    advertise: Optional[List[Advertise]] = Field(default=None, json_schema_extra={"data_path": ["omp"]})
    ipv6_advertise: Optional[List[Ipv6Advertise]] = Field(
        default=None, json_schema_extra={"data_path": ["omp"], "vmanage_key": "ipv6-advertise"}
    )
    pool: Optional[List[Pool]] = Field(default=None, json_schema_extra={"data_path": ["nat64", "v4"]})
    natpool: Optional[List[Natpool]] = Field(default=None, json_schema_extra={"data_path": ["nat"]})
    static: Optional[List[Static]] = Field(default=None, json_schema_extra={"data_path": ["nat"]})
    subnet_static: Optional[List[SubnetStatic]] = Field(
        default=None, json_schema_extra={"data_path": ["nat"], "vmanage_key": "subnet-static"}
    )
    port_forward: Optional[List[PortForward]] = Field(
        default=None, json_schema_extra={"data_path": ["nat"], "vmanage_key": "port-forward"}
    )
    route_import: Optional[List[RouteImport]] = Field(default=None, json_schema_extra={"vmanage_key": "route-import"})
    route_import_from: Optional[List[RouteImportFrom]] = Field(
        default=None, json_schema_extra={"vmanage_key": "route-import-from"}
    )
    route_export: Optional[List[RouteExport]] = Field(default=None, json_schema_extra={"vmanage_key": "route-export"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn"

    def generate_vpn_id(self, session):
        if self.vpn_id not in [0, 512]:
            payload = {"resourcePoolDataType": "vpn", "tenantId": self.org_name, "tenantVpn": self.vpn_id}
            url = "/dataservice/resourcepool/resource/vpn"
            response = session.put(url=url, json=payload).json()
            self.vpn_id = response["deviceVpn"]
