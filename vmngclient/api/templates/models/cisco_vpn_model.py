from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.api.templates.feature_template import FeatureTemplate


class Role(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Dns(BaseModel):
    dns_addr: str = Field(alias="dns-addr")
    role: Role = Role.PRIMARY

    class Config:
        allow_population_by_field_name = True


class DnsIpv6(BaseModel):
    dns_addr: str = Field(alias="dns-addr")
    role: Optional[Role] = Role.PRIMARY

    class Config:
        allow_population_by_field_name = True


class Host(BaseModel):
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


class Service(BaseModel):
    svc_type: SvcType = Field(alias="svc-type")
    address: List[str]
    interface: str
    track_enable: bool = Field(True, alias="track-enable")

    class Config:
        allow_population_by_field_name = True

    @validator("track_enable")
    def convert_to_string(cls, value):
        return str(value).lower()


class ServiceRouteService(str, Enum):
    SIG = "sig"


class ServiceRoute(BaseModel):
    prefix: str
    vpn: int
    service: ServiceRouteService = ServiceRouteService.SIG


class NextHop(BaseModel):
    address: str
    distance: Optional[int] = 1


class NextHopWithTrack(BaseModel):
    address: str
    distance: Optional[int] = 1
    tracker: str


class Routev4(BaseModel):
    prefix: str
    next_hop: Optional[List[NextHop]] = Field(alias="next-hop")
    next_hop_with_track: Optional[List[NextHopWithTrack]] = Field(alias="next-hop-with-track")
    null0: Optional[bool]
    distance: Optional[int] = 1
    vpn: Optional[int]
    dhcp: Optional[bool]

    class Config:
        allow_population_by_field_name = True


class NextHopv6(BaseModel):
    address: str
    distance: Optional[int] = 1


class Nat(str, Enum):
    NAT64 = "NAT64"
    NAT66 = "NAT66"


class Routev6(BaseModel):
    prefix: str
    next_hop: Optional[List[NextHopv6]] = Field(alias="next-hop")
    null0: Optional[bool]
    vpn: Optional[int]
    nat: Optional[Nat]

    class Config:
        allow_population_by_field_name = True


class GreRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[str]]


class IpsecRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[str]]


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


class PrefixList(BaseModel):
    prefix_entry: str = Field(alias="prefix-entry")
    aggregate_only: Optional[bool] = Field(alias="aggregate-only")
    region: Optional[Region]

    class Config:
        allow_population_by_field_name = True


class Advertise(BaseModel):
    protocol: AdvertiseProtocol
    route_policy: Optional[str] = Field(alias="route-policy")
    protocol_sub_type: Optional[List[AdvertiseProtocolSubType]] = Field(alias="protocol-sub-type")
    prefix_list: Optional[List[PrefixList]] = Field(alias="prefix-list")

    class Config:
        allow_population_by_field_name = True


class Ipv6AdvertiseProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"


class Ipv6AdvertiseProtocolSubType(str, Enum):
    EXTERNAL = "external"


class Ipv6Advertise(BaseModel):
    protocol: Ipv6AdvertiseProtocol
    route_policy: Optional[str] = Field(alias="route-policy")
    protocol_sub_type: Optional[List[Ipv6AdvertiseProtocolSubType]] = Field(alias="protocol-sub-type")
    prefix_list: Optional[List[PrefixList]] = Field(alias="prefix-list")

    class Config:
        allow_population_by_field_name = True


class LeakFromGlobalProtocol(str, Enum):
    ALL = "all"
    STATIC = "static"
    MOBILE = "mobile"
    CONNECTED = "connected"
    RIP = "rip"
    ODR = "odr"


class Pool(BaseModel):
    name: str
    start_address: str = Field(alias="start-address")
    end_address: str = Field(alias="end-address")
    overload: Optional[bool]
    leak_from_global: bool
    leak_from_global_protocol: LeakFromGlobalProtocol
    leak_to_global: bool

    class Config:
        allow_population_by_field_name = True


class Direction(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Overload(str, Enum):
    TRUE = "true"
    FALSE = "false"


class Natpool(BaseModel):
    name: int
    prefix_length: int = Field(alias="prefix-length")
    range_start: str = Field(alias="range-start")
    range_end: str = Field(alias="range-end")
    overload: Overload = Overload.TRUE
    direction: Direction
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Static(BaseModel):
    pool_name: Optional[int] = Field(alias="pool-name")
    source_ip: str = Field(alias="source-ip")
    translate_ip: str = Field(alias="translate-ip")
    static_nat_direction: StaticNatDirection = Field(alias="static-nat-direction")
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class SubnetStatic(BaseModel):
    source_ip_subnet: str = Field(alias="source-ip-subnet")
    translate_ip_subnet: str = Field(alias="translate-ip-subnet")
    prefix_length: int = Field(alias="prefix-length")
    static_nat_direction: StaticNatDirection = Field(alias="static-nat-direction")
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class Proto(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class PortForward(BaseModel):
    pool_name: Optional[int] = Field(alias="pool-name")
    source_port: int = Field(alias="source-port")
    translate_port: int = Field(alias="translate-port")
    source_ip: str = Field(alias="source-ip")
    translate_ip: str = Field(alias="translate-ip")
    proto: Proto

    class Config:
        allow_population_by_field_name = True


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


class RouteImportRedistribute(BaseModel):
    protocol: RouteImportRedistributeProtocol
    route_policy: Optional[str] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteImport(BaseModel):
    protocol: RouteImportProtocol
    protocol_sub_type: List[RouteImportProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[str] = Field(alias="route-policy")
    redistribute: Optional[List[RouteImportRedistribute]]

    class Config:
        allow_population_by_field_name = True


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


class RouteImportFromRedistribute(BaseModel):
    protocol: RouteImportFromRedistributeProtocol
    route_policy: Optional[str] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteImportFrom(BaseModel):
    source_vpn: int = Field(alias="source-vpn")
    protocol: RouteImportFromProtocol
    protocol_sub_type: List[RouteImportFromProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[str] = Field(alias="route-policy")
    redistribute: Optional[List[RouteImportFromRedistribute]]

    class Config:
        allow_population_by_field_name = True


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


class RouteExportRedistribute(BaseModel):
    protocol: RouteExportRedistributeProtocol
    route_policy: Optional[str] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteExport(BaseModel):
    protocol: RouteExportProtocol
    protocol_sub_type: List[RouteExportProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[str] = Field(alias="route-policy")
    redistribute: Optional[List[RouteExportRedistribute]]

    class Config:
        allow_population_by_field_name = True


class CiscoVPNModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    vpn_id: int = Field(alias="vpn-id", default=0)
    vpn_name: Optional[str] = Field(alias="name")
    tenant_vpn_id: Optional[int] = Field(alias="tenant-vpn-id")
    org_name: Optional[str] = Field(alias="org-name")
    omp_admin_distance_ipv4: Optional[int] = Field(alias="omp-admin-distance-ipv4")
    omp_admin_distance_ipv6: Optional[int] = Field(alias="omp-admin-distance-ipv6")
    dns: Optional[List[Dns]]
    dns_ipv6: Optional[List[DnsIpv6]] = Field(alias="dns-ipv6")
    layer4: Optional[bool] = Field(data_path=["ecmp-hash-key"])
    host: Optional[List[Host]]
    service: Optional[List[Service]]
    service_route: Optional[List[ServiceRoute]] = Field(data_path=["ip"], alias="service-route")
    route_v4: Optional[List[Routev4]] = Field(data_path=["ip"], alias="route")
    route_v6: Optional[List[Routev6]] = Field(data_path=["ipv6"], alias="route")
    gre_route: Optional[List[GreRoute]] = Field(data_path=["ip"], alias="gre-route")
    ipsec_route: Optional[List[IpsecRoute]] = Field(data_path=["ip"], alias="ipsec-route")
    advertise: Optional[List[Advertise]] = Field(data_path=["omp"])
    ipv6_advertise: Optional[List[Ipv6Advertise]] = Field(data_path=["omp"], alias="ipv6-advertise")
    pool: Optional[List[Pool]] = Field(data_path=["nat64", "v4"])
    natpool: Optional[List[Natpool]] = Field(data_path=["nat"])
    static: Optional[List[Static]] = Field(data_path=["nat"])
    subnet_static: Optional[List[SubnetStatic]] = Field(data_path=["nat"], alias="subnet-static")
    port_forward: Optional[List[PortForward]] = Field(data_path=["nat"], alias="port-forward")
    route_import: Optional[List[RouteImport]] = Field(alias="route-import")
    route_import_from: Optional[List[RouteImportFrom]] = Field(alias="route-import-from")
    route_export: Optional[List[RouteExport]] = Field(alias="route-export")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn"
