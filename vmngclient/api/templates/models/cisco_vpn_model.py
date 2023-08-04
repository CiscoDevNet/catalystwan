from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate


class Role(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


class Dns(BaseModel):
    dns_addr: str = Field(alias="dns-addr")
    role: Optional[Role] = Role.PRIMARY

    class Config:
        allow_population_by_field_name = True


class Role(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"


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
    track_enable: Optional[bool] = Field(True, alias="track-enable")

    class Config:
        allow_population_by_field_name = True


class Service(str, Enum):
    SIG = "sig"


class ServiceRoute(BaseModel):
    prefix: str
    vpn: int
    service: Service


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


class NextHop(BaseModel):
    address: str
    distance: Optional[int] = 1


class Nat(str, Enum):
    NAT64 = "NAT64"
    NAT66 = "NAT66"


class Routev6(BaseModel):
    prefix: str
    next_hop: Optional[List[NextHop]] = Field(alias="next-hop")
    null0: Optional[bool]
    vpn: Optional[int]
    nat: Nat

    class Config:
        allow_population_by_field_name = True


class GreRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[str]]


class IpsecRoute(BaseModel):
    prefix: str
    vpn: int
    interface: Optional[List[List]]


class Protocol(str, Enum):
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


class ProtocolSubType(str, Enum):
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
    protocol: Protocol
    route_policy: Optional[str] = Field(alias="route-policy")
    protocol_sub_type: Optional[List[ProtocolSubType]] = Field(alias="protocol-sub-type")
    prefix_list: Optional[List[PrefixList]] = Field(alias="prefix-list")

    class Config:
        allow_population_by_field_name = True


class Protocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"


class ProtocolSubType(str, Enum):
    EXTERNAL = "external"


class Region(str, Enum):
    CORE = "core"
    ACCESS = "access"


class PrefixList(BaseModel):
    prefix_entry: str = Field(alias="prefix-entry")
    aggregate_only: Optional[bool] = Field(alias="aggregate-only")
    region: Region

    class Config:
        allow_population_by_field_name = True


class Ipv6Advertise(BaseModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(alias="route-policy")
    protocol_sub_type: Optional[List[ProtocolSubType]] = Field(alias="protocol-sub-type")
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


class Natpool(BaseModel):
    name: int
    prefix_length: int = Field(alias="prefix-length")
    range_start: str = Field(alias="range-start")
    range_end: str = Field(alias="range-end")
    overload: Optional[bool] = True
    direction: Direction
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class PoolName(str, Enum):
    pass


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Static(BaseModel):
    pool_name: Optional[PoolName] = Field(alias="pool-name")
    source_ip: str = Field(alias="source-ip")
    translate_ip: str = Field(alias="translate-ip")
    static_nat_direction: StaticNatDirection = Field(alias="static-nat-direction")
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class SubnetStatic(BaseModel):
    source_ip_subnet: str = Field(alias="source-ip-subnet")
    translate_ip_subnet: str = Field(alias="translate-ip-subnet")
    prefix_length: int = Field(alias="prefix-length")
    static_nat_direction: StaticNatDirection = Field(alias="static-nat-direction")
    tracker_id: Optional[int] = Field(alias="tracker-id")

    class Config:
        allow_population_by_field_name = True


class PoolName(str, Enum):
    pass


class Proto(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class PortForward(BaseModel):
    pool_name: Optional[PoolName] = Field(alias="pool-name")
    source_port: int = Field(alias="source-port")
    translate_port: int = Field(alias="translate-port")
    source_ip: str = Field(alias="source-ip")
    translate_ip: str = Field(alias="translate-ip")
    proto: Proto

    class Config:
        allow_population_by_field_name = True


class Protocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"


class ProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RoutePolicy(str, Enum):
    pass


class Protocol(str, Enum):
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class RoutePolicy(str, Enum):
    pass


class Redistribute(BaseModel):
    protocol: Protocol
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteImport(BaseModel):
    protocol: Protocol
    protocol_sub_type: List[ProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")
    redistribute: Optional[List[Redistribute]]

    class Config:
        allow_population_by_field_name = True


class Protocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"
    EIGRP = "eigrp"


class ProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RoutePolicy(str, Enum):
    pass


class Protocol(str, Enum):
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class RoutePolicy(str, Enum):
    pass


class Redistribute(BaseModel):
    protocol: Protocol
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteImportFrom(BaseModel):
    source_vpn: int = Field(alias="source-vpn")
    protocol: Protocol
    protocol_sub_type: List[ProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")
    redistribute: Optional[List[Redistribute]]

    class Config:
        allow_population_by_field_name = True


class Protocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    EIGRP = "eigrp"
    OSPF = "ospf"


class ProtocolSubType(str, Enum):
    EXTERNAL = "external"


class RoutePolicy(str, Enum):
    pass


class Protocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"


class RoutePolicy(str, Enum):
    pass


class Redistribute(BaseModel):
    protocol: Protocol
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class RouteExport(BaseModel):
    protocol: Protocol
    protocol_sub_type: List[ProtocolSubType] = Field(alias="protocol-sub-type")
    route_policy: Optional[RoutePolicy] = Field(alias="route-policy")
    redistribute: Optional[List[Redistribute]]

    class Config:
        allow_population_by_field_name = True


class CiscoVPNModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    vpn_id: int = Field(alias="vpn-id", default=0)
    name: Optional[str]
    tenant_vpn_id: Optional[int] = Field(alias="tenant-vpn-id")
    org_name: Optional[str] = Field(alias="org-name")
    omp_admin_distance_ipv4: Optional[int] = Field(alias="omp-admin-distance-ipv4")
    omp_admin_distance_ipv6: Optional[int] = Field(alias="omp-admin-distance-ipv6")
    dns: Optional[List[Dns]]
    dns_ipv6: Optional[List[DnsIpv6]] = Field(alias="dns-ipv6")
    layer4: Optional[bool]
    host: Optional[List[Host]]
    service: Optional[List[Service]]
    service_route: Optional[List[ServiceRoute]] = Field(alias="service-route")
    route_v4: Optional[List[Routev4]] = Field(vmanage_key="route", data_path=["ip", "route"])
    route_v6: Optional[List[Routev6]] = Field(vmanage_key="route", data_path=["ipv6", "route"])
    gre_route: Optional[List[GreRoute]] = Field(alias="gre-route")
    ipsec_route: Optional[List[IpsecRoute]] = Field(alias="ipsec-route")
    advertise: Optional[List[Advertise]]
    ipv6_advertise: Optional[List[Ipv6Advertise]] = Field(alias="ipv6-advertise")
    pool: Optional[List[Pool]]
    natpool: Optional[List[Natpool]]
    static: Optional[List[Static]]
    subnet_static: Optional[List[SubnetStatic]] = Field(alias="subnet-static")
    port_forward: Optional[List[PortForward]] = Field(alias="port-forward")
    route_import: Optional[List[RouteImport]] = Field(alias="route-import")
    route_import_from: Optional[List[RouteImportFrom]] = Field(alias="route-import-from")
    route_export: Optional[List[RouteExport]] = Field(alias="route-export")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn"
