import ipaddress
from enum import Enum
from pathlib import Path
from typing import Annotated, ClassVar, List, Literal, Optional, Union

from pydantic import BeforeValidator, ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.models.cisco_omp_model import DEFAULT_OMP_SENDPATH_LIMIT
from catalystwan.api.templates.models.cisco_system import Tracker
from catalystwan.api.templates.models.cisco_vpn_model import Dns
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel, ConvertIPToStringModel

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

Trusted = Annotated[bool, BeforeValidator(lambda x: x if isinstance(x, bool) else x == [1])]
SamplingRateStream = Annotated[Union[int, None], BeforeValidator(lambda x: None if x == "" else x)]


class SecondaryIPv4Address(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: Optional[ipaddress.IPv4Interface] = None


class SecondaryIPv6Address(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: Optional[ipaddress.IPv6Interface] = None


Direction = Literal["in", "out"]


class AccessList(ConvertBoolToStringModel):
    direction: Direction
    acl_name: str = Field(json_schema_extra={"vmanage_key": "acl-name"})
    model_config = ConfigDict(populate_by_name=True)


class DhcpHelperV6(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv6Address
    vpn: Optional[int] = None


NatChoice = Literal["interface", "pool", "loopback"]


class StaticNat66(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_prefix: ipaddress.IPv6Interface = Field(json_schema_extra={"vmanage_key": "source-prefix"})
    translated_source_prefix: str = Field(json_schema_extra={"vmanage_key": "translated-source-prefix"})
    source_vpn_id: int = Field(DEFAULT_STATIC_NAT64_SOURCE_VPN_ID, json_schema_extra={"vmanage_key": "source-vpn-id"})
    model_config = ConfigDict(populate_by_name=True)


StaticNatDirection = Literal["inside", "outside"]


class Static(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        serialization_alias="source-ip",
        validation_alias="source-ip",
        json_schema_extra={"vmanage_key": "source-ip"},
    )
    translate_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        serialization_alias="translate-ip",
        validation_alias="translate-ip",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    static_nat_direction: StaticNatDirection = Field(
        default="inside",
        serialization_alias="static-nat-direction",
        validation_alias="static-nat-direction",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    source_vpn: Optional[int] = Field(
        default=DEFAULT_STATIC_NAT_SOURCE_VPN_ID,
        serialization_alias="source-vpn",
        validation_alias="source-vpn",
        json_schema_extra={"vmanage_key": "source-vpn"},
    )
    model_config = ConfigDict(populate_by_name=True)


Proto = Literal["tcp", "udp"]


class StaticPortForward(ConvertBoolToStringModel, ConvertIPToStringModel):
    source_ip: ipaddress.IPv4Address = Field(
        serialization_alias="source-ip", validation_alias="source-ip", json_schema_extra={"vmanage_key": "source-ip"}
    )
    translate_ip: ipaddress.IPv4Address = Field(
        serialization_alias="translate-ip",
        validation_alias="translate-ip",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    static_nat_direction: StaticNatDirection = Field(
        default="inside",
        serialization_alias="static-nat-direction",
        validation_alias="static-nat-direction",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    source_port: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_SOURCE_PORT,
        serialization_alias="source-port",
        validation_alias="source-port",
        json_schema_extra={"vmanage_key": "source-port"},
    )
    translate_port: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_TRANSLATE_PORT,
        serialization_alias="translate-port",
        validation_alias="translate-port",
        json_schema_extra={"vmanage_key": "translate-port"},
    )
    proto: Proto
    source_vpn: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_SOURCE_VPN,
        serialization_alias="source-vpn",
        validation_alias="source-vpn",
        json_schema_extra={"vmanage_key": "source-vpn"},
    )
    model_config = ConfigDict(populate_by_name=True)


CoreRegion = Literal["core", "core-shared"]
SecondaryRegion = Literal["core", "secondary-only", "secondary-shared"]


Encap = Literal["gre", "ipsec"]


class Encapsulation(ConvertBoolToStringModel):
    encap: Encap
    preference: Optional[int] = None
    weight: int = DEFAULT_ENCAPSULATION_WEIGHT


Mode = Literal["hub", "spoke"]


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


Carrier = Literal[
    "default", "carrier1", "carrier2", "carrier3", "carrier4", "carrier5", "carrier6", "carrier7", "carrier8"
]

MediaType = Literal["auto-select", "rj45", "sfp"]


Speed = Literal["10", "100", "1000", "2500", "10000"]


Duplex = Literal["full", "half", "auto"]


class Ip(ConvertBoolToStringModel, ConvertIPToStringModel):
    addr: ipaddress.IPv4Address
    mac: str


class Ipv4Secondary(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv4Address


TrackAction = Literal["Decrement", "Shutdown"]


class TrackingObject(ConvertBoolToStringModel):
    name: int
    track_action: TrackAction = Field(
        default="Decrement",
        validation_alias="track-action",
        serialization_alias="track-action",
        json_schema_extra={"vmanage_key": "track-action"},
    )
    decrement: int
    model_config = ConfigDict(populate_by_name=True)


class Vrrp(ConvertBoolToStringModel, ConvertIPToStringModel):
    grp_id: int = Field(
        validation_alias="grp-id", serialization_alias="grp-id", json_schema_extra={"vmanage_key": "grp-id"}
    )
    priority: int = DEFAULT_VRRP_PRIORITY
    timer: int = DEFAULT_VRRP_TIMER
    track_omp: bool = Field(
        default=False,
        validation_alias="track-omp",
        serialization_alias="track-omp",
        json_schema_extra={"vmanage_key": "track-omp"},
    )
    track_prefix_list: Optional[str] = Field(
        default=None,
        validation_alias="track-prefix-list",
        serialization_alias="track-prefix-list",
        json_schema_extra={"vmanage_key": "track-prefix-list"},
    )
    address: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"data_path": ["ipv4"], "vmanage_key": "address"}
    )
    ipv4_secondary: Optional[List[Ipv4Secondary]] = Field(
        default=None,
        validation_alias="ipv4-secondary",
        serialization_alias="ipv4-secondary",
        json_schema_extra={"vmanage_key": "ipv4-secondary"},
    )
    tloc_change_pref: bool = Field(
        default=False,
        validation_alias="tloc-change-pref",
        serialization_alias="tloc-change-pref",
        json_schema_extra={"vmanage_key": "tloc-change-pref"},
    )
    value: int
    tracking_object: Optional[List[TrackingObject]] = Field(
        default=None,
        validation_alias="tracking-object",
        serialization_alias="tracking-object",
        json_schema_extra={"vmanage_key": "tracking-object"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6(ConvertBoolToStringModel, ConvertIPToStringModel):
    ipv6_link_local: ipaddress.IPv6Address = Field(
        serialization_alias="ipv6-link-local",
        validation_alias="ipv6-link-local",
        json_schema_extra={"vmanage_key": "ipv6-link-local"},
    )
    prefix: Optional[ipaddress.IPv6Interface] = None
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Vrrp(ConvertBoolToStringModel):
    grp_id: int = Field(
        serialization_alias="grp-id", validation_alias="grp-id", json_schema_extra={"vmanage_key": "grp-id"}
    )
    priority: int = DEFAULT_IPV6_VRRP_PRIORITY
    timer: int = DEFAULT_IPV6_VRRP_TIMER
    track_omp: bool = Field(
        default=False,
        serialization_alias="track-omp",
        validation_alias="track-omp",
        json_schema_extra={"vmanage_key": "track-omp"},
    )
    track_prefix_list: Optional[str] = Field(
        default=None,
        validation_alias="track-prefix-list",
        serialization_alias="track-prefix-list",
        json_schema_extra={"vmanage_key": "track-prefix-list"},
    )
    ipv6: Optional[List[Ipv6]] = None
    model_config = ConfigDict(populate_by_name=True)


class CiscoVpnInterfaceModel(FeatureTemplate, ConvertBoolToStringModel, ConvertIPToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    if_name: str = Field(
        serialization_alias="if-name", validation_alias="if-name", json_schema_extra={"vmanage_key": "if-name"}
    )
    interface_description: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "description"})
    poe: Optional[bool] = None
    ipv4_address: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["ip"], "vmanage_key": "address"})
    secondary_ipv4_address: Optional[List[SecondaryIPv4Address]] = Field(
        default=None,
        validation_alias="secondary-address",
        serialization_alias="secondary-address",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "secondary-address"},
    )
    dhcp_ipv4_client: Optional[bool] = Field(
        default=None,
        validation_alias="dhcp-client",
        serialization_alias="dhcp-client",
        json_schema_extra={"vmanage_key": "dhcp-client"},
    )
    dhcp_distance: Optional[int] = Field(
        default=None,
        validation_alias="dhcp-distance",
        serialization_alias="dhcp-distance",
        json_schema_extra={"vmanage_key": "dhcp-distance"},
    )
    ipv6_address: Optional[ipaddress.IPv6Interface] = Field(
        default=None, json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "address"}
    )
    dhcp_ipv6_client: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "dhcp-client"})
    secondary_ipv6_address: Optional[List[SecondaryIPv6Address]] = Field(
        default=None,
        validation_alias="secondary-address",
        serialization_alias="secondary-address",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "secondary-address"},
    )
    access_list_ipv4: Optional[List[AccessList]] = Field(
        default=None,
        validation_alias="access-list",
        serialization_alias="access-list",
        json_schema_extra={"vmanage_key": "access-list"},
    )
    dhcp_helper: Optional[List[ipaddress.IPv4Address]] = Field(
        default=None,
        serialization_alias="dhcp-helper",
        validation_alias="dhcp-helper",
        json_schema_extra={"vmanage_key": "dhcp-helper"},
    )
    dhcp_helper_v6: Optional[List[DhcpHelperV6]] = Field(
        default=None,
        validation_alias="dhcp-helper-v6",
        serialization_alias="dhcp-helper-v6",
        json_schema_extra={"vmanage_key": "dhcp-helper-v6"},
    )
    tracker: Optional[Union[List[str], List[Tracker]]] = None
    auto_bandwidth_detect: Optional[bool] = Field(
        default=None,
        validation_alias="auto-bandwidth-detect",
        serialization_alias="auto-bandwidth-detect",
        json_schema_extra={"vmanage_key": "auto-bandwidth-detect"},
    )
    iperf_server: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        validation_alias="iperf-server",
        serialization_alias="iperf-server",
        json_schema_extra={"vmanage_key": "iperf-server"},
    )
    nat: Optional[bool] = None
    nat_choice: Optional[NatChoice] = Field(
        default=None,
        validation_alias="nat-choice",
        serialization_alias="nat-choice",
        json_schema_extra={"vmanage_key": "nat-choice"},
    )
    udp_timeout: Optional[int] = Field(
        default=None,
        serialization_alias="udp-timeout",
        validation_alias="udp-timeout",
        json_schema_extra={"vmanage_key": "udp-timeout"},
    )
    tcp_timeout: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tcp-timeout"})
    nat_range_start: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"vmanage_key": "range-start"}
    )
    nat_range_end: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        validation_alias="range-end",
        serialization_alias="range-end",
        json_schema_extra={"vmanage_key": "range-end"},
    )
    overload: Optional[bool] = None
    loopback_interface: Optional[str] = Field(
        default=None,
        validation_alias="loopback-interface",
        serialization_alias="loopback-interface",
        json_schema_extra={"vmanage_key": "loopback-interface"},
    )
    prefix_length: Optional[int] = Field(
        default=None,
        validation_alias="prefix-length",
        serialization_alias="prefix-length",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    enable: Optional[bool] = None
    nat64: Optional[bool] = None
    nat66: Optional[bool] = None
    static_nat66: Optional[List[StaticNat66]] = Field(
        default=None,
        validation_alias="static-nat66",
        serialization_alias="static-nat66",
        json_schema_extra={"vmanage_key": "static-nat66"},
    )
    static: Optional[List[Static]] = Field(
        default=None, json_schema_extra={"data_path": ["nat"], "vmanage_key": "static"}
    )
    static_port_forward: Optional[List[StaticPortForward]] = Field(
        default=None, json_schema_extra={"vmanage_key": "static-port-forward"}
    )
    enable_core_region: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "enable-core-region"})
    core_region: Optional[CoreRegion] = Field(default=None, json_schema_extra={"vmanage_key": "core-region"})
    secondary_region: Optional[SecondaryRegion] = Field(
        default=None, json_schema_extra={"vmanage_key": "secondary-region"}
    )
    tloc_encapsulation: Optional[List[Encapsulation]] = Field(
        default=None, json_schema_extra={"vmanage_key": "encapsulation", "data_path": ["tunnel-interface"]}
    )
    border: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface"]})
    per_tunnel_qos: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "per-tunnel-qos"})
    per_tunnel_qos_aggregator: Optional[bool] = Field(
        default=None, json_schema_extra={"vmanage_key": "per-tunnel-qos-aggregator"}
    )
    mode: Optional[Mode] = None
    tunnels_bandwidth: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tunnels-bandwidth"})
    group: Optional[List[int]] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface"]})
    value: Optional[Value] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "color"]})
    max_control_connections: Optional[int] = Field(
        default=None,
        validation_alias="max-control-connections",
        serialization_alias="max-control-connections",
        json_schema_extra={"vmanage_key": "max-control-connections", "data_path": ["tunnel-interface"]},
    )
    control_connections: Optional[bool] = Field(
        default=None,
        validation_alias="control-connections",
        serialization_alias="control-connections",
        json_schema_extra={"vmanage_key": "control-connections", "data_path": ["tunnel-interface"]},
    )
    vbond_as_stun_server: Optional[bool] = Field(
        default=None, json_schema_extra={"vmanage_key": "vbond-as-stun-server", "data_path": ["tunnel-interface"]}
    )
    exclude_controller_group_list: Optional[List[int]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "exclude-controller-group-list", "data_path": ["tunnel-interface"]},
    )
    vmanage_connection_preference: Optional[int] = Field(
        default=None,
        validation_alias="vmanage-connection-preference",
        serialization_alias="vmanage-connection-preference",
        json_schema_extra={"vmanage_key": "vmanage-connection-preference", "data_path": ["tunnel-interface"]},
    )
    port_hop: Optional[bool] = Field(
        default=None, json_schema_extra={"vmanage_key": "port-hop", "data_path": ["tunnel-interface"]}
    )
    restrict: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "color"]})
    dst_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "dst-ip", "data_path": ["tunnel-interface", "tloc-extension-gre-to"]},
    )
    carrier: Optional[Carrier] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface"]})
    nat_refresh_interval: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "nat-refresh-interval", "data_path": ["tunnel-interface"]}
    )
    hello_interval: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "hello-interval", "data_path": ["tunnel-interface"]}
    )
    hello_tolerance: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "hello-tolerance", "data_path": ["tunnel-interface"]}
    )
    bind: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface"]})
    last_resort_circuit: Optional[bool] = Field(
        default=None,
        validation_alias="last-resort-circuit",
        serialization_alias="last-resort-circuit",
        json_schema_extra={"vmanage_key": "last-resort-circuit", "data_path": ["tunnel-interface"]},
    )
    low_bandwidth_link: Optional[bool] = Field(
        default=None,
        validation_alias="low-bandwidth-link",
        serialization_alias="low-bandwidth-link",
        json_schema_extra={"vmanage_key": "low-bandwidth-link", "data_path": ["tunnel-interface"]},
    )
    tunnel_tcp_mss_adjust: Optional[int] = Field(
        default=None,
        validation_alias="tunnel-tcp-mss-adjust",
        serialization_alias="tunnel-tcp-mss-adjust",
        json_schema_extra={"vmanage_key": "tunnel-tcp-mss-adjust", "data_path": ["tunnel-interface"]},
    )
    clear_dont_fragment: Optional[bool] = Field(
        default=None,
        validation_alias="clear-dont-fragment",
        serialization_alias="clear-dont-fragment",
        json_schema_extra={"vmanage_key": "clear-dont-fragment", "data_path": ["tunnel-interface"]},
    )
    propagate_sgt: Optional[bool] = Field(
        default=None,
        validation_alias="propagate-sgt",
        serialization_alias="propagate-sgt",
        json_schema_extra={"data_path": ["tunnel-interface"], "vmanage_key": "propagate-sgt"},
    )
    network_broadcast: Optional[bool] = Field(
        default=None, json_schema_extra={"vmanage_key": "network-broadcast", "data_path": ["tunnel-interface"]}
    )
    all: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    bgp: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    dhcp: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    dns: Optional[List[Dns]] = None
    icmp: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    sshd: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    netconf: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]}
    )
    ntp: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    ospf: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    stun: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    snmp: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    https: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]})
    media_type: Optional[MediaType] = Field(default=None, json_schema_extra={"vmanage_key": "media-type"})
    intrf_mtu: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "intrf-mtu"})
    mtu: Optional[int] = None
    tcp_mss_adjust: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tcp-mss-adjust"})
    tloc_extension: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "tloc-extension"})
    load_interval: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "load-interval"})
    src_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"vmanage_key": "src-ip", "data_path": ["tloc-extension-gre-from"]}
    )
    xconnect: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["tloc-extension-gre-from"]})
    mac_address: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "mac-address"})
    speed: Optional[Speed] = None
    duplex: Optional[Duplex] = None
    shutdown: Optional[bool] = False
    arp_timeout: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "arp-timeout"})
    autonegotiate: Optional[bool] = None
    ip_directed_broadcast: Optional[bool] = Field(
        default=None,
        validation_alias="ip-directed-broadcast",
        serialization_alias="ip-directed-broadcast",
        json_schema_extra={"vmanage_key": "ip-directed-broadcast"},
    )
    icmp_redirect_disable: Optional[bool] = Field(
        default=None,
        validation_alias="icmp-redirect-disable",
        serialization_alias="icmp-redirect-disable",
        json_schema_extra={"vmanage_key": "icmp-redirect-disable"},
    )
    qos_adaptive: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "qos-adaptive"})
    period: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["qos-adaptive"]})
    bandwidth_down: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "bandwidth-down", "data_path": ["qos-adaptive", "downstream"]}
    )
    dmin: Optional[SamplingRateStream] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "downstream", "range"]},
        description="Shaping Rate Downstream: Min Downstream (Kbps)",
    )
    dmax: Optional[SamplingRateStream] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "downstream", "range"]},
        description="Shaping Rate Downstream: Max Downstream (Kbps)",
    )
    bandwidth_up: Optional[int] = Field(
        default=None, json_schema_extra={"vmanage_key": "bandwidth-up", "data_path": ["qos-adaptive", "upstream"]}
    )
    umin: Optional[SamplingRateStream] = Field(
        default=None, json_schema_extra={"data_path": ["qos-adaptive", "upstream", "range"]}
    )
    umax: Optional[SamplingRateStream] = Field(
        default=None, json_schema_extra={"data_path": ["qos-adaptive", "upstream", "range"]}
    )
    shaping_rate: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "shaping-rate"})
    qos_map: Optional[str] = Field(
        default=None,
        validation_alias="qos-map",
        serialization_alias="qos-map",
        json_schema_extra={"vmanage_key": "qos-map"},
    )
    qos_map_vpn: Optional[str] = Field(
        default=None,
        validation_alias="qos-map-vpn",
        serialization_alias="qos-map-vpn",
        json_schema_extra={"vmanage_key": "qos-map-vpn"},
    )
    service_provider: Optional[str] = Field(
        default=None,
        serialization_alias="service-provider",
        validation_alias="service-provider",
        json_schema_extra={"vmanage_key": "service-provider"},
    )
    bandwidth_upstream: Optional[int] = Field(
        default=None,
        serialization_alias="bandwidth-upstream",
        validation_alias="bandwidth-upstream",
        json_schema_extra={"vmanage_key": "bandwidth-upstream"},
    )
    bandwidth_downstream: Optional[int] = Field(
        default=None,
        serialization_alias="bandwidth-downstream",
        validation_alias="bandwidth-downstream",
        json_schema_extra={"vmanage_key": "bandwidth-downstream"},
    )
    block_non_source_ip: Optional[bool] = Field(
        default=None,
        validation_alias="block-non-source-ip",
        serialization_alias="block-non-source-ip",
        json_schema_extra={"vmanage_key": "block-non-source-ip"},
    )
    rule_name: Optional[str] = Field(
        default=None,
        serialization_alias="rule-name",
        validation_alias="rule-name",
        json_schema_extra={"vmanage_key": "rule-name", "data_path": ["rewrite-rule"]},
    )
    access_list_ipv6: Optional[List[AccessList]] = Field(
        default=None,
        validation_alias="access-list-ipv6",
        serialization_alias="access-list-ipv6",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "access-list"},
    )
    ip: Optional[List[Ip]] = Field(default=None, json_schema_extra={"data_path": ["arp"]})
    vrrp: Optional[List[Vrrp]] = Field(default=None, json_schema_extra={"vmanage_key": "vrrp"})
    ipv6_vrrp: Optional[List[Ipv6Vrrp]] = Field(
        default=None,
        serialization_alias="ipv6-vrrp",
        validation_alias="ipv6-vrrp",
        json_schema_extra={"vmanage_key": "ipv6-vrrp"},
    )
    enable_sgt_propagation: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["trustsec", "propagate"], "vmanage_key": "sgt"}
    )
    security_group_tag: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["trustsec", "static"], "vmanage_key": "sgt"}
    )
    trusted: Optional[Trusted] = Field(default=None, json_schema_extra={"data_path": ["trustsec", "static"]})
    enable_sgt_authorization_and_forwarding: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["trustsec"], "vmanage_key": "enable"}
    )
    enable_sgt_enforcement: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["trustsec", "enforcement"], "vmanage_key": "enable"}
    )
    enforcement_sgt: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["trustsec", "enforcement"], "vmanage_key": "sgt"}
    )
    send_path_limit: Optional[int] = Field(
        default=DEFAULT_OMP_SENDPATH_LIMIT,
        validation_alias="send-path-limit",
        serialization_alias="send-path-limit",
        json_schema_extra={"vmanage_key": "send-path-limit"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn_interface"
