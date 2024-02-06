from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId


class SummaryPrefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_address: Optional[Union[Global[str], Variable]] = None
    subnet_mask: Optional[Union[Global[str], Variable]] = None


class SummaryRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Optional[SummaryPrefix] = None
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    no_advertise: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="noAdvertise", default=None)


class NetworkType(str, Enum):
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    PONIT_TO_MULTIPOINT = "point-to-multipoint"


class AuthenticationType(str, Enum):
    MESSAGE_DIGEST = "message-digest"


class AreaType(str, Enum):
    STUB = "stub"
    NSSA = "nssa"


class OspfInterfaceParametres(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Optional[Union[Global[str], Variable]]
    hello_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="helloInterval", default=None)
    dead_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="deadInterval", default=None)
    retransmit_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="retransmitInterval", default=None
    )
    cost: Optional[Union[Global[int], Variable, Default[None]]] = None
    priority: Optional[Union[Global[int], Variable, Default[int]]] = None
    network: Optional[Union[Global[NetworkType], Variable, Default[NetworkType]]] = Default[NetworkType](
        value=NetworkType.BROADCAST
    )
    passive_interface: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        alias="passiveInterface", default=None
    )
    authentication_type: Optional[Union[Global[AuthenticationType], Variable, Default[None]]] = Field(
        alias="type", default=None
    )
    message_digest_key: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        alias="messageDigestKey", default=None
    )
    md5: Optional[Union[Global[str], Variable, Default[None]]] = None


class OspfArea(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    area_number: Union[Global[int], Variable] = Field(alias="aNum")
    area_type: Optional[Union[Global[AreaType], Default[None]]] = Field(alias="aType", default=None)
    no_summary: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(alias="noSummary", default=None)
    interface: Optional[List[OspfInterfaceParametres]] = None
    range: Optional[List[SummaryRoute]]


class AdvertiseType(str, Enum):
    ADMINISTRATIVE = "administrative"
    ON_STARTUP = "on-startup"


class RouterLsa(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ad_type: Global[AdvertiseType] = Field(alias="adType")
    time: Optional[Union[Global[int], Variable]] = None


class RedistributeProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OMP = "omp"
    NAT = "nat"
    EIGRP = "eigrp"


class RedistributedRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Global[RedistributeProtocol], Variable]
    dia: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)


class MetricType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


class OspfData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    router_id: Optional[Union[Global[str], Variable, Default[None]]] = Field(alias="routerId", default=None)
    reference_bandwidth: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="referenceBandwidth", default=None
    )
    rfc1583: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    originate: Optional[Union[Global[bool], Default[bool]]] = None
    always: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    metric: Optional[Union[Global[int], Variable, Default[None]]] = None
    metric_type: Optional[Union[Global[MetricType], Variable, Default[None]]] = Field(alias="metricType", default=None)
    external: Optional[Union[Global[int], Variable, Default[int]]] = None
    inter_area: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="interArea", default=None)
    intra_area: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="intraArea", default=None)
    delay: Optional[Union[Global[int], Variable, Default[int]]] = None
    initial_hold: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="initialHold", default=None)
    max_hold: Optional[Union[Global[int], Variable, Default[int]]] = Field(alias="maxHold", default=None)
    redistribute: Optional[List[RedistributedRoute]] = None
    router_lsa: Optional[List[RouterLsa]] = Field(alias="routerLsa", default=None)
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    area: Optional[List[OspfArea]] = None


class OspfCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: OspfData
    metadata: Optional[dict] = None
