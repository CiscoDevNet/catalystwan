# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

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


class Redistribute(FeatureTemplateValidator):
    protocol: Protocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    dia: Optional[BoolStr] = True
    model_config = ConfigDict(populate_by_name=True)


class AdType(str, Enum):
    ADMINISTRATIVE = "administrative"
    ON_STARTUP = "on-startup"


class RouterLsa(FeatureTemplateValidator):
    ad_type: AdType = Field(json_schema_extra={"vmanage_key": "ad-type"})
    time: int
    model_config = ConfigDict(populate_by_name=True)


class Direction(str, Enum):
    IN = "in"


class RoutePolicy(FeatureTemplateValidator):
    direction: Direction
    pol_name: str = Field(json_schema_extra={"vmanage_key": "pol-name"})
    model_config = ConfigDict(populate_by_name=True)


class Network(str, Enum):
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    POINT_TO_MULTIPOINT = "point-to-multipoint"


class Type(str, Enum):
    SIMPLE = "simple"
    MESSAGE_DIGEST = "message-digest"
    NULL = "null"


class Interface(FeatureTemplateValidator):
    name: str
    hello_interval: Optional[int] = Field(
        DEFAULT_OSPF_DEAD_INTERVAL, json_schema_extra={"vmanage_key": "hello-interval"}
    )
    dead_interval: Optional[int] = Field(DEFAULT_OSPF_DEAD_INTERVAL, json_schema_extra={"vmanage_key": "dead-interval"})
    retransmit_interval: Optional[int] = Field(
        DEFAULT_OSPF_RETRANSMIT_INTERVAL, json_schema_extra={"vmanage_key": "retransmit-interval"}
    )
    cost: Optional[int] = None
    priority: Optional[int] = DEFAULT_OSPF_INTERFACE_PRIORITY
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[BoolStr] = Field(default=False, json_schema_extra={"vmanage_key": "passive-interface"})
    type: Optional[Type] = Field(default=None, json_schema_extra={"data_path": ["authentication"]})
    message_digest_key: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "message-digest-key", "data_path": ["authentication", "message-digest"]},
    )
    md5: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["authentication", "message-digest"]})
    model_config = ConfigDict(populate_by_name=True)


class Range(FeatureTemplateValidator):
    address: ipaddress.IPv4Interface
    cost: Optional[int] = None
    no_advertise: Optional[BoolStr] = Field(default=False, json_schema_extra={"vmanage_key": "no-advertise"})
    model_config = ConfigDict(populate_by_name=True)


class Area(FeatureTemplateValidator):
    a_num: int = Field(json_schema_extra={"vmanage_key": "a-num"})
    stub: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]}
    )
    nssa: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]}
    )
    interface: Optional[List[Interface]] = None
    range: Optional[List[Range]] = None
    model_config = ConfigDict(populate_by_name=True)


class CiscoOSPFModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    router_id: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospf"]}
    )
    reference_bandwidth: Optional[int] = Field(
        DEFAULT_OSPF_REFERENCE_BANDWIDTH,
        json_schema_extra={"data_path": ["ospf", "auto-cost"], "vmanage_key": "reference-bandwidth"},
    )
    rfc1583: Optional[BoolStr] = Field(default=True, json_schema_extra={"data_path": ["ospf", "compatible"]})
    originate: Optional[BoolStr] = Field(default=None, json_schema_extra={"data_path": ["ospf", "default-information"]})
    always: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"data_path": ["ospf", "default-information", "originate"]}
    )
    metric: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["ospf", "default-information", "originate"]}
    )
    metric_type: Optional[MetricType] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "metric-type", "data_path": ["ospf", "default-information", "originate"]},
    )
    external: Optional[int] = Field(DEFAULT_OSPF_EXTERNAL, json_schema_extra={"data_path": ["ospf", "distance"]})
    inter_area: Optional[int] = Field(
        DEFAULT_OSPF_INTER_AREA, json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "inter-area"}
    )
    intra_area: Optional[int] = Field(
        DEFAULT_OSPF_INTRA_AREA, json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "intra-area"}
    )
    delay: Optional[int] = Field(DEFAULT_OSPF_DELAY, json_schema_extra={"data_path": ["ospf", "timers", "spf"]})
    initial_hold: Optional[int] = Field(
        DEFAULT_OSPF_INITIAL_HOLD,
        json_schema_extra={"vmanage_key": "initial-hold", "data_path": ["ospf", "timers", "spf"]},
    )
    max_hold: Optional[int] = Field(
        DEFAULT_OSPF_MAX_HOLD, json_schema_extra={"vmanage_key": "max-hold", "data_path": ["ospf", "timers", "spf"]}
    )
    redistribute: Optional[List[Redistribute]] = Field(
        default=None, json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospf"]}
    )
    router_lsa: Optional[List[RouterLsa]] = Field(
        default=None, json_schema_extra={"vmanage_key": "router-lsa", "data_path": ["ospf", "max-metric"]}
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None, json_schema_extra={"vmanage_key": "route-policy", "data_path": ["ospf"]}
    )
    area: Optional[List[Area]] = Field(default=None, json_schema_extra={"vmanage_key": "area", "data_path": ["ospf"]})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospf"
