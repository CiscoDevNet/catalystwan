from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global
from catalystwan.models.configuration.common import RefId


class Action(str, Enum):
    REJECT = "reject"
    ACCEPT = "accept"


class Protocol(str, Enum):
    IPV4 = "IPV4"
    IPV6 = "IPV6"
    BOTH = "BOTH"


class Criteria(str, Enum):
    OR = "or"
    AND = "and"
    EXACT = "exact"


class StandardCommunityList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    criteria: Union[Global[Criteria], Default[Criteria]] = Default[Criteria](value=Criteria.OR)
    standard_community_list: List[RefId] = Field(alias="standardCommunityList")


class ExpandedCommunityList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    expanded_community_list: RefId = Field(alias="expandedCommunityList")


class RoutePolicyMatch(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    as_path_list: Optional[RefId] = Field(alias="asPathList", default=None)
    community_list: Optional[Union[StandardCommunityList, ExpandedCommunityList]] = Field(
        alias="communityList", default=None
    )
    ext_community_list: Optional[RefId] = Field(alias="extCommunityList", default=None)
    bgp_local_preference: Optional[Global[int]] = Field(alias="bgpLocalPreference", default=None)
    metric: Optional[Global[int]] = None
    omp_tag: Optional[Global[int]] = Field(alias="ompTag", default=None)
    ospf_tag: Optional[Global[int]] = Field(alias="ospfTag", default=None)
    ipv4_address: Optional[RefId] = Field(alias="ipv4Address", default=None)
    ipv4_nexthop: Optional[RefId] = Field(alias="ipv4NextHop", default=None)
    ipv6_address: Optional[RefId] = Field(alias="ipv6Address", default=None)
    ipv6_nexthop: Optional[RefId] = Field(alias="ipv6NextHop", default=None)


class MetricType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


class Origin(str, Enum):
    EGP = "egp"
    IGP = "igp"
    INCOMPLETE = "incomplete"


class AcceptAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    enable_accept_action: Default[bool] = Default[bool](value=True)
    set_as_path: Optional[Global[int]] = Field(alias="setAsPath", default=None)
    set_community: Optional[Union[Global[bool], Default[bool]]] = Field(alias="setCommunity", default=None)
    set_local_preference: Optional[Global[int]] = Field(alias="setLocalPreference", default=None)
    set_metric: Optional[Global[int]] = Field(alias="setMetric", default=None)
    set_metric_type: Optional[Global[MetricType]] = Field(alias="setMetricType", default=None)
    set_omp_tag: Optional[Global[int]] = Field(alias="setOmpTag", default=None)
    set_origin: Optional[Global[Origin]] = Field(alias="setOrigin", default=None)
    set_ospf_tag: Optional[Global[int]] = Field(alias="setOspfTag", default=None)
    set_weight: Optional[Global[int]] = Field(alias="setWeight", default=None)
    set_ipv4_nexthop: Optional[Global[str]] = Field(alias="setIpv4NextHop", default=None)
    set_ipv6_nexthop: Optional[Global[str]] = Field(alias="setIpv6NextHop", default=None)


class AcceptActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    accept: AcceptAction


class RejectActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    reject: Default[bool] = Default[bool](value=True)


class RoutePolicySequence(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    sequence_id: Global[int] = Field(alias="sequenceId")
    sequence_name: Global[str] = Field(alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        alias="baseAction", default=Default[Action](value=Action.REJECT)
    )
    protocol: Union[Global[Protocol], Default[Protocol]] = Default[Protocol](value=Protocol.IPV4)
    match_entries: Optional[List[RoutePolicyMatch]] = Field(alias="matchEntries", default=None)
    actions: Optional[List[Union[AcceptActions, RejectActions]]] = None


class RoutePolicyData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        alias="defaultAction", default=Default[Action](value=Action.REJECT)
    )
    sequences: List[RoutePolicySequence] = []


class RoutePolicyCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: RoutePolicyData
    metadata: Optional[dict] = None
