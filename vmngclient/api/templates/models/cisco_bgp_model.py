from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from vmngclient.api.templates.feature_template import FeatureTemplate


class Export(BaseModel):
    asn_ip: str = Field(alias="asn-ip")
    model_config = ConfigDict(populate_by_name=True)


class Import(BaseModel):
    asn_ip: str = Field(alias="asn-ip")
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv4(BaseModel):
    vpn_id: int = Field(alias="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import", alias="import")
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv6(BaseModel):
    vpn_id: int = Field(alias="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import", alias="import")
    model_config = ConfigDict(populate_by_name=True)


class MplsInterface(BaseModel):
    if_name: Optional[str] = Field(None, alias="if-name")
    model_config = ConfigDict(populate_by_name=True)


class AddressFamilyType(str, Enum):
    IPV4_UNICAST = "ipv4-unicast"


class AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(None, alias="as-set")
    summary_only: Optional[bool] = Field(None, alias="summary-only")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("as_set", "summary_only")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class Ipv6AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(False, alias="as-set")
    summary_only: Optional[bool] = Field(False, alias="summary-only")
    model_config = ConfigDict(populate_by_name=True)


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
    route_policy: Optional[str] = Field(None, alias="route-policy")
    model_config = ConfigDict(populate_by_name=True)


class AddressFamily(BaseModel):
    family_type: AddressFamilyType = Field(alias="family-type")
    aggregate_address: Optional[List[AggregateAddress]] = Field(None, alias="aggregate-address")
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(None, alias="ipv6-aggregate-address")
    network: Optional[List[Network]] = None
    ipv6_network: Optional[List[Ipv6Network]] = Field(None, alias="ipv6-network")
    paths: Optional[int] = None
    originate: Optional[bool] = None
    name: Optional[str] = None
    filter: Optional[bool] = None
    redistribute: Optional[List[Redistribute]] = None
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("originate", "filter")
    @classmethod
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
    pol_name: str = Field(alias="pol-name")
    model_config = ConfigDict(populate_by_name=True)


class NeighborAddressFamily(BaseModel):
    family_type: NeighborFamilyType = Field(alias="family-type")
    prefix_num: Optional[int] = Field(None, alias="prefix-num")
    threshold: Optional[int] = None
    restart: Optional[int] = None
    warning_only: Optional[bool] = Field(None, alias="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(None, alias="route-policy")
    model_config = ConfigDict(populate_by_name=True)


class Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(alias="remote-as")
    keepalive: Optional[int] = None
    holdtime: Optional[int] = None
    if_name: Optional[str] = Field(None, alias="if-name")
    next_hop_self: Optional[bool] = Field(None, alias="next-hop-self")
    send_community: Optional[bool] = Field(None, alias="send-community")
    send_ext_community: Optional[bool] = Field(None, alias="send-ext-community")
    ebgp_multihop: Optional[int] = Field(None, alias="ebgp-multihop")
    password: Optional[str] = None
    send_label: Optional[bool] = Field(None, alias="send-label")
    send_label_explicit: Optional[bool] = Field(None, alias="send-label-explicit")
    as_override: Optional[bool] = Field(None, alias="as-override")
    as_number: Optional[int] = Field(None, alias="as-number")
    address_family: Optional[List[NeighborAddressFamily]] = Field(None, alias="address-family")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator(
        "shutdown",
        "next_hop_self",
        "send_community",
        "send_ext_community",
        "send_label",
        "send_label_explicit",
        "as_override",
    )
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class IPv6NeighborFamilyType(str, Enum):
    IPV6_UNICAST = "ipv6-unicast"


class IPv6NeighborAddressFamily(BaseModel):
    family_type: IPv6NeighborFamilyType = Field(alias="family-type")
    prefix_num: Optional[int] = Field(0, alias="prefix-num")
    threshold: Optional[int] = None
    restart: Optional[int] = None
    warning_only: Optional[bool] = Field(False, alias="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(None, alias="route-policy")
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(alias="remote-as")
    keepalive: Optional[int] = None
    holdtime: Optional[int] = None
    if_name: Optional[str] = Field(None, alias="if-name")
    next_hop_self: Optional[bool] = Field(False, alias="next-hop-self")
    send_community: Optional[bool] = Field(True, alias="send-community")
    send_ext_community: Optional[bool] = Field(True, alias="send-ext-community")
    ebgp_multihop: Optional[int] = Field(1, alias="ebgp-multihop")
    password: Optional[str] = None
    send_label: Optional[bool] = Field(False, alias="send-label")
    send_label_explicit: Optional[bool] = Field(False, alias="send-label-explicit")
    as_override: Optional[bool] = Field(False, alias="as-override")
    as_number: Optional[int] = Field(None, alias="as-number")
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(None, alias="address-family")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator(
        "shutdown",
        "next_hop_self",
        "send_community",
        "send_ext_community",
        "send_label",
        "send_label_explicit",
        "as_override",
    )
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class CiscoBGPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    as_num: Optional[str] = Field(alias="as-num")
    shutdown: Optional[bool]
    router_id: Optional[str] = Field(alias="router-id")
    propagate_aspath: Optional[bool] = Field(alias="propagate-aspath")
    propagate_community: Optional[bool] = Field(alias="propagate-community")
    route_target_ipv4: List[RouteTargetIpv4] = Field([], alias="route-target-ipv4")
    route_target_ipv6: List[RouteTargetIpv6] = Field([], alias="route-target-ipv6")
    mpls_interface: Optional[List[MplsInterface]] = Field(alias="mpls-interface")
    external: Optional[int]
    internal: Optional[int]
    local: Optional[int]
    keepalive: Optional[int]
    holdtime: Optional[int]
    always_compare: Optional[bool] = Field(alias="always-compare")
    deterministic: Optional[bool]
    missing_as_worst: Optional[bool] = Field(alias="missing-as-worst")
    compare_router_id: Optional[bool] = Field(alias="compare-router-id")
    multipath_relax: Optional[bool] = Field(alias="multipath-relax")
    address_family: Optional[List[AddressFamily]] = Field(alias="address-family")
    neighbor: Optional[List[Neighbor]]
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = Field(alias="ipv6-neighbor")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bgp"

    @field_validator("shutdown")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()
