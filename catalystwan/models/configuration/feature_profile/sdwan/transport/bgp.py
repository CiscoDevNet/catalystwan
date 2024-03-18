# Copyright 2024 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_variable

FamilyType = Literal["ipv4-unicast", "vpnv4-unicast", "vpnv6-unicast"]
FamilyTypeIpv6 = Literal["ipv6-unicast", "vpnv6-unicast"]
Mask = Literal[
    "255.255.255.255",
    "255.255.255.254",
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0",
    "0.0.0.0",
]
PolicyTypeOff = Literal["off"]
PolicyTypeRestart = Literal["restart"]
PolicyTypeWarningDisablePeer = Literal["warning-only", "disable-peer"]
Protocol = Literal["static", "connected", "ospf", "ospfv3", "nat"]
Protocol2 = Literal["static", "connected", "ospf"]


class RefIdItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ref_id: Global[str] = Field(..., serialization_alias="refId", validation_alias="refId")


class MaxPrefixConfigDisabled(BaseModel):
    """
    Set maximum number of prefixes accepted from BGP peer and threshold exceeded policy actions(restart or warning)
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    policy_type: Global[PolicyTypeOff] = Field(
        ...,
        serialization_alias="policyType",
        validation_alias="policyType",
        description="Neighbor received maximum prefix policy is disabled.",
    )


class MaxPrefixConfigRestart(BaseModel):
    """
    Set maximum number of prefixes accepted from BGP peer and threshold exceeded policy actions(restart or warning)
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    policy_type: Global[PolicyTypeRestart] = Field(
        ...,
        serialization_alias="policyType",
        validation_alias="policyType",
        description="Neighbor maximum prefix policy is enabled,"
        "when maximum prefix threshold is exceeded, policy action is restarting device.",
    )
    prefix_num: Union[Global[int], Variable] = Field(
        ...,
        serialization_alias="prefixNum",
        validation_alias="prefixNum",
        description="Set maximum number of prefixes accepted from BGP peer",
    )
    threshold: Union[Global[int], Variable, Default[int]] = Field(
        ...,
        description="Set threshold(1 to 100) at which to generate a warning message",
    )
    restart_interval: Union[Global[int], Variable] = Field(
        ...,
        serialization_alias="restartInterval",
        validation_alias="restartInterval",
        description="Set the restart interval(minutes) when to restart BGP connection if threshold is exceeded",
    )


class MaxPrefixConfigWarningDisablePeer(BaseModel):
    """
    Set maximum number of prefixes accepted from BGP peer and threshold exceeded policy actions(restart or warning)
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    policy_type: Global[PolicyTypeWarningDisablePeer] = Field(
        ...,
        serialization_alias="policyType",
        validation_alias="policyType",
        description="Neighbor maximum prefix policy is enabled,"
        "when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.",
    )
    prefix_num: Union[Global[int], Variable] = Field(
        ...,
        serialization_alias="prefixNum",
        validation_alias="prefixNum",
        description="Set maximum number of prefixes accepted from BGP peer",
    )
    threshold: Union[Global[int], Variable, Default[int]] = Field(
        ...,
        description="Set threshold(1 to 100) at which to generate a warning message",
    )


class AddressFamilyItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    family_type: Global[FamilyType] = Field(
        ...,
        serialization_alias="familyType",
        validation_alias="familyType",
        description="Set IPv4 unicast address family",
    )
    max_prefix_config: Optional[
        Union[MaxPrefixConfigDisabled, MaxPrefixConfigRestart, MaxPrefixConfigWarningDisablePeer]
    ] = Field(
        default=None,
        serialization_alias="maxPrefixConfig",
        validation_alias="maxPrefixConfig",
        description="Set maximum number of prefixes accepted from BGP peer"
        "and threshold exceeded policy actions (restart or warning)",
    )
    in_route_policy: Optional[Union[RefIdItem, Default[None]]] = Field(
        default=None,
        serialization_alias="inRoutePolicy",
        validation_alias="inRoutePolicy",
        description="In direction route policy name",
    )
    out_route_policy: Optional[Union[RefIdItem, Default[None]]] = Field(
        default=None,
        serialization_alias="outRoutePolicy",
        validation_alias="outRoutePolicy",
        description="out direction route policy name",
    )


class NeighborItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Variable, Global[IPv4Address]] = Field(..., description="Set neighbor address")
    description: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, description="Set description"
    )
    shutdown: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="Enable or disable a BGP neighbor"
    )
    remote_as: Union[Global[str], Global[int], Variable] = Field(
        ...,
        serialization_alias="remoteAs",
        validation_alias="remoteAs",
        description="Set remote autonomous system number <1..4294967295> or <XX.YY>",
    )
    local_as: Optional[Union[Global[str], Global[int], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="localAs",
        validation_alias="localAs",
        description="Set local autonomous system number <1..4294967295> or <XX.YY>"
        "Local-AS cannot have the local BGP protocol AS number or the AS number of the remote peer."
        "The local-as is valid only if the peer is a true eBGP peer."
        "It does not work for two peers in different sub-ASs in a confederation.",
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Set how often to advertise keepalive messages to BGP peer",
    )
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Set how long to wait since receiving a keepalive message to consider BGP peer unavailable",
    )
    if_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="ifName",
        validation_alias="ifName",
        description="Source interface name for BGP neighbor",
    )
    next_hop_self: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="nextHopSelf",
        validation_alias="nextHopSelf",
        description="Set router to be next hop for routes advertised to neighbor",
    )
    send_community: Optional[Union[Variable, Global[bool], Default[Literal[True]]]] = Field(
        default=None,
        serialization_alias="sendCommunity",
        validation_alias="sendCommunity",
        description="Send community attribute",
    )
    send_ext_community: Optional[Union[Variable, Global[bool], Default[Literal[True]]]] = Field(
        default=None,
        serialization_alias="sendExtCommunity",
        validation_alias="sendExtCommunity",
        description="Send extended community attribute",
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="ebgpMultihop",
        validation_alias="ebgpMultihop",
        description="Set TTL value for peers that are not directly connected",
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        description="Set MD5 password on TCP connection with BGP peer"
        "[Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    send_label: Optional[Union[Global[bool], Default[Literal[False]]]] = Field(
        default=None, serialization_alias="sendLabel", validation_alias="sendLabel", description="Send label"
    )
    send_label_explicit: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="sendLabelExplicit",
        validation_alias="sendLabelExplicit",
        description="Send explicit null label",
    )
    as_override: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="asOverride",
        validation_alias="asOverride",
        description="Override matching AS-number while sending update",
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="asNumber",
        validation_alias="asNumber",
        description="The number of accept as-path with my AS present in it",
    )
    address_family: Optional[List[AddressFamilyItem]] = Field(
        default=None,
        serialization_alias="addressFamily",
        validation_alias="addressFamily",
        description="Set BGP address family",
        max_length=3,
    )


class VariableFamilyItem1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    family_type: Global[FamilyTypeIpv6] = Field(
        ...,
        serialization_alias="familyType",
        validation_alias="familyType",
        description="Set IPv6 unicast address family",
    )
    max_prefix_config: Optional[
        Union[MaxPrefixConfigDisabled, MaxPrefixConfigRestart, MaxPrefixConfigWarningDisablePeer]
    ] = Field(
        default=None,
        serialization_alias="maxPrefixConfig",
        validation_alias="maxPrefixConfig",
        description="Set maximum number of prefixes accepted from BGP peer and"
        "threshold exceeded policy actions(restart or warning)",
    )
    in_route_policy: Optional[Union[Default[None], RefIdItem]] = Field(
        default=None,
        serialization_alias="inRoutePolicy",
        validation_alias="inRoutePolicy",
        description="In direction route policy name",
    )
    out_route_policy: Optional[Union[Default[None], RefIdItem]] = Field(
        default=None,
        serialization_alias="outRoutePolicy",
        validation_alias="outRoutePolicy",
        description="out direction route policy name",
    )


class Ipv6NeighborItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Global[IPv6Address], Variable] = Field(..., description="Set IPv6 neighbor address")
    description: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, description="Set description"
    )
    shutdown: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="Enable or disable a BGP neighbor"
    )
    remote_as: Union[Global[str], Global[int], Variable] = Field(
        ...,
        serialization_alias="remoteAs",
        validation_alias="remoteAs",
        description="Set remote autonomous system number <1..4294967295> or <XX.YY>",
    )
    local_as: Optional[Union[Global[str], Global[int], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="localAs",
        validation_alias="localAs",
        description="Set local autonomous number <1..4294967295> or <XX.YY>"
        "Local-AS cannot have the local BGP protocol AS number or the AS number of the remote peer."
        "The local-as is valid only if the peer is a true eBGP peer."
        "It does not work for two peers in different sub-ASs in a confederation.",
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Interval (seconds) of keepalive messages sent to its BGP peer",
    )
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Interval (seconds) not receiving a keepalive message declares a BGP peer down",
    )
    if_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="ifName",
        validation_alias="ifName",
        description="Source interface name for BGP neighbor",
    )
    next_hop_self: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="nextHopSelf",
        validation_alias="nextHopSelf",
        description="Set router to be next hop for routes advertised to neighbor",
    )
    send_community: Optional[Union[Variable, Global[bool], Default[Literal[True]]]] = Field(
        default=None,
        serialization_alias="sendCommunity",
        validation_alias="sendCommunity",
        description="Send community attribute",
    )
    send_ext_community: Optional[Union[Variable, Global[bool], Default[Literal[True]]]] = Field(
        default=None,
        serialization_alias="sendExtCommunity",
        validation_alias="sendExtCommunity",
        description="Send extended community attribute",
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        serialization_alias="ebgpMultihop",
        validation_alias="ebgpMultihop",
        description="Set TTL value for peers that are not directly connected",
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None,
        description="Set MD5 password on TCP connection with BGP peer"
        "[Note: Catalyst SD-WAN Manager will encrypt this field before saving."
        "Cleartext strings will not be returned back to the user in GET responses for sensitive fields.]",
    )
    as_override: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="asOverride",
        validation_alias="asOverride",
        description="Override matching AS-number while sending update",
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="asNumber",
        validation_alias="asNumber",
        description="The number of accept as-path with my AS present in it",
    )
    address_family: Optional[List[VariableFamilyItem1]] = Field(
        default=None,
        serialization_alias="addressFamily",
        validation_alias="addressFamily",
        description="Set IPv6 BGP address family",
        max_length=2,
    )


class Prefix(BaseModel):
    """
    Configure the IPv4 prefixes to aggregate
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Variable, Global[IPv4Address]]
    mask: Union[Variable, Global[Mask]]


class AggregateAddres(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Prefix = Field(..., description="Configure the IPv4 prefixes to aggregate")
    as_set: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, serialization_alias="asSet", validation_alias="asSet", description="Set AS set path information"
    )
    summary_only: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="summaryOnly",
        validation_alias="summaryOnly",
        description="Variable out more specific routes from updates",
    )


class Prefix1(BaseModel):
    """
    Configure the prefixes for BGP to announce
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Variable, Global[IPv4Address]]
    mask: Union[Variable, Global[Mask]]


class NetworkItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Prefix1 = Field(..., description="Configure the prefixes for BGP to announce")


class RedistributeItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    protocol: Union[Global[Protocol], Variable] = Field(..., description="Set the protocol to redistribute routes from")
    route_policy: Optional[Union[Default[None], RefIdItem]] = Field(
        default=None,
        serialization_alias="routePolicy",
        validation_alias="routePolicy",
        description="Configure policy to apply to prefixes received from BGP neighbor",
    )


class AddressFamily(BaseModel):
    """
    Set IPv4 unicast BGP address family
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    aggregate_address: Optional[List[AggregateAddres]] = Field(
        default=None,
        serialization_alias="aggregateVariable",
        validation_alias="aggregateVariable",
        description="Aggregate prefixes in specific range",
    )
    network: Optional[List[NetworkItem]] = Field(
        default=None, description="Configure the networks for BGP to advertise"
    )
    paths: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        description="Set maximum number of parallel IBGP paths for multipath load sharing",
    )
    originate: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="BGP Default Information Variable"
    )
    name: Optional[Union[Default[None], RefIdItem]] = Field(default=None, description="Table Map Policy name")
    filter: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="Table map filtered or not"
    )
    redistribute: Optional[List[RedistributeItem]] = Field(
        default=None, description="Redistribute routes into BGP", max_length=7
    )


class Ipv6AggregateAddres(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Union[Global[str], Variable] = Field(..., description="Configure the IPv6 prefixes to aggregate")
    as_set: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, serialization_alias="asSet", validation_alias="asSet", description="Set AS set path information"
    )
    summary_only: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="summaryOnly",
        validation_alias="summaryOnly",
        description="Variable out more specific routes from updates",
    )


class Ipv6NetworkItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Union[Global[str], Variable] = Field(..., description="Configure the prefixes for BGP to announce")


class Ipv6RedistributeItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    protocol: Union[Global[Protocol2], Variable] = Field(
        ..., description="Set the protocol to redistribute routes from"
    )
    route_policy: Optional[Union[Default[None], RefIdItem]] = Field(
        default=None,
        serialization_alias="routePolicy",
        validation_alias="routePolicy",
        description="Configure policy to apply to prefixes received from BGP neighbor",
    )


class Ipv6AddressFamily(BaseModel):
    """
    Set BGP address family
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddres]] = Field(
        default=None,
        serialization_alias="ipv6AggregateVariable",
        validation_alias="ipv6AggregateVariable",
        description="IPv6 Aggregate prefixes in specific range",
    )
    ipv6_network: Optional[List[Ipv6NetworkItem]] = Field(
        default=None,
        serialization_alias="ipv6Network",
        validation_alias="ipv6Network",
        description="Configure the networks for BGP to advertise",
    )
    paths: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        description="Set maximum number of parallel IBGP paths for multipath load sharing",
    )
    originate: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="BGP Default Information Variable"
    )
    name: Optional[Union[Default[None], RefIdItem]] = Field(default=None, description="Table Map Policy name")
    filter: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None, description="Table map filtered or not"
    )
    redistribute: Optional[List[Ipv6RedistributeItem]] = Field(
        default=None, description="Redistribute routes into BGP", max_length=5
    )


class MplsInterfaceItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    if_name: Union[Global[str], Variable] = Field(
        ..., serialization_alias="ifName", validation_alias="ifName", description="Interface Name"
    )


class WanRoutingBgpParcel(_ParcelBase):
    type_: Literal["bgp"] = Field(default="bgp", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    as_num: Union[Global[int], Global[str], Variable] = Field(
        default=as_variable("{{lbgp_1_basicConf_asNumber}}"),
        serialization_alias="asNum",
        validation_alias="asNum",
        description="Set autonomous system number <1..4294967295> or <XX.YY>",
    )
    router_id: Optional[Union[Global[IPv4Address], Variable, Default[None]]] = Field(
        default=None,
        serialization_alias="routerId",
        validation_alias="routerId",
        description="Configure BGP router identifier",
    )
    propagate_aspath: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="propagateAspath",
        validation_alias="propagateAspath",
        description="Propagate AS Path",
    )
    propagate_community: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="propagateCommunity",
        validation_alias="propagateCommunity",
        description="Propagate Community",
    )
    external: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, description="Set administrative distance for external BGP routes"
    )
    internal: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, description="Set administrative distance for internal BGP routes"
    )
    local: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, description="Set administrative distance for local BGP routes"
    )
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Interval (seconds) of keepalive messages sent to its BGP peer",
    )
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None,
        description="Interval (seconds) not receiving a keepalive message declares a BGP peer down",
    )
    always_compare: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="alwaysCompare",
        validation_alias="alwaysCompare",
        description="Compare MEDs from all ASs when selecting active BGP paths",
    )
    deterministic: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        description="Compare MEDs from all routes from same AS when selecting active BGP paths",
    )
    missing_as_worst: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="missingAsWorst",
        validation_alias="missingAsWorst",
        description="If path has no MED, consider it to be worst path when selecting active BGP paths",
    )
    compare_router_id: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="compareGlobal[ipaddress.IPv4Variable]",
        validation_alias="compareGlobal[ipaddress.IPv4Variable]",
        description="Compare router IDs when selecting active BGP paths",
    )
    multipath_relax: Optional[Union[Variable, Global[bool], Default[Literal[False]]]] = Field(
        default=None,
        serialization_alias="multipathRelax",
        validation_alias="multipathRelax",
        description="Ignore AS for multipath selection",
    )
    neighbor: Optional[List[NeighborItem]] = Field(default=None, description="Set BGP IPv4 neighbors")
    ipv6_neighbor: Optional[List[Ipv6NeighborItem]] = Field(
        default=None,
        serialization_alias="ipv6Neighbor",
        validation_alias="ipv6Neighbor",
        description="Set BGP IPv6 neighbors",
    )
    address_family: Optional[AddressFamily] = Field(
        default=None,
        serialization_alias="addressFamily",
        validation_alias="addressFamily",
        description="Set IPv4 unicast BGP address family",
    )
    ipv6_address_family: Optional[Ipv6AddressFamily] = Field(
        default=None,
        serialization_alias="ipv6VariableFamily",
        validation_alias="ipv6VariableFamily",
        description="Set BGP address family",
    )
    mpls_interface: Optional[List[MplsInterfaceItem]] = Field(
        default=None,
        serialization_alias="mplsInterface",
        validation_alias="mplsInterface",
        description="MPLS BGP Interface",
    )
