from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId
from catalystwan.models.configuration.feature_profile.common import Prefix


class NetworkType(str, Enum):
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    PONIT_TO_MULTIPOINT = "point-to-multipoint"


class NoAuthType(str, Enum):
    NO_AUTH = "no-auth"


class IpsecSha1AuthType(str, Enum):
    IPSEC_SHA1 = "ipsec-sha1"


class NoAuth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    auth_type: Union[Global[NoAuthType], Default[NoAuthType]] = Field(
        alias="authType", default=Default[NoAuthType](value=NoAuthType.NO_AUTH)
    )


class IpsecSha1Auth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    auth_type: Global[IpsecSha1AuthType] = Field(
        alias="authType", default=Global[IpsecSha1AuthType](value=IpsecSha1AuthType.IPSEC_SHA1)
    )
    spi: Union[Global[int], Variable]
    auth_key: Union[Global[str], Variable] = Field(alias="authKey")


class Ospfv3InterfaceParametres(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Optional[Union[Global[str], Variable]] = Field(alias="ifName")
    hello_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="helloInterval", default=None)
    dead_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="deadInterval", default=None)
    retransmit_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="retransmitInterval", default=None
    )
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    priority: Optional[Union[Global[int], Variable, Default[int]]] = None
    network_type: Optional[Union[Global[NetworkType], Variable, Default[None]]] = Field(
        alias="networkType", default=None
    )
    passive_interface: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="passiveInterface", default=None
    )
    authentication_config: Optional[Union[NoAuth, IpsecSha1Auth]] = Field(alias="authenticationConfig", default=None)


class SummaryRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    network: Union[Global[str], Variable]
    no_advertise: Union[Global[bool], Variable, Default[bool]] = Field(alias="noAdvertise")
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None


class SummaryRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    network: Optional[Prefix] = None
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    no_advertise: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="noAdvertise", default=None)


class StubArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_type: Global[str] = Field(alias="areaType", default=Global[str](value="stub"))
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="noSummary", default=None)


class NssaArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_type: Global[str] = Field(alias="areaType", default=Global[str](value="nssa"))
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="noSummary", default=None)
    always_translate: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="alwaysTranslate", default=None
    )


class NormalArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_type: Global[str] = Field(alias="areaType", default=Global[str](value="normal"))


class DefaultArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_type: Default[None] = Field(alias="areaType", default=Default[None](value=None))


class Ospfv3IPv4Area(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_number: Union[Global[int], Variable] = Field(alias="areaNum")
    area_type_config: Optional[Union[StubArea, NssaArea, NormalArea, DefaultArea]] = Field(
        alias="areaTypeConfig", default=None
    )
    interfaces: List[Ospfv3InterfaceParametres]
    ranges: Optional[List[SummaryRoute]] = None


class Ospfv3IPv6Area(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_number: Union[Global[int], Variable] = Field(alias="areaNum")
    area_type_config: Optional[Union[StubArea, NssaArea, NormalArea, DefaultArea]] = Field(
        alias="areaTypeConfig", default=None
    )
    interfaces: List[Ospfv3InterfaceParametres]
    ranges: Optional[List[SummaryRoute]] = None


class MaxMetricRouterLsaAction(str, Enum):
    DISABLED = "disabled"
    IMMEDIATELY = "immediately"
    ON_STARTUP = "on-startup"


class MaxMetricRouterLsa(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    action: Global[MaxMetricRouterLsaAction]
    on_startup_time: Optional[Union[Global[int], Variable]] = Field(alias="onStartUpTime", default=None)


class RedistributeProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OMP = "omp"
    NAT = "nat-route"
    EIGRP = "eigrp"


class RedistributeProtocolIPv6(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OMP = "omp"
    EIGRP = "eigrp"


class MetricType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocol], Variable]
    nat_dia: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="natDia", default=None)
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)


class RedistributedRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocolIPv6], Variable]
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)


class DefaultOriginate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    originate: Union[Global[bool], Default[bool]]
    always: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    metric: Optional[Union[Global[str], Variable, Default[None]]] = None
    metricType: Optional[Union[Global[MetricType], Variable, Default[None]]] = None


class SpfTimers(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    delay: Optional[Union[Global[int], Variable, Default[int]]] = None
    initial_hold: Optional[Union[Global[int], Variable, Default[int]]] = None
    max_hold: Optional[Union[Global[int], Variable, Default[int]]] = None


class AdvancedOspfv3Attributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    reference_bandwidth: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="referenceBandwidth", default=None
    )
    compatible_rfc1583: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="compatibleRfc1583", default=None
    )
    default_originate: Optional[DefaultOriginate] = Field(alias="defaultOriginate", default=None)
    spf_timers: Optional[SpfTimers] = Field(alias="spfTimers", default=None)
    policy_name: Optional[Union[Default[None], RefId]] = Field(alias="policyName", default=None)
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = None


class BasicOspfv3Attributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    router_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="routerId", default=None)
    distance: Optional[Union[Global[int], Variable, Default[int]]] = None
    external_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="externalDistance", default=None
    )
    inter_area_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="interAreaDistance", default=None
    )
    intra_area_distance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="intraAreaDistance", default=None
    )


class Ospfv3IPv4Data(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    basic: Optional[BasicOspfv3Attributes] = None
    advanced: Optional[AdvancedOspfv3Attributes] = None
    redistribute: Optional[RedistributedRoute] = None
    max_metric_router_lsa: Optional[MaxMetricRouterLsa] = Field(alias="maxMetricRouterLsa", default=None)
    area: List[Ospfv3IPv4Area]


class Ospfv3IPv6Data(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    basic: Optional[BasicOspfv3Attributes] = None
    advanced: Optional[AdvancedOspfv3Attributes] = None
    redistribute: Optional[RedistributedRouteIPv6] = None
    max_metric_router_lsa: Optional[MaxMetricRouterLsa] = Field(alias="maxMetricRouterLsa", default=None)
    area: List[Ospfv3IPv6Area]


class Ospfv3IPv4CreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: Ospfv3IPv4Data


class Ospfv3IPv6CreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: Ospfv3IPv6Data
    metadata: Optional[dict] = None
