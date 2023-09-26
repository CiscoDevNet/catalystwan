import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel, ConvertIPToStringModel

DEFAULT_STATIC_NAT64_SOURCE_VPN_ID = 0
DEFAULT_STATIC_NAT_SOURCE_VPN_ID = 0
DEFAULT_STATIC_PORT_FORWARD_SOURCE_PORT = 0
DEFAULT_STATIC_PORT_FORWARD_TRANSLATE_PORT = 0
DEFAULT_STATIC_PORT_FORWARD_SOURCE_VPN = 0
DEFAULT_ENCAPSULATION_WEIGHT = 1
DEFAULT_VRRP_PRIORITY = 100
DEFAULT_VRRP_TIMER = 1000
DEFAULT_IPV6_VRRP_PRIORITY = 100
DEFAULT_IPV6_VRRP_TIMER = 1000


class SecondaryIPv4Address(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: Optional[ipaddress.IPv4Interface]


class SecondaryIPv6Address(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: Optional[ipaddress.IPv6Interface]


class Direction(str, Enum):
    IN = "in"
    OUT = "out"


class AccessList(ConvertBoolToStringModel):
    direction: Direction
    acl_name: str = Field(vmanage_key="acl-name")

    class Config:
        allow_population_by_field_name = True


class DhcpHelperV6(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv6Address
    vpn: Optional[int]


class NatChoice(str, Enum):
    INTERFACE = "Interface"
    POOL = "Pool"
    LOOPBACK = "Loopback"


class StaticNat66(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_prefix: ipaddress.IPv6Interface = Field(vmanage_key="source-prefix")
    translated_source_prefix: str = Field(vmanage_key="translated-source-prefix")
    source_vpn_id: int = Field(DEFAULT_STATIC_NAT64_SOURCE_VPN_ID, vmanage_key="source-vpn-id")

    class Config:
        allow_population_by_field_name = True


class StaticNatDirection(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class Static(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_ip: ipaddress.IPv4Address = Field(vmanage_key="source-ip")
    translate_ip: ipaddress.IPv4Address = Field(vmanage_key="translate-ip")
    static_nat_direction: StaticNatDirection = Field(StaticNatDirection.INSIDE, vmanage_key="static-nat-direction")
    source_vpn: int = Field(DEFAULT_STATIC_NAT_SOURCE_VPN_ID, vmanage_key="source-vpn")

    class Config:
        allow_population_by_field_name = True


class Proto(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class StaticPortForward(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_ip: ipaddress.IPv4Address = Field(vmanage_key="source-ip")
    translate_ip: ipaddress.IPv4Address = Field(vmanage_key="translate-ip")
    static_nat_direction: StaticNatDirection = Field(StaticNatDirection.INSIDE, vmanage_key="static-nat-direction")
    source_port: int = Field(DEFAULT_STATIC_PORT_FORWARD_SOURCE_PORT, vmanage_key="source-port")
    translate_port: int = Field(DEFAULT_STATIC_PORT_FORWARD_TRANSLATE_PORT, vmanage_key="translate-port")
    proto: Proto
    source_vpn: int = Field(DEFAULT_STATIC_PORT_FORWARD_SOURCE_VPN, vmanage_key="source-vpn")

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


class Encapsulation(ConvertBoolToStringModel):
    encap: Encap
    preference: Optional[int]
    weight: int = DEFAULT_ENCAPSULATION_WEIGHT


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


class Ip(ConvertBoolToStringModel, ConvertIPToStringModel):
    addr: ipaddress.IPv4Address
    mac: str


class Ipv4Secondary(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv4Address


class TrackAction(str, Enum):
    DECREMENT = "Decrement"
    SHUTDOWN = "Shutdown"


class TrackingObject(ConvertBoolToStringModel):
    name: int
    track_action: TrackAction = Field(TrackAction.DECREMENT, vmanage_key="track-action")
    decrement: int

    class Config:
        allow_population_by_field_name = True


class Vrrp(ConvertBoolToStringModel, ConvertIPToStringModel):
    grp_id: int = Field(vmanage_key="grp-id")
    priority: int = DEFAULT_VRRP_PRIORITY
    timer: int = DEFAULT_VRRP_TIMER
    track_omp: bool = Field(False, vmanage_key="track-omp")
    track_prefix_list: Optional[str] = Field(vmanage_key="track-prefix-list")
    address: Optional[ipaddress.IPv4Address] = Field(data_path=["ipv4"], vmanage_key="address")
    ipv4_secondary: Optional[List[Ipv4Secondary]] = Field(vmanage_key="ipv4-secondary")
    tloc_change_pref: bool = Field(False, vmanage_key="tloc-change-pref")
    value: int
    tracking_object: Optional[List[TrackingObject]] = Field(vmanage_key="tracking-object")

    class Config:
        allow_population_by_field_name = True


class Ipv6(ConvertBoolToStringModel, ConvertIPToStringModel):
    ipv6_link_local: ipaddress.IPv6Address = Field(vmanage_key="ipv6-link-local")
    prefix: Optional[ipaddress.IPv6Interface]

    class Config:
        allow_population_by_field_name = True


class Ipv6Vrrp(ConvertBoolToStringModel):
    grp_id: int = Field(vmanage_key="grp-id")
    priority: int = DEFAULT_IPV6_VRRP_PRIORITY
    timer: int = DEFAULT_IPV6_VRRP_TIMER
    track_omp: bool = Field(False, vmanage_key="track-omp")
    track_prefix_list: Optional[str] = Field(vmanage_key="track-prefix-list")
    ipv6: Optional[List[Ipv6]]

    class Config:
        allow_population_by_field_name = True


class CiscoVpnInterfaceModel(FeatureTemplate, ConvertBoolToStringModel, ConvertIPToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    if_name: str = Field(vmanage_key="if-name")
    interface_description: Optional[str] = Field(vmanage_key="description")
    poe: Optional[bool]
    ipv4_address: Optional[str] = Field(data_path=["ip"], vmanage_key="address")
    secondary_ipv4_address: Optional[List[SecondaryIPv4Address]] = Field(
        data_path=["ip"], vmanage_key="secondary-address"
    )
    dhcp_ipv4_client: Optional[bool] = Field(vmanage_key="dhcp-client")
    dhcp_distance: Optional[int] = Field(vmanage_key="dhcp-distance")
    ipv6_address: Optional[ipaddress.IPv6Interface] = Field(data_path=["ipv6"], vmanage_key="address")
    dhcp_ipv6_client: Optional[bool] = Field(vmanage_key="dhcp-client")
    secondary_ipv6_address: Optional[List[SecondaryIPv6Address]] = Field(
        data_path=["ipv6"], vmanage_key="secondary-address"
    )
    access_list_ipv4: Optional[List[AccessList]] = Field(vmanage_key="access-list")
    dhcp_helper: Optional[List[ipaddress.IPv4Address]] = Field(vmanage_key="dhcp-helper")
    dhcp_helper_v6: Optional[List[DhcpHelperV6]] = Field(vmanage_key="dhcp-helper-v6")
    tracker: Optional[List[str]]
    auto_bandwidth_detect: Optional[bool] = Field(vmanage_key="auto-bandwidth-detect")
    iperf_server: Optional[ipaddress.IPv4Address] = Field(vmanage_key="iperf-server")
    nat: Optional[bool]
    nat_choice: Optional[NatChoice] = Field(vmanage_key="nat-choice")
    udp_timeout: Optional[int] = Field(vmanage_key="udp-timeout")
    tcp_timeout: Optional[int] = Field(vmanage_key="tcp-timeout")
    nat_range_start: Optional[ipaddress.IPv4Address] = Field(vmanage_key="range-start")
    nat_range_end: Optional[ipaddress.IPv4Address] = Field(vmanage_key="range-end")
    overload: Optional[bool]
    loopback_interface: Optional[str] = Field(vmanage_key="loopback-interface")
    prefix_length: Optional[int] = Field(vmanage_key="prefix-length")
    enable: Optional[bool]
    nat64: Optional[bool]
    nat66: Optional[bool]
    static_nat66: Optional[List[StaticNat66]] = Field(vmanage_key="static-nat66")
    static: Optional[List[Static]] = Field(data_path=["nat"], vmanage_key="static")
    static_port_forward: Optional[List[StaticPortForward]] = Field(vmanage_key="static-port-forward")
    enable_core_region: Optional[bool] = Field(vmanage_key="enable-core-region")
    core_region: Optional[CoreRegion] = Field(vmanage_key="core-region")
    secondary_region: Optional[SecondaryRegion] = Field(vmanage_key="secondary-region")
    tloc_encapsulation: Optional[List[Encapsulation]] = Field(
        vmanage_key="encapsulation", data_path=["tunnel-interface"]
    )
    border: Optional[bool] = Field(data_path=["tunnel-interface"])
    per_tunnel_qos: Optional[bool] = Field(vmanage_key="per-tunnel-qos")
    per_tunnel_qos_aggregator: Optional[bool] = Field(vmanage_key="per-tunnel-qos-aggregator")
    mode: Optional[Mode]
    tunnels_bandwidth: Optional[int] = Field(vmanage_key="tunnels-bandwidth")
    group: Optional[List[int]] = Field(data_path=["tunnel-interface"])
    value: Optional[Value] = Field(data_path=["tunnel-interface", "color"])
    max_control_connections: Optional[int] = Field(
        vmanage_key="max-control-connections", data_path=["tunnel-interface"]
    )
    control_connections: Optional[bool] = Field(vmanage_key="control-connections", data_path=["tunnel-interface"])
    vbond_as_stun_server: Optional[bool] = Field(vmanage_key="vbond-as-stun-server", data_path=["tunnel-interface"])
    exclude_controller_group_list: Optional[List[int]] = Field(
        vmanage_key="exclude-controller-group-list", data_path=["tunnel-interface"]
    )
    vmanage_connection_preference: Optional[int] = Field(
        vmanage_key="vmanage-connection-preference", data_path=["tunnel-interface"]
    )
    port_hop: Optional[bool] = Field(vmanage_key="port-hop", data_path=["tunnel-interface"])
    restrict: Optional[bool] = Field(data_path=["tunnel-interface", "color"])
    dst_ip: Optional[ipaddress.IPv4Address] = Field(
        vmanage_key="dst-ip", data_path=["tunnel-interface", "tloc-extension-gre-to"]
    )
    carrier: Optional[Carrier] = Field(data_path=["tunnel-interface"])
    nat_refresh_interval: Optional[int] = Field(vmanage_key="nat-refresh-interval", data_path=["tunnel-interface"])
    hello_interval: Optional[int] = Field(vmanage_key="hello-interval", data_path=["tunnel-interface"])
    hello_tolerance: Optional[int] = Field(vmanage_key="hello-tolerance", data_path=["tunnel-interface"])
    bind: Optional[str] = Field(data_path=["tunnel-interface"])
    last_resort_circuit: Optional[bool] = Field(vmanage_key="last-resort-circuit", data_path=["tunnel-interface"])
    low_bandwidth_link: Optional[bool] = Field(vmanage_key="low-bandwidth-link", data_path=["tunnel-interface"])
    tunnel_tcp_mss_adjust: Optional[int] = Field(vmanage_key="tunnel-tcp-mss-adjust", data_path=["tunnel-interface"])
    clear_dont_fragment: Optional[bool] = Field(vmanage_key="clear-dont-fragment", data_path=["tunnel-interface"])
    propagate_sgt: Optional[bool] = Field(data_path=["tunnel-interface"], vmanage_key="propagate-sgt")
    network_broadcast: Optional[bool] = Field(vmanage_key="network-broadcast", data_path=["tunnel-interface"])
    all: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    bgp: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    dhcp: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    dns: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    icmp: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    sshd: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    netconf: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    ntp: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    ospf: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    stun: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    snmp: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    https: Optional[bool] = Field(data_path=["tunnel-interface", "allow-service"])
    media_type: Optional[MediaType] = Field(vmanage_key="media-type")
    intrf_mtu: Optional[int] = Field(vmanage_key="intrf-mtu")
    mtu: Optional[int]
    tcp_mss_adjust: Optional[int] = Field(vmanage_key="tcp-mss-adjust")
    tloc_extension: Optional[str] = Field(vmanage_key="tloc-extension")
    load_interval: Optional[int] = Field(vmanage_key="load-interval")
    src_ip: Optional[ipaddress.IPv4Address] = Field(vmanage_key="src-ip", data_path=["tloc-extension-gre-from"])
    xconnect: Optional[str] = Field(data_path=["tloc-extension-gre-from"])
    mac_address: Optional[str] = Field(vmanage_key="mac-address")
    speed: Optional[Speed]
    duplex: Optional[Duplex]
    shutdown: Optional[bool] = False
    arp_timeout: Optional[int] = Field(vmanage_key="arp-timeout")
    autonegotiate: Optional[bool]
    ip_directed_broadcast: Optional[bool] = Field(vmanage_key="ip-directed-broadcast")
    icmp_redirect_disable: Optional[bool] = Field(vmanage_key="icmp-redirect-disable")
    qos_adaptive: Optional[bool] = Field(vmanage_key="qos-adaptive")
    period: Optional[int] = Field(data_path=["qos-adaptive"])
    bandwidth_down: Optional[int] = Field(vmanage_key="bandwidth-down", data_path=["qos-adaptive", "downstream"])
    dmin: Optional[int] = Field(data_path=["qos-adaptive", "downstream", "range"])
    dmax: Optional[int] = Field(data_path=["qos-adaptive", "downstream", "range"])
    bandwidth_up: Optional[int] = Field(vmanage_key="bandwidth-up", data_path=["qos-adaptive", "upstream"])
    umin: Optional[int] = Field(data_path=["qos-adaptive", "upstream", "range"])
    umax: Optional[int] = Field(data_path=["qos-adaptive", "upstream", "range"])
    shaping_rate: Optional[int] = Field(vmanage_key="shaping-rate")
    qos_map: Optional[str] = Field(vmanage_key="qos-map")
    qos_map_vpn: Optional[str] = Field(vmanage_key="qos-map-vpn")
    service_provider: Optional[str] = Field(vmanage_key="service-provider")
    bandwidth_upstream: Optional[int] = Field(vmanage_key="bandwidth-upstream")
    bandwidth_downstream: Optional[int] = Field(vmanage_key="bandwidth-downstream")
    block_non_source_ip: Optional[bool] = Field(vmanage_key="block-non-source-ip")
    rule_name: Optional[str] = Field(vmanage_key="rule-name", data_path=["rewrite-rule"])
    access_list_ipv6: Optional[List[AccessList]] = Field(data_path=["ipv6"], vmanage_key="access-list")
    ip: Optional[List[Ip]] = Field(data_path=["arp"])
    vrrp: Optional[List[Vrrp]] = Field(vmanage_key="vrrp")
    ipv6_vrrp: Optional[List[Ipv6Vrrp]] = Field(vmanage_key="ipv6-vrrp")
    enable_sgt_propagation: Optional[bool] = Field(data_path=["trustsec", "propagate"], vmanage_key="sgt")
    security_group_tag: Optional[int] = Field(data_path=["trustsec", "static"], vmanage_key="sgt")
    trusted: Optional[bool] = Field(data_path=["trustsec", "static"])
    enable_sgt_authorization_and_forwarding: Optional[bool] = Field(data_path=["trustsec"], vmanage_key="enable")
    enable_sgt_enforcement: Optional[bool] = Field(data_path=["trustsec", "enforcement"], vmanage_key="enable")
    enforcement_sgt: Optional[int] = Field(data_path=["trustsec", "enforcement"], vmanage_key="sgt")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn_interface"
