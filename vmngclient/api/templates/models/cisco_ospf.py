import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel, ConvertIPToStringModel

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
    type: Optional[Type] = Field(data_path=["authentication"])
    message_digest_key: Optional[int] = Field(
        alias="message-digest-key", data_path=["authentication", "message-digest"]
    )
    md5: Optional[str] = Field(data_path=["authentication", "message-digest"])

    class Config:
        allow_population_by_field_name = True


class Range(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv4Interface
    cost: Optional[int]
    no_advertise: Optional[bool] = Field(False, alias="no-advertise")

    class Config:
        allow_population_by_field_name = True


class Area(ConvertBoolToStringModel):
    a_num: int = Field(alias="a-num")
    stub: Optional[bool] = Field(alias="no-summary", data_path=["stub"])
    nssa: Optional[bool] = Field(alias="no-summary", data_path=["nssa"])
    interface: Optional[List[Interface]]
    range: Optional[List[Range]]

    class Config:
        allow_population_by_field_name = True


class CiscoOSPFModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    router_id: Optional[str] = Field(alias="router-id", data_path=["ospf"])
    reference_bandwidth: Optional[int] = Field(
        DEFAULT_OSPF_REFERENCE_BANDWIDTH, data_path=["ospf", "auto-cost"], alias="reference-bandwidth"
    )
    rfc1583: Optional[bool] = Field(True, data_path=["ospf", "compatible"])
    originate: Optional[bool] = Field(data_path=["ospf", "default-information"])
    always: Optional[bool] = Field(data_path=["ospf", "default-information", "originate"])
    metric: Optional[int] = Field(data_path=["ospf", "default-information", "originate"])
    metric_type: Optional[MetricType] = Field(
        alias="metric-type", data_path=["ospf", "default-information", "originate"]
    )
    external: Optional[int] = Field(DEFAULT_OSPF_EXTERNAL, data_path=["ospf", "distance"])
    inter_area: Optional[int] = Field(DEFAULT_OSPF_INTER_AREA, data_path=["ospf", "distance"], alias="inter-area")
    intra_area: Optional[int] = Field(DEFAULT_OSPF_INTRA_AREA, data_path=["ospf", "distance"], alias="intra-area")
    delay: Optional[int] = Field(DEFAULT_OSPF_DELAY, data_path=["ospf", "timers", "spf"])
    initial_hold: Optional[int] = Field(
        DEFAULT_OSPF_INITIAL_HOLD, alias="initial-hold", data_path=["ospf", "timers", "spf"]
    )
    max_hold: Optional[int] = Field(DEFAULT_OSPF_MAX_HOLD, alias="max-hold", data_path=["ospf", "timers", "spf"])
    redistribute: Optional[List[Redistribute]] = Field(alias="redistribute", data_path=["ospf"])
    router_lsa: Optional[List[RouterLsa]] = Field(alias="router-lsa", data_path=["ospf", "max-metric"])
    route_policy: Optional[List[RoutePolicy]] = Field(alias="route-policy", data_path=["ospf"])
    area: Optional[List[Area]] = Field(alias="area", data_path=["ospf"])

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospf"
