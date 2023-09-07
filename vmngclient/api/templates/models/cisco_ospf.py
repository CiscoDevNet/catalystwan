import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel

DEFAULT_OSPF_HELLO_INTERVAL = 10
DEFAULT_OSPF_DEAD_INTERVAL = 40
DEFAULT_OSPF_RETRANSMIT_INTERVAL = 5
DEFAULT_OSPF_INTERFACE_PRIORITY = 1
DEFAULT_OSPF_REFERENCE_BANDWIDTH = 100
DEFAULT_OSPF_EXTERNAL = 110
DEFAULT_OSPF_INTER_AREA = 110
DEFAULT_OSPF_INTRA_AREA = 110
DEFAULT_OSPF_DELAY = 200
DEFAULT_OSPF_INITIAL_HOLD = 1000
DEFAULT_OSPF_MAX_HOLD = 10000


class MetricType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


class Protocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OMP = "omp"
    NAT = "nat"
    EIGRP = "eigrp"


class Redistribute(ConvertBoolToStringModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(alias="route-policy")
    dia: Optional[bool] = True

    class Config:
        allow_population_by_field_name = True


class AdType(str, Enum):
    ADMINISTRATIVE = "administrative"
    ON_STARTUP = "on-startup"


class RouterLsa(ConvertBoolToStringModel):
    ad_type: AdType = Field(alias="ad-type")
    time: int

    class Config:
        allow_population_by_field_name = True


class Direction(str, Enum):
    IN = "in"


class RoutePolicy(ConvertBoolToStringModel):
    direction: Direction
    pol_name: str = Field(alias="pol-name")

    class Config:
        allow_population_by_field_name = True


class Network(str, Enum):
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    POINT_TO_MULTIPOINT = "point-to-multipoint"


class Type(str, Enum):
    SIMPLE = "simple"
    MESSAGE_DIGEST = "message-digest"
    NULL = "null"


class Interface(ConvertBoolToStringModel):
    name: str
    hello_interval: Optional[int] = Field(DEFAULT_OSPF_DEAD_INTERVAL, alias="hello-interval")
    dead_interval: Optional[int] = Field(DEFAULT_OSPF_DEAD_INTERVAL, alias="dead-interval")
    retransmit_interval: Optional[int] = Field(DEFAULT_OSPF_RETRANSMIT_INTERVAL, alias="retransmit-interval")
    cost: Optional[int]
    priority: Optional[int] = DEFAULT_OSPF_INTERFACE_PRIORITY
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[bool] = Field(False, alias="passive-interface")
    type: Optional[Type]
    message_digest_key: Optional[int] = Field(alias="message-digest-key")
    md5: Optional[str]

    class Config:
        allow_population_by_field_name = True


class Range(ConvertBoolToStringModel):
    address: ipaddress.IPv4Interface
    cost: Optional[int]
    no_advertise: Optional[bool] = Field(False, alias="no-advertise")

    class Config:
        allow_population_by_field_name = True


class Area(ConvertBoolToStringModel):
    a_num: int = Field(alias="a-num")
    stub_no_summary: Optional[bool] = Field(vmanage_key="no-summary", data_path=["stub", "no_summary"])
    nssa_no_summary: Optional[bool] = Field(vmanage_key="no-summary")
    interface: Optional[List[Interface]]
    range: Optional[List[Range]]

    class Config:
        allow_population_by_field_name = True


class CiscoOSPFModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    router_id: Optional[ipaddress.IPv4Address] = Field(alias="router-id")
    reference_bandwidth: Optional[int] = Field(DEFAULT_OSPF_REFERENCE_BANDWIDTH, alias="reference-bandwidth")
    rfc1583: Optional[bool] = True
    originate: Optional[bool]
    always: Optional[bool]
    metric: Optional[int]
    metric_type: Optional[MetricType] = Field(alias="metric-type")
    external: Optional[int] = DEFAULT_OSPF_EXTERNAL
    inter_area: Optional[int] = Field(DEFAULT_OSPF_INTER_AREA, alias="inter-area")
    intra_area: Optional[int] = Field(DEFAULT_OSPF_INTRA_AREA, alias="intra-area")
    delay: Optional[int] = DEFAULT_OSPF_DELAY
    initial_hold: Optional[int] = Field(DEFAULT_OSPF_INITIAL_HOLD, alias="initial-hold")
    max_hold: Optional[int] = Field(DEFAULT_OSPF_MAX_HOLD, alias="max-hold")
    redistribute: Optional[List[Redistribute]]
    router_lsa: Optional[List[RouterLsa]] = Field(alias="router-lsa")
    route_policy: Optional[List[RoutePolicy]] = Field(alias="route-policy")
    area: Optional[List[Area]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospf"
