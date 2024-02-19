from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.templates.feature_template import FeatureTemplate


class Export(BaseModel):
    asn_ip: str = Field(json_schema_extra={"vmanage_key": "asn-ip"})
    model_config = ConfigDict(populate_by_name=True)


class Import(BaseModel):
    asn_ip: str = Field(json_schema_extra={"vmanage_key": "asn-ip"})
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv4(BaseModel):
    vpn_id: int = Field(json_schema_extra={"vmanage_key": "vpn-id"})
    export: List[Export]
    import_: List[Import] = Field(json_schema_extra={"vmanage_key": "import"})
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv6(BaseModel):
    vpn_id: int = Field(json_schema_extra={"vmanage_key": "vpn-id"})
    export: List[Export]
    import_: List[Import] = Field(json_schema_extra={"vmanage_key": "import"})
    model_config = ConfigDict(populate_by_name=True)


class MplsInterface(BaseModel):
    if_name: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "if-name"})
    model_config = ConfigDict(populate_by_name=True)


class AddressFamilyType(str, Enum):
    IPV4_UNICAST = "ipv4-unicast"


class AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "as-set"})
    summary_only: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "summary-only"})
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("as_set", "summary_only")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class Ipv6AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "as-set"})
    summary_only: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "summary-only"})
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
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class AddressFamily(BaseModel):
    family_type: AddressFamilyType = Field(json_schema_extra={"vmanage_key": "family-type"})
    aggregate_address: Optional[List[AggregateAddress]] = Field(
        default=None, json_schema_extra={"vmanage_key": "aggregate-address"}
    )
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(
        default=None, json_schema_extra={"vmanage_key": "ipv6-aggregate-address"}
    )
    network: Optional[List[Network]] = None
    ipv6_network: Optional[List[Ipv6Network]] = Field(default=None, json_schema_extra={"vmanage_key": "ipv6-network"})
    paths: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-paths"]})
    originate: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["default-information"]})
    policy_name: Optional[str] = Field(
        default=None, json_schema_extra={"data_path": ["table-map"], "vmanage_key": "name"}
    )
    filter: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["table-map"]})
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
    pol_name: str = Field(json_schema_extra={"vmanage_key": "pol-name"})
    model_config = ConfigDict(populate_by_name=True)


class NeighborAddressFamily(BaseModel):
    family_type: NeighborFamilyType = Field(json_schema_extra={"vmanage_key": "family-type"})
    prefix_num: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"}
    )
    threshold: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    restart: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    warning_only: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"}
    )
    route_policy: Optional[List[RoutePolicy]] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(json_schema_extra={"vmanage_key": "remote-as"})
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    if_name: Optional[str] = Field(
        default=None, json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"}
    )
    next_hop_self: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "next-hop-self"})
    send_community: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "send-community"})
    send_ext_community: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "send-ext-community"})
    ebgp_multihop: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "ebgp-multihop"})
    password: Optional[str] = None
    send_label: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "send-label"})
    send_label_explicit: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "send-label-explicit"})
    as_override: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "as-override"})
    as_number: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"}
    )
    address_family: Optional[List[NeighborAddressFamily]] = Field(
        default=None, json_schema_extra={"vmanage_key": "address-family"}
    )
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
    family_type: IPv6NeighborFamilyType = Field(json_schema_extra={"vmanage_key": "family-type"})
    prefix_num: Optional[int] = Field(
        0, json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"}
    )
    threshold: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    restart: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    warning_only: Optional[bool] = Field(
        False, json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"}
    )
    route_policy: Optional[List[RoutePolicy]] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(default=None, json_schema_extra={"vmanage_key": "remote-as"})
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    if_name: Optional[str] = Field(
        default=None, json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"}
    )
    next_hop_self: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "next-hop-self"})
    send_community: Optional[bool] = Field(True, json_schema_extra={"vmanage_key": "send-community"})
    send_ext_community: Optional[bool] = Field(True, json_schema_extra={"vmanage_key": "send-ext-community"})
    ebgp_multihop: Optional[int] = Field(1, json_schema_extra={"vmanage_key": "ebgp-multihop"})
    password: Optional[str] = None
    send_label: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "send-label"})
    send_label_explicit: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "send-label-explicit"})
    as_override: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "as-override"})
    as_number: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"}
    )
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(
        default=None, json_schema_extra={"vmanage_key": "address-family"}
    )
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

    as_num: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "as-num"})
    shutdown: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["bgp"]})
    router_id: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "router-id"})
    propagate_aspath: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-aspath"}
    )
    propagate_community: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-community"}
    )
    route_target_ipv4: List[RouteTargetIpv4] = Field(
        [], json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv4"}
    )
    route_target_ipv6: List[RouteTargetIpv6] = Field(
        [], json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv6"}
    )
    mpls_interface: Optional[List[MplsInterface]] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "mpls-interface"}
    )
    external: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    internal: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    local: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "timers"]})
    always_compare: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "always-compare"}
    )
    deterministic: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["bgp", "best-path", "med"]})
    missing_as_worst: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "missing-as-worst"}
    )
    compare_router_id: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp", "best-path"], "vmanage_key": "compare-router-id"}
    )
    multipath_relax: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp", "best-path", "as-path"], "vmanage_key": "multipath-relax"}
    )
    address_family: Optional[List[AddressFamily]] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "address-family"}
    )
    neighbor: Optional[List[Neighbor]] = Field(default=None, json_schema_extra={"data_path": ["bgp"]})
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "ipv6-neighbor"}
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bgp"

    @field_validator("shutdown", "deterministic", "missing_as_worst", "compare_router_id", "multipath_relax")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()
