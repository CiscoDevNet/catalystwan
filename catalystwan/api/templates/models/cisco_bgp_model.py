from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.templates.feature_template import FeatureTemplate

NeighborFamilyType = Literal["ipv4-unicast", "vpnv4-unicast", "vpnv6-unicast"]
Direction = Literal["in", "out"]
AddressFamilyType = Literal["ipv4-unicast"]
IPv6NeighborFamilyType = Literal["ipv6-unicast"]


class Export(BaseModel):
    asn_ip: str = Field(
        validation_alias="asn-ip", serialization_alias="asn-ip", json_schema_extra={"vmanage_key": "asn-ip"}
    )
    model_config = ConfigDict(populate_by_name=True)


class Import(BaseModel):
    asn_ip: str = Field(
        validation_alias="asn-ip", serialization_alias="asn-ip", json_schema_extra={"vmanage_key": "asn-ip"}
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv4(BaseModel):
    vpn_id: int = Field(
        serialization_alias="vpn-id", validation_alias="vpn-id", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    export: List[Export]
    import_: List[Import] = Field(json_schema_extra={"vmanage_key": "import"})
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv6(BaseModel):
    vpn_id: int = Field(
        serialization_alias="vpn-id", validation_alias="vpn-id", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    export: List[Export]
    import_: List[Import] = Field(json_schema_extra={"vmanage_key": "import"})
    model_config = ConfigDict(populate_by_name=True)


class MplsInterface(BaseModel):
    if_name: Optional[str] = Field(
        serialization_alias="if-name",
        validation_alias="if-name",
        default=None,
        json_schema_extra={"vmanage_key": "if-name"},
    )
    model_config = ConfigDict(populate_by_name=True)


class AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(
        default=None,
        serialization_alias="as-set",
        validation_alias="as-set",
        json_schema_extra={"vmanage_key": "as-set"},
    )
    summary_only: Optional[bool] = Field(
        default=None,
        serialization_alias="summary-only",
        validation_alias="summary-only",
        json_schema_extra={"vmanage_key": "summary-only"},
    )
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("as_set", "summary_only")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class Ipv6AggregateAddress(BaseModel):
    prefix: str
    as_set: Optional[bool] = Field(
        default=False,
        serialization_alias="as-set",
        validation_alias="as-set",
        json_schema_extra={"vmanage_key": "as-set"},
    )
    summary_only: Optional[bool] = Field(
        default=False,
        serialization_alias="summary-only",
        validation_alias="summary-only",
        json_schema_extra={"vmanage_key": "summary-only"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Network(BaseModel):
    prefix: str


class Ipv6Network(BaseModel):
    prefix: str


Protocol = Literal["static", "connected", "ospf", "ospfv3", "omp", "nat", "eigrp"]


class Redistribute(BaseModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class AddressFamily(BaseModel):
    family_type: AddressFamilyType = Field(
        serialization_alias="family-type",
        validation_alias="family-type",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    aggregate_address: Optional[List[AggregateAddress]] = Field(
        default=None,
        serialization_alias="aggregate-address",
        validation_alias="aggregate-address",
        json_schema_extra={"vmanage_key": "aggregate-address"},
    )
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(
        default=None,
        serialization_alias="ipv6-aggregate-address",
        validation_alias="ipv6-aggregate-address",
        json_schema_extra={"vmanage_key": "ipv6-aggregate-address"},
    )
    network: Optional[List[Network]] = None
    ipv6_network: Optional[List[Ipv6Network]] = Field(
        default=None,
        serialization_alias="ipv6-network",
        validation_alias="ipv6-network",
        json_schema_extra={"vmanage_key": "ipv6-network"},
    )
    paths: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-paths"]})
    originate: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["default-information"]})
    policy_name: Optional[str] = Field(
        default=None,
        serialization_alias="name",
        validation_alias="name",
        json_schema_extra={"data_path": ["table-map"], "vmanage_key": "name"},
    )
    filter: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["table-map"]})
    redistribute: Optional[List[Redistribute]] = None
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("originate", "filter")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()


class RoutePolicy(BaseModel):
    direction: Direction
    pol_name: str = Field(
        validation_alias="pol-name", serialization_alias="pol-name", json_schema_extra={"vmanage_key": "pol-name"}
    )
    model_config = ConfigDict(populate_by_name=True)


class NeighborAddressFamily(BaseModel):
    family_type: NeighborFamilyType = Field(
        serialization_alias="family-type",
        validation_alias="family-type",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    prefix_num: Optional[int] = Field(
        default=None,
        serialization_alias="prefix-num",
        validation_alias="prefix-num",
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"},
    )
    threshold: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    restart: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    warning_only: Optional[bool] = Field(
        default=None,
        serialization_alias="warning-only",
        validation_alias="warning-only",
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(
        validation_alias="remote-as", serialization_alias="remote-as", json_schema_extra={"vmanage_key": "remote-as"}
    )
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    if_name: Optional[str] = Field(
        default=None,
        validation_alias="if-name",
        serialization_alias="if-name",
        json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"},
    )
    next_hop_self: Optional[bool] = Field(
        default=None,
        validation_alias="next-hop-self",
        serialization_alias="next-hop-self",
        json_schema_extra={"vmanage_key": "next-hop-self"},
    )
    send_community: Optional[bool] = Field(
        default=None,
        validation_alias="send-community",
        serialization_alias="send-community",
        json_schema_extra={"vmanage_key": "send-community"},
    )
    send_ext_community: Optional[bool] = Field(
        default=None,
        validation_alias="send-ext-community",
        serialization_alias="send-ext-community",
        json_schema_extra={"vmanage_key": "send-ext-community"},
    )
    ebgp_multihop: Optional[int] = Field(
        default=None,
        validation_alias="ebgp-multihop",
        serialization_alias="ebgp-multihop",
        json_schema_extra={"vmanage_key": "ebgp-multihop"},
    )
    password: Optional[str] = None
    send_label: Optional[bool] = Field(
        default=None,
        validation_alias="send-label",
        serialization_alias="send-label",
        json_schema_extra={"vmanage_key": "send-label"},
    )
    send_label_explicit: Optional[bool] = Field(
        default=None,
        validation_alias="send-label-explicit",
        serialization_alias="send-label-explicit",
        json_schema_extra={"vmanage_key": "send-label-explicit"},
    )
    as_override: Optional[bool] = Field(
        default=None,
        validation_alias="as-override",
        serialization_alias="as-override",
        json_schema_extra={"vmanage_key": "as-override"},
    )
    as_number: Optional[int] = Field(
        default=None,
        validation_alias="as-number",
        serialization_alias="as-number",
        json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"},
    )
    address_family: Optional[List[NeighborAddressFamily]] = Field(
        default=None,
        validation_alias="address-family",
        serialization_alias="address-family",
        json_schema_extra={"vmanage_key": "address-family"},
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


class IPv6NeighborAddressFamily(BaseModel):
    family_type: IPv6NeighborFamilyType = Field(
        serialization_alias="family-type",
        validation_alias="family-type",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    prefix_num: Optional[int] = Field(
        default=0,
        serialization_alias="prefix-num",
        validation_alias="prefix-num",
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"},
    )
    threshold: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    restart: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["maximum-prefixes"]})
    warning_only: Optional[bool] = Field(
        default=False,
        serialization_alias="warning-only",
        validation_alias="warning-only",
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        validation_alias="route-policy",
        serialization_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Neighbor(BaseModel):
    address: str
    description: Optional[str] = None
    shutdown: Optional[bool] = None
    remote_as: int = Field(
        default=None,
        validation_alias="remote-as",
        serialization_alias="remote-as",
        json_schema_extra={"vmanage_key": "remote-as"},
    )
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["timers"]})
    if_name: Optional[str] = Field(
        default=None,
        validation_alias="if-name",
        serialization_alias="if-name",
        json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"},
    )
    next_hop_self: Optional[bool] = Field(
        default=False,
        serialization_alias="next-hop-self",
        validation_alias="next-hop-self",
        json_schema_extra={"vmanage_key": "next-hop-self"},
    )
    send_community: Optional[bool] = Field(
        default=True,
        serialization_alias="send-community",
        validation_alias="send-community",
        json_schema_extra={"vmanage_key": "send-community"},
    )
    send_ext_community: Optional[bool] = Field(
        default=True,
        serialization_alias="send-ext-community",
        validation_alias="send-ext-community",
        json_schema_extra={"vmanage_key": "send-ext-community"},
    )
    ebgp_multihop: Optional[int] = Field(
        default=1,
        serialization_alias="ebgp-multihop",
        validation_alias="ebgp-multihop",
        json_schema_extra={"vmanage_key": "ebgp-multihop"},
    )
    password: Optional[str] = None
    send_label: Optional[bool] = Field(
        default=False,
        validation_alias="send-label",
        serialization_alias="send-label",
        json_schema_extra={"vmanage_key": "send-label"},
    )
    send_label_explicit: Optional[bool] = Field(
        default=False,
        validation_alias="send-label-explicit",
        serialization_alias="send-label-explicit",
        json_schema_extra={"vmanage_key": "send-label-explicit"},
    )
    as_override: Optional[bool] = Field(
        default=False,
        validation_alias="as-override",
        serialization_alias="as-override",
        json_schema_extra={"vmanage_key": "as-override"},
    )
    as_number: Optional[int] = Field(
        default=None,
        validation_alias="as-number",
        serialization_alias="as-number",
        json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"},
    )
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(
        default=None,
        validation_alias="address-family",
        serialization_alias="address-family",
        json_schema_extra={"vmanage_key": "address-family"},
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

    as_num: Optional[str] = Field(
        default=None,
        serialization_alias="as-num",
        validation_alias="as-num",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "as-num"},
    )
    shutdown: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["bgp"]})
    router_id: Optional[str] = Field(
        default=None,
        serialization_alias="router-id",
        validation_alias="router-id",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "router-id"},
    )
    propagate_aspath: Optional[bool] = Field(
        default=None,
        serialization_alias="propagate-aspath",
        validation_alias="propagate-aspath",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-aspath"},
    )
    propagate_community: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-community"}
    )
    route_target_ipv4: List[RouteTargetIpv4] = Field(
        default=[],
        validation_alias="route-target-ipv4",
        serialization_alias="route-target-ipv4",
        json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv4"},
    )
    route_target_ipv6: List[RouteTargetIpv6] = Field(
        default=[],
        validation_alias="route-target-ipv6",
        serialization_alias="route-target-ipv6",
        json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv6"},
    )
    mpls_interface: Optional[List[MplsInterface]] = Field(
        default=None,
        validation_alias="mpls-interface",
        serialization_alias="mpls-interface",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "mpls-interface"},
    )
    external: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    internal: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    local: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "distance"]})
    keepalive: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "timers"]})
    holdtime: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["bgp", "timers"]})
    always_compare: Optional[bool] = Field(
        default=None,
        serialization_alias="always-compare",
        validation_alias="always-compare",
        json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "always-compare"},
    )
    deterministic: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["bgp", "best-path", "med"]})
    missing_as_worst: Optional[bool] = Field(
        default=None,
        validation_alias="missing-as-worst",
        serialization_alias="missing-as-worst",
        json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "missing-as-worst"},
    )
    compare_router_id: Optional[bool] = Field(
        default=None,
        validation_alias="compare-router-id",
        serialization_alias="compare-router-id",
        json_schema_extra={"data_path": ["bgp", "best-path"], "vmanage_key": "compare-router-id"},
    )
    multipath_relax: Optional[bool] = Field(
        default=None,
        validation_alias="multipath-relax",
        serialization_alias="multipath-relax",
        json_schema_extra={"data_path": ["bgp", "best-path", "as-path"], "vmanage_key": "multipath-relax"},
    )
    address_family: Optional[List[AddressFamily]] = Field(
        default=None,
        validation_alias="address-family",
        serialization_alias="address-family",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "address-family"},
    )
    neighbor: Optional[List[Neighbor]] = Field(default=None, json_schema_extra={"data_path": ["bgp"]})
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = Field(
        default=None,
        validation_alias="ipv6-neighbor",
        serialization_alias="ipv6-neighbor",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "ipv6-neighbor"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bgp"

    @field_validator("shutdown", "deterministic", "missing_as_worst", "compare_router_id", "multipath_relax")
    @classmethod
    def cast_to_str(cls, value):
        if value is not None:
            return str(value).lower()
