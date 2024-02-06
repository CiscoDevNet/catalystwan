from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId
from catalystwan.models.configuration.feature_profile.common import Prefix


class AggregatePrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    as_set: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="asSet", default=Default[bool](value=False)
    )
    summary_only: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="summaryOnly", default=Default[bool](value=False)
    )


class AggregatePrefixIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Union[Global[str], Variable]
    as_set: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="asSet", default=Default[bool](value=False)
    )
    summary_only: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="summaryOnly", default=Default[bool](value=False)
    )


class NetworkPrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix


class NetworkPrefixIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Union[Global[str], Variable]


class RedistributeProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    OMP = "omp"
    NAT = "nat"
    OSPF = "ospf"
    OSPFV3 = "ospfv3"
    EIGRP = "eigrp"


class RedistributeProtocolIPv6(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    OMP = "omp"
    OSPF = "ospf"


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocol], Variable]
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy")


class RedistributedRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocolIPv6], Variable]
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy")


class AddressFamilyIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    aggregate_address: Optional[List[AggregatePrefix]] = Field(alias="aggregateAddress")
    network: Optional[List[NetworkPrefix]] = None
    paths: Optional[Union[Global[int], Variable, Default[None]]] = None
    originate: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    name: Optional[Union[Default[None], RefId]] = None
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    redistribute: Optional[List[RedistributedRoute]] = None


class PolicyType(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    policy_type: Global[str] = Field(alias="policyType")


class PolicyTypeWithThreshold(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    policy_type: Global[str] = Field(alias="policyType")
    prefix_number: Union[Global[int], Variable] = Field(alias="prefixNum")
    threshold: Union[Global[int], Variable, Default[int]] = Default[int](value=75)


class PolicyTypeWithRestart(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    policy_type: Global[str] = Field(alias="policyType")
    prefix_number: Union[Global[int], Variable] = Field(alias="prefixNum")
    threshold: Union[Global[int], Variable, Default[int]] = Default[int](value=75)
    restart_interval: Union[Global[int], Variable]


class AddressFamilyIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    aggregate_address: Optional[List[AggregatePrefixIPv6]] = Field(alias="ipv6AggregateAddress")
    network: Optional[List[NetworkPrefixIPv6]] = Field(alias="ipv6Network")
    paths: Optional[Union[Global[int], Variable, Default[None]]] = None
    originate: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    name: Optional[Union[Default[None], RefId]] = None
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    redistribute: Optional[List[RedistributedRouteIPv6]] = None


class BgpAddressFamily(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    family_type: Global[str] = Field(alias="familyType")
    max_prefix_config: Optional[Union[PolicyType, PolicyTypeWithRestart, PolicyTypeWithThreshold]] = Field(
        alias="maxPrefixConfig"
    )
    in_route_policy: Optional[Union[Default[None], RefId]] = Field(alias="inRoutePolicy")
    out_route_policy: Optional[Union[Default[None], RefId]] = Field(alias="outRoutePolicy")


class BgpIPv4Neighbor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable]
    description: Optional[Union[Global[str], Variable, Default[None]]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    remote_as: Union[Global[int], Variable] = Field(alias="remoteAs")
    local_as: Union[Global[int], Variable] = Field(alias="localAs", default=None)
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=180)
    interface_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="ifName", default=None)
    next_hop_self: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="nextHopSelf", default=Default[bool](value=False)
    )
    send_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendCommunity", default=Default[bool](value=True)
    )
    send_ext_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendExtCommunity", default=Default[bool](value=True)
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ebgpMultihop", default=Default[int](value=1)
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = None
    send_label: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendLabel", default=Default[bool](value=False)
    )
    as_override: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="asOverride", default=Default[bool](value=False)
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="asNumber", default=None)
    address_family: Optional[BgpAddressFamily] = Field(alias="addressFamily")


class BgpIPv6Neighbor(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Global[str], Variable]
    description: Optional[Union[Global[str], Variable, Default[None]]] = None
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    remote_as: Union[Global[int], Variable] = Field(alias="remoteAs")
    local_as: Union[Global[int], Variable] = Field(alias="localAs", default=None)
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=180)
    interface_name: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="ifName", default=None)
    next_hop_self: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="nextHopSelf", default=Default[bool](value=False)
    )
    send_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendCommunity", default=Default[bool](value=True)
    )
    send_ext_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendExtCommunity", default=Default[bool](value=True)
    )
    ebgp_multihop: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="ebgpMultihop", default=Default[int](value=1)
    )
    password: Optional[Union[Global[str], Variable, Default[None]]] = None
    send_label: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="sendLabel", default=Default[bool](value=False)
    )
    as_override: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="asOverride", default=Default[bool](value=False)
    )
    as_number: Optional[Union[Global[int], Variable, Default[None]]] = Field(alias="asNumber", default=None)
    address_family: Optional[BgpAddressFamily] = Field(alias="addressFamily")


class BgpData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    as_num: Union[Global[int], Variable] = Field(alias="asNum")
    router_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="routerId", default=None)
    propagate_aspath: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="propagateAspath", default=Default[bool](value=False)
    )
    propagate_community: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="propagateCommunity", default=Default[bool](value=False)
    )
    external: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=20)
    internal: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=200)
    local: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=20)
    keepalive: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=60)
    holdtime: Optional[Union[Global[int], Variable, Default[int]]] = Default[int](value=180)
    always_compare: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="alwaysCompare", default=Default[bool](value=False)
    )
    deterministic: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    missing_as_worst: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="missingAsWorst", default=Default[bool](value=False)
    )
    compare_router_id: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="compareRouterId", default=Default[bool](value=False)
    )
    multipath_relax: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="multipathRelax", default=Default[bool](value=False)
    )
    neighbor: Optional[List[BgpIPv4Neighbor]] = None
    ipv6_neighbor: Optional[List[BgpIPv6Neighbor]] = Field(alias="ipv6Neighbor", default=None)
    address_family: Optional[AddressFamilyIPv4] = Field(alias="addressFamily", default=None)
    ipv6_address_family: Optional[AddressFamilyIPv6] = Field(alias="ipv6AddressFamily", default=None)


class BgpCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: BgpData
    metadata: Optional[dict] = None
