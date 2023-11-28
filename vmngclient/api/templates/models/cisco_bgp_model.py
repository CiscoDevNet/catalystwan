from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import BaseModel, Field, validator

from vmngclient.api.templates.feature_template import FeatureTemplate


class Export(BaseModel):
    asn_ip: str = Field(vmanage_key="asn-ip")

    class Config:
        allow_population_by_field_name = True


class Import(BaseModel):
    asn_ip: str = Field(vmanage_key="asn-ip")

    class Config:
        allow_population_by_field_name = True


class RouteTargetIpv4(BaseModel):
    vpn_id: int = Field(vmanage_key="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import")

    class Config:
        allow_population_by_field_name = True


class RouteTargetIpv6(BaseModel):
    vpn_id: int = Field(vmanage_key="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import")

    class Config:
        allow_population_by_field_name = True


class MplsInterface(BaseModel):
    if_name: Optional[str] = Field(vmanage_key="if-name")

    class Config:
        allow_population_by_field_name = True


class AddressFamilyType(str, Enum):
    IPV4_UNICAST = "ipv4-unicast"


class AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(vmanage_key="as-set")
    summary_only: Optional[bool] = Field(vmanage_key="summary-only")

    class Config:
        allow_population_by_field_name = True

    @validator("as_set", "summary_only")
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class Ipv6AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(False, vmanage_key="as-set")
    summary_only: Optional[bool] = Field(False, vmanage_key="summary-only")

    class Config:
        allow_population_by_field_name = True


class Network(BaseModel):
    prefix: str


class Ipv6Network(BaseModel):
    prefix: str


class Protocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    OSPF = "ospf"
    OSPFV3 = "ospfv3"
    OMP = "omp"
    EIGRP = "eigrp"
    NAT = "nat"


class Redistribute(BaseModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(vmanage_key="route-policy")

    class Config:
        allow_population_by_field_name = True


class AddressFamily(BaseModel):
    family_type: AddressFamilyType = Field(vmanage_key="family-type")
    aggregate_address: Optional[List[AggregateAddress]] = Field(vmanage_key="aggregate-address")
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(vmanage_key="ipv6-aggregate-address")
    network: Optional[List[Network]]
    ipv6_network: Optional[List[Ipv6Network]] = Field(vmanage_key="ipv6-network")
    paths: Optional[int] = Field(data_path=["maximum-paths"])
    originate: Optional[bool] = Field(data_path=["default-information"])
    policy_name: Optional[str] = Field(data_path=["table-map"], vmanage_key="name")
    filter: Optional[bool] = Field(data_path=["table-map"])
    redistribute: Optional[List[Redistribute]]

    class Config:
        allow_population_by_field_name = True

    @validator("originate", "filter")
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class NeighborFamilyType(str, Enum):
    IPV4_UNICAST = "ipv4-unicast"
    VPNV4_UNICAST = "vpnv4-unicast"
    VPNV6_UNICAST = "vpnv6-unicast"


class Direction(str, Enum):
    IN = "in"
    OUT = "out"


class RoutePolicy(BaseModel):
    direction: Direction
    pol_name: str = Field(vmanage_key="pol-name")

    class Config:
        allow_population_by_field_name = True


class NeighborAddressFamily(BaseModel):
    family_type: NeighborFamilyType = Field(vmanage_key="family-type")
    prefix_num: Optional[int] = Field(data_path=["maximum-prefixes"], vmanage_key="prefix-num")
    threshold: Optional[int] = Field(data_path=["maximum-prefixes"])
    restart: Optional[int] = Field(data_path=["maximum-prefixes"])
    warning_only: Optional[bool] = Field(data_path=["maximum-prefixes"], vmanage_key="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(vmanage_key="route-policy")

    class Config:
        allow_population_by_field_name = True


class Neighbor(BaseModel):
    address: str
    description: Optional[str]
    shutdown: Optional[bool]
    remote_as: int = Field(vmanage_key="remote-as")
    keepalive: Optional[int] = Field(data_path=["timers"])
    holdtime: Optional[int] = Field(data_path=["timers"])
    if_name: Optional[str] = Field(data_path=["update-source"], vmanage_key="if-name")
    next_hop_self: Optional[bool] = Field(vmanage_key="next-hop-self")
    send_community: Optional[bool] = Field(vmanage_key="send-community")
    send_ext_community: Optional[bool] = Field(vmanage_key="send-ext-community")
    ebgp_multihop: Optional[int] = Field(vmanage_key="ebgp-multihop")
    password: Optional[str]
    send_label: Optional[bool] = Field(vmanage_key="send-label")
    send_label_explicit: Optional[bool] = Field(vmanage_key="send-label-explicit")
    as_override: Optional[bool] = Field(vmanage_key="as-override")
    as_number: Optional[int] = Field(data_path=["allowas-in"], vmanage_key="as-number")
    address_family: Optional[List[NeighborAddressFamily]] = Field(vmanage_key="address-family")

    class Config:
        allow_population_by_field_name = True

    @validator(
        "shutdown",
        "next_hop_self",
        "send_community",
        "send_ext_community",
        "send_label",
        "send_label_explicit",
        "as_override",
    )
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class IPv6NeighborFamilyType(str, Enum):
    IPV6_UNICAST = "ipv6-unicast"


class IPv6NeighborAddressFamily(BaseModel):
    family_type: IPv6NeighborFamilyType = Field(vmanage_key="family-type")
    prefix_num: Optional[int] = Field(0, data_path=["maximum-prefixes"], vmanage_key="prefix-num")
    threshold: Optional[int] = Field(data_path=["maximum-prefixes"])
    restart: Optional[int] = Field(data_path=["maximum-prefixes"])
    warning_only: Optional[bool] = Field(False, data_path=["maximum-prefixes"], vmanage_key="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(vmanage_key="route-policy")

    class Config:
        allow_population_by_field_name = True


class Ipv6Neighbor(BaseModel):
    address: str
    description: Optional[str]
    shutdown: Optional[bool]
    remote_as: int = Field(vmanage_key="remote-as")
    keepalive: Optional[int] = Field(data_path=["timers"])
    holdtime: Optional[int] = Field(data_path=["timers"])
    if_name: Optional[str] = Field(data_path=["update-source"], vmanage_key="if-name")
    next_hop_self: Optional[bool] = Field(False, vmanage_key="next-hop-self")
    send_community: Optional[bool] = Field(True, vmanage_key="send-community")
    send_ext_community: Optional[bool] = Field(True, vmanage_key="send-ext-community")
    ebgp_multihop: Optional[int] = Field(1, vmanage_key="ebgp-multihop")
    password: Optional[str]
    send_label: Optional[bool] = Field(False, vmanage_key="send-label")
    send_label_explicit: Optional[bool] = Field(False, vmanage_key="send-label-explicit")
    as_override: Optional[bool] = Field(False, vmanage_key="as-override")
    as_number: Optional[int] = Field(data_path=["allowas-in"], vmanage_key="as-number")
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(vmanage_key="address-family")

    class Config:
        allow_population_by_field_name = True

    @validator(
        "shutdown",
        "next_hop_self",
        "send_community",
        "send_ext_community",
        "send_label",
        "send_label_explicit",
        "as_override",
    )
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class CiscoBGPModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    as_num: Optional[str] = Field(data_path=["bgp"], vmanage_key="as-num")
    shutdown: Optional[bool] = Field(data_path=["bgp"])
    router_id: Optional[str] = Field(data_path=["bgp"], vmanage_key="router-id")
    propagate_aspath: Optional[bool] = Field(data_path=["bgp"], vmanage_key="propagate-aspath")
    propagate_community: Optional[bool] = Field(data_path=["bgp"], vmanage_key="propagate-community")
    route_target_ipv4: List[RouteTargetIpv4] = Field([], data_path=["bgp", "target"], vmanage_key="route-target-ipv4")
    route_target_ipv6: List[RouteTargetIpv6] = Field([], data_path=["bgp", "target"], vmanage_key="route-target-ipv6")
    mpls_interface: Optional[List[MplsInterface]] = Field(data_path=["bgp"], vmanage_key="mpls-interface")
    external: Optional[int] = Field(data_path=["bgp", "distance"])
    internal: Optional[int] = Field(data_path=["bgp", "distance"])
    local: Optional[int] = Field(data_path=["bgp", "distance"])
    keepalive: Optional[int] = Field(data_path=["bgp", "timers"])
    holdtime: Optional[int] = Field(data_path=["bgp", "timers"])
    always_compare: Optional[bool] = Field(data_path=["bgp", "best-path", "med"], vmanage_key="always-compare")
    deterministic: Optional[bool] = Field(data_path=["bgp", "best-path", "med"])
    missing_as_worst: Optional[bool] = Field(data_path=["bgp", "best-path", "med"], vmanage_key="missing-as-worst")
    compare_router_id: Optional[bool] = Field(data_path=["bgp", "best-path"], vmanage_key="compare-router-id")
    multipath_relax: Optional[bool] = Field(data_path=["bgp", "best-path", "as-path"], vmanage_key="multipath-relax")
    address_family: Optional[List[AddressFamily]] = Field(data_path=["bgp"], vmanage_key="address-family")
    neighbor: Optional[List[Neighbor]] = Field(data_path=["bgp"])
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = Field(data_path=["bgp"], vmanage_key="ipv6-neighbor")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bgp"

    @validator("shutdown", "deterministic", "missing_as_worst", "compare_router_id", "multipath_relax")
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()
