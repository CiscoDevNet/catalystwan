from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.api.templates.feature_template import FeatureTemplate


class Export(BaseModel):
    asn_ip: str = Field(alias="asn-ip")

    class Config:
        allow_population_by_field_name = True


class Import(BaseModel):
    asn_ip: str = Field(alias="asn-ip")

    class Config:
        allow_population_by_field_name = True


class RouteTargetIpv4(BaseModel):
    vpn_id: int = Field(alias="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import", alias="import")

    class Config:
        allow_population_by_field_name = True


class RouteTargetIpv6(BaseModel):
    vpn_id: int = Field(alias="vpn-id")
    export: List[Export]
    import_: List[Import] = Field(vmanage_key="import", alias="import")

    class Config:
        allow_population_by_field_name = True


class MplsInterface(BaseModel):
    if_name: Optional[str] = Field(alias="if-name")

    class Config:
        allow_population_by_field_name = True


class AddressFamilyType(str, Enum):
    IPV4_UNICAST = "ipv4-unicast"


class AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(alias="as-set")
    summary_only: Optional[bool] = Field(alias="summary-only")

    class Config:
        allow_population_by_field_name = True

    @validator("as_set", "summary_only")
    def cast_to_str(cls, value):
        if not value:
            return
        return str(value).lower()


class Ipv6AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(False, alias="as-set")
    summary_only: Optional[bool] = Field(False, alias="summary-only")

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
    route_policy: Optional[str] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class AddressFamily(BaseModel):
    family_type: AddressFamilyType = Field(alias="family-type")
    aggregate_address: Optional[List[AggregateAddress]] = Field(alias="aggregate-address")
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(alias="ipv6-aggregate-address")
    network: Optional[List[Network]]
    ipv6_network: Optional[List[Ipv6Network]] = Field(alias="ipv6-network")
    paths: Optional[int]
    originate: Optional[bool]
    name: Optional[str]
    filter: Optional[bool]
    redistribute: Optional[List[Redistribute]]

    class Config:
        allow_population_by_field_name = True

    @validator("originate", "filter")
    def cast_to_str(cls, value):
        if not value:
            return
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

    class Config:
        allow_population_by_field_name = True


class NeighborAddressFamily(BaseModel):
    family_type: NeighborFamilyType = Field(alias="family-type")
    prefix_num: Optional[int] = Field(alias="prefix-num")
    threshold: Optional[int]
    restart: Optional[int]
    warning_only: Optional[bool] = Field(alias="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class Neighbor(BaseModel):
    address: str
    description: Optional[str]
    shutdown: Optional[bool]
    remote_as: int = Field(alias="remote-as")
    keepalive: Optional[int]
    holdtime: Optional[int]
    if_name: Optional[str] = Field(alias="if-name")
    next_hop_self: Optional[bool] = Field(alias="next-hop-self")
    send_community: Optional[bool] = Field(alias="send-community")
    send_ext_community: Optional[bool] = Field(alias="send-ext-community")
    ebgp_multihop: Optional[int] = Field(alias="ebgp-multihop")
    password: Optional[str]
    send_label: Optional[bool] = Field(alias="send-label")
    send_label_explicit: Optional[bool] = Field(alias="send-label-explicit")
    as_override: Optional[bool] = Field(alias="as-override")
    as_number: Optional[int] = Field(alias="as-number")
    address_family: Optional[List[NeighborAddressFamily]] = Field(alias="address-family")

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
        if not value:
            return
        return str(value).lower()


class IPv6NeighborFamilyType(str, Enum):
    IPV6_UNICAST = "ipv6-unicast"


class IPv6NeighborAddressFamily(BaseModel):
    family_type: IPv6NeighborFamilyType = Field(alias="family-type")
    prefix_num: Optional[int] = Field(0, alias="prefix-num")
    threshold: Optional[int]
    restart: Optional[int]
    warning_only: Optional[bool] = Field(False, alias="warning-only")
    route_policy: Optional[List[RoutePolicy]] = Field(alias="route-policy")

    class Config:
        allow_population_by_field_name = True


class Ipv6Neighbor(BaseModel):
    address: str
    description: Optional[str]
    shutdown: Optional[bool]
    remote_as: int = Field(alias="remote-as")
    keepalive: Optional[int]
    holdtime: Optional[int]
    if_name: Optional[str] = Field(alias="if-name")
    next_hop_self: Optional[bool] = Field(False, alias="next-hop-self")
    send_community: Optional[bool] = Field(True, alias="send-community")
    send_ext_community: Optional[bool] = Field(True, alias="send-ext-community")
    ebgp_multihop: Optional[int] = Field(1, alias="ebgp-multihop")
    password: Optional[str]
    send_label: Optional[bool] = Field(False, alias="send-label")
    send_label_explicit: Optional[bool] = Field(False, alias="send-label-explicit")
    as_override: Optional[bool] = Field(False, alias="as-override")
    as_number: Optional[int] = Field(alias="as-number")
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(alias="address-family")

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
        if not value:
            return
        return str(value).lower()


class CiscoBGPModel(FeatureTemplate):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

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

    @validator("shutdown")
    def cast_to_str(cls, value):
        if not value:
            return
        return str(value).lower()
