import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field
from vmngclient.api.templates.feature_template import FeatureTemplate


class STRINGBOOL(str, Enum):
    TRUE = "true"
    FALSE = "false"


class SecondaryIPv4Address(BaseModel):
    address: Optional[ipaddress.IPv4Interface]


class SecondaryIPv6Address(BaseModel):
    address: Optional[ipaddress.IPv6Interface]


class Direction(str, Enum):
    IN = "in"
    OUT = "out"


class AccessList(BaseModel):
    direction: Direction
    acl_name: str = Field(alias="acl-name")

    class Config:
        allow_population_by_field_name = True


class DhcpHelperV6(BaseModel):
    address: ipaddress.IPv6Address
    vpn: Optional[int]


class NatChoice(str, Enum):
    INTERFACE = "Interface"
    POOL = "Pool"
    LOOPBACK = "Loopback"


class StaticNat66(BaseModel):
    source_prefix: ipaddress.IPv6Interface = Field(alias="source-prefix")
    translated_source_prefix: str = Field(alias="translated-source-prefix")
    source_vpn_id: int = Field(0, alias="source-vpn-id")

    class Config:
        allow_population_by_field_name = True


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Static(BaseModel):
    source_ip: ipaddress.IPv4Address = Field(alias="source-ip")
    translate_ip: ipaddress.IPv4Address = Field(alias="translate-ip")
    static_nat_direction: StaticNatDirection = Field(
        StaticNatDirection.INSIDE, alias="static-nat-direction"
    )
    source_vpn: int = Field(0, alias="source-vpn")

    class Config:
        allow_population_by_field_name = True


class Proto(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class StaticPortForward(BaseModel):
    source_ip: ipaddress.IPv4Address = Field(alias="source-ip")
    translate_ip: ipaddress.IPv4Address = Field(alias="translate-ip")
    static_nat_direction: StaticNatDirection = Field(
        StaticNatDirection.INSIDE, alias="static-nat-direction"
    )
    source_port: int = Field(0, alias="source-port")
    translate_port: int = Field(0, alias="translate-port")
    proto: Proto
    source_vpn: int = Field(0, alias="source-vpn")

    class Config:
        allow_population_by_field_name = True


class CoreRegion(str, Enum):
    CORE = "core"
    CORE_SHARED = "core-shared"


class SecondaryRegion(str, Enum):
    OFF = "off"
    SECONDARY_ONLY = "secondary-only"
    SECONDARY_SHARED = "secondary-shared"


class Encap(str, Enum):
    GRE = "gre"
    IPSEC = "ipsec"


class Encapsulation(BaseModel):
    encap: Encap
    preference: Optional[int]
    weight: int = 1


class Mode(str, Enum):
    HUB = "hub"
    SPOKE = "spoke"


class Value(str, Enum):
    DEFAULT = "default"
    MPLS = "mpls"
    METRO_ETHERNET = "metro-ethernet"
    BIZ_INTERNET = "biz-internet"
    PUBLIC_INTERNET = "public-internet"
    LTE = "lte"
    THREEG = "3g"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    CUSTOM1 = "custom1"
    CUSTOM2 = "custom2"
    CUSTOM3 = "custom3"
    PRIVATE1 = "private1"
    PRIVATE2 = "private2"
    PRIVATE3 = "private3"
    PRIVATE4 = "private4"
    PRIVATE5 = "private5"
    PRIVATE6 = "private6"


class Carrier(str, Enum):
    DEFAULT = "default"
    CARRIER1 = "carrier1"
    CARRIER2 = "carrier2"
    CARRIER3 = "carrier3"
    CARRIER4 = "carrier4"
    CARRIER5 = "carrier5"
    CARRIER6 = "carrier6"
    CARRIER7 = "carrier7"
    CARRIER8 = "carrier8"


class MediaType(str, Enum):
    AUTO_SELECT = "auto-select"
    RJ45 = "rj45"
    SFP = "sfp"


class Speed(str, Enum):
    TEN = "10"
    HUNDRED = "100"
    THOUSAND = "1000"
    TWOANDAHALFTHOUSAND = "2500"
    TENTHOUSAND = "10000"


class Duplex(str, Enum):
    FULL = "full"
    HALF = "half"
    AUTO = "auto"


class Ip(BaseModel):
    addr: ipaddress.IPv4Address
    mac: str


class Ipv4Secondary(BaseModel):
    address: ipaddress.IPv4Address


class TrackAction(str, Enum):
    DECREMENT = "Decrement"
    SHUTDOWN = "Shutdown"


class TrackingObject(BaseModel):
    name: int
    track_action: TrackAction = Field(TrackAction.DECREMENT, alias="track-action")
    decrement: int

    class Config:
        allow_population_by_field_name = True


class Vrrp(BaseModel):
    grp_id: int = Field(alias="grp-id")
    priority: int = 100
    timer: int = 1000
    track_omp: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="track-omp")
    track_prefix_list: Optional[str] = Field(alias="track-prefix-list")
    address: Optional[ipaddress.IPv4Address]
    ipv4_secondary: Optional[List[Ipv4Secondary]] = Field(alias="ipv4-secondary")
    tloc_change_pref: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="tloc-change-pref")
    value: int
    tracking_object: Optional[List[TrackingObject]] = Field(alias="tracking-object")

    class Config:
        allow_population_by_field_name = True


class Ipv6(BaseModel):
    ipv6_link_local: ipaddress.IPv6Address = Field(alias="ipv6-link-local")
    prefix: Optional[ipaddress.IPv6Interface]

    class Config:
        allow_population_by_field_name = True


class Ipv6Vrrp(BaseModel):
    grp_id: int = Field(alias="grp-id")
    priority: int = 100
    timer: int = 1000
    track_omp: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="track-omp")
    track_prefix_list: Optional[str] = Field(alias="track-prefix-list")
    ipv6: Optional[List[Ipv6]]

    class Config:
        allow_population_by_field_name = True


class CiscoVpnInterfaceModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    if_name: str = Field(alias="if-name")
    description: Optional[str]
    poe: Optional[STRINGBOOL]
    ipv4_address: Optional[ipaddress.IPv4Interface] = Field(vmanage_key="address")
    secondary_ipv4_address: Optional[List[SecondaryIPv4Address]] = Field(
        vmanage_key="secondary-address", alias="secondary-address"
    )
    dhcp_ipv4_client: STRINGBOOL = Field(
        STRINGBOOL.FALSE, vmanage_key="dhcp-client", alias="dhcp-client"
    )
    dhcp_distance: int = Field(1, alias="dhcp-distance")
    ipv6_address: Optional[ipaddress.IPv6Interface] = Field(vmanage_key="address")
    dhcp_ipv6_client: STRINGBOOL = Field(
        STRINGBOOL.FALSE, vmanage_key="dhcp-client", alias="dhcp-client"
    )
    secondary_ipv6_address: Optional[List[SecondaryIPv6Address]] = Field(
        vmanage_key="secondary-address", alias="secondary-address"
    )
    access_list_ipv4: Optional[List[AccessList]] = Field(
        vmanage_key="access-list", alias="access-list"
    )
    dhcp_helper: Optional[List[ipaddress.IPv4Address]] = Field(alias="dhcp-helper")
    dhcp_helper_v6: Optional[List[DhcpHelperV6]] = Field(alias="dhcp-helper-v6")
    tracker: Optional[List[str]]
    auto_bandwidth_detect: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="auto-bandwidth-detect"
    )
    iperf_server: Optional[ipaddress.IPv4Address] = Field(alias="iperf-server")
    nat: STRINGBOOL = STRINGBOOL.FALSE
    nat_choice: NatChoice = Field(NatChoice.INTERFACE, alias="nat-choice")
    udp_timeout: int = Field(1, alias="udp-timeout")
    tcp_timeout: int = Field(60, alias="tcp-timeout")
    nat_range_start: Optional[ipaddress.IPv4Address] = Field(alias="range-start")
    nat_range_end: Optional[ipaddress.IPv4Address] = Field(alias="range-end")
    overload: STRINGBOOL = STRINGBOOL.TRUE
    loopback_interface: Optional[str] = Field(alias="loopback-interface")
    prefix_length: Optional[int] = Field(alias="prefix-length")
    enable: Optional[STRINGBOOL]
    nat64: Optional[STRINGBOOL]
    nat66: Optional[STRINGBOOL]
    static_nat66: Optional[List[StaticNat66]] = Field(alias="static-nat66")
    static: Optional[List[Static]]
    static_port_forward: Optional[List[StaticPortForward]] = Field(
        alias="static-port-forward"
    )
    enable_core_region: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="enable-core-region")
    core_region: CoreRegion = Field(CoreRegion.CORE, alias="core-region")
    secondary_region: SecondaryRegion = Field(
        SecondaryRegion.OFF, alias="secondary-region"
    )
    tloc_encapsulation: Optional[List[Encapsulation]]
    border: STRINGBOOL = STRINGBOOL.FALSE
    per_tunnel_qos: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="per-tunnel-qos")
    per_tunnel_qos_aggregator: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="per-tunnel-qos-aggregator"
    )
    mode: Optional[Mode]
    tunnels_bandwidth: int = Field(50, alias="tunnels-bandwidth")
    group: Optional[List[int]]
    value: Value = Value.DEFAULT
    max_control_connections: Optional[int] = Field(alias="max-control-connections")
    control_connections: STRINGBOOL = Field(
        STRINGBOOL.TRUE, alias="control-connections"
    )
    vbond_as_stun_server: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="vbond-as-stun-server"
    )
    exclude_controller_group_list: Optional[List[int]] = Field(
        alias="exclude-controller-group-list"
    )
    vmanage_connection_preference: int = Field(5, alias="vmanage-connection-preference")
    port_hop: STRINGBOOL = Field(STRINGBOOL.TRUE, alias="port-hop")
    restrict: Optional[STRINGBOOL]
    dst_ip: Optional[ipaddress.IPv4Address] = Field(alias="dst-ip")
    carrier: Carrier = Carrier.DEFAULT
    nat_refresh_interval: int = Field(5, alias="nat-refresh-interval")
    hello_interval: int = Field(1000, alias="hello-interval")
    hello_tolerance: int = Field(12, alias="hello-tolerance")
    bind: Optional[str]
    last_resort_circuit: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="last-resort-circuit"
    )
    low_bandwidth_link: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="low-bandwidth-link")
    tunnel_tcp_mss_adjust: Optional[int] = Field(alias="tunnel-tcp-mss-adjust")
    clear_dont_fragment: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="clear-dont-fragment"
    )
    propagate_sgt: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="propagate-sgt")
    network_broadcast: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="network-broadcast")
    all: Optional[STRINGBOOL]
    bgp: Optional[STRINGBOOL]
    dhcp: STRINGBOOL = STRINGBOOL.TRUE
    dns: STRINGBOOL = STRINGBOOL.TRUE
    icmp: STRINGBOOL = STRINGBOOL.TRUE
    sshd: Optional[STRINGBOOL]
    netconf: Optional[STRINGBOOL]
    ntp: Optional[STRINGBOOL]
    ospf: Optional[STRINGBOOL]
    stun: Optional[STRINGBOOL]
    snmp: Optional[STRINGBOOL]
    https: STRINGBOOL = STRINGBOOL.TRUE
    media_type: Optional[MediaType] = Field(alias="media-type")
    intrf_mtu: int = Field(1500, alias="intrf-mtu")
    mtu: int = 1500
    tcp_mss_adjust: Optional[int] = Field(alias="tcp-mss-adjust")
    tloc_extension: Optional[str] = Field(alias="tloc-extension")
    load_interval: int = Field(30, alias="load-interval")
    src_ip: Optional[ipaddress.IPv4Address] = Field(alias="src-ip")
    xconnect: Optional[str]
    mac_address: Optional[str] = Field(alias="mac-address")
    speed: Optional[Speed]
    duplex: Optional[Duplex]
    shutdown: STRINGBOOL = STRINGBOOL.TRUE
    arp_timeout: int = Field(1200, alias="arp-timeout")
    autonegotiate: Optional[STRINGBOOL]
    ip_directed_broadcast: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="ip-directed-broadcast"
    )
    icmp_redirect_disable: STRINGBOOL = Field(
        STRINGBOOL.TRUE, alias="icmp-redirect-disable"
    )
    qos_adaptive: STRINGBOOL = Field(STRINGBOOL.FALSE, alias="qos-adaptive")
    period: int = 15
    bandwidth_down: Optional[int] = Field(alias="bandwidth-down")
    dmin: Optional[int]
    dmax: Optional[int]
    bandwidth_up: Optional[int] = Field(alias="bandwidth-up")
    umin: Optional[int]
    umax: Optional[int]
    shaping_rate: Optional[int] = Field(alias="shaping-rate")
    qos_map: Optional[str] = Field(alias="qos-map")
    qos_map_vpn: Optional[str] = Field(alias="qos-map-vpn")
    service_provider: Optional[str] = Field(alias="service-provider")
    bandwidth_upstream: Optional[int] = Field(alias="bandwidth-upstream")
    bandwidth_downstream: Optional[int] = Field(alias="bandwidth-downstream")
    block_non_source_ip: STRINGBOOL = Field(
        STRINGBOOL.FALSE, alias="block-non-source-ip"
    )
    rule_name: Optional[str] = Field(alias="rule-name")
    access_list_ipv6: Optional[List[AccessList]] = Field(
        vmanage_key="access-list", alias="access-list"
    )
    ip: Optional[List[Ip]]
    vrrp: Optional[List[Vrrp]]
    ipv6_vrrp: Optional[List[Ipv6Vrrp]] = Field(alias="ipv6-vrrp")
    enable_sgt_propagation: STRINGBOOL = Field(
        STRINGBOOL.TRUE, vmanage_key="sgt", alias="sgt"
    )
    sgt: Optional[int]
    trusted: STRINGBOOL = STRINGBOOL.FALSE
    enable_sgt_authorization_and_forwarding: Optional[STRINGBOOL] = Field(
        vmanage_key="enable", alias="enable"
    )
    enable_sgt_enforcement: Optional[STRINGBOOL] = Field(
        vmanage_key="enable", alias="enable"
    )
    enforcement_sgt: Optional[int] = Field(vmanage_key="sgt")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn_interface"
