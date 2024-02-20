import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel, ConvertIPToStringModel

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

MetricType = Literal[
    "type1",
    "type2",
]
Protocol = Literal["static", "connected", "bgp", "ospf", "omp", "nat", "eigrp"]
AdType = Literal["administrative", "on-startup"]
Network = Literal["broadcast", "point-to-point", "non-broadcast", "point-to-multipoint"]
Type = Literal["simple", "message-digest", "null"]
Direction = Literal["in"]


class Redistribute(ConvertBoolToStringModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(
        default=None,
        serialization_alias="route-policy",
        validation_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    dia: Optional[bool] = True
    model_config = ConfigDict(populate_by_name=True)


class RouterLsa(ConvertBoolToStringModel):
    ad_type: AdType = Field(
        serialization_alias="ad-type", validation_alias="ad-type", json_schema_extra={"vmanage_key": "ad-type"}
    )
    time: int
    model_config = ConfigDict(populate_by_name=True)


class RoutePolicy(ConvertBoolToStringModel):
    direction: Direction
    pol_name: str = Field(
        validation_alias="pol-name", serialization_alias="pol-name", json_schema_extra={"vmanage_key": "pol-name"}
    )
    model_config = ConfigDict(populate_by_name=True)


class Interface(ConvertBoolToStringModel):
    name: str
    hello_interval: Optional[int] = Field(
        default=DEFAULT_OSPF_DEAD_INTERVAL,
        serialization_alias="hello-interval",
        validation_alias="hello-interval",
        json_schema_extra={"vmanage_key": "hello-interval"},
    )
    dead_interval: Optional[int] = Field(
        default=DEFAULT_OSPF_DEAD_INTERVAL,
        serialization_alias="dead-interval",
        validation_alias="dead-interval",
        json_schema_extra={"vmanage_key": "dead-interval"},
    )
    retransmit_interval: Optional[int] = Field(
        default=DEFAULT_OSPF_RETRANSMIT_INTERVAL,
        serialization_alias="retransmit-interval",
        validation_alias="retransmit-interval",
        json_schema_extra={"vmanage_key": "retransmit-interval"},
    )
    cost: Optional[int] = None
    priority: Optional[int] = DEFAULT_OSPF_INTERFACE_PRIORITY
    network: Optional[Network] = "broadcast"
    passive_interface: Optional[bool] = Field(
        default=False,
        serialization_alias="passive-interface",
        validation_alias="passive-interface",
        json_schema_extra={"vmanage_key": "passive-interface"},
    )
    type: Optional[Type] = Field(default=None, json_schema_extra={"data_path": ["authentication"]})
    message_digest_key: Optional[int] = Field(
        default=None,
        validation_alias="message-digest-key",
        serialization_alias="message-digest-key",
        json_schema_extra={"vmanage_key": "message-digest-key", "data_path": ["authentication", "message-digest"]},
    )
    md5: Optional[str] = Field(default=None, json_schema_extra={"data_path": ["authentication", "message-digest"]})
    model_config = ConfigDict(populate_by_name=True)


class Range(ConvertBoolToStringModel, ConvertIPToStringModel):
    address: ipaddress.IPv4Interface
    cost: Optional[int] = None
    no_advertise: Optional[bool] = Field(
        default=False,
        serialization_alias="no-advertise",
        validation_alias="no-advertise",
        json_schema_extra={"vmanage_key": "no-advertise"},
    )

    model_config = ConfigDict(populate_by_name=True)


class Area(ConvertBoolToStringModel):
    a_num: int = Field(
        serialization_alias="a-num", validation_alias="a-num", json_schema_extra={"vmanage_key": "a-num"}
    )
    stub: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]})
    nssa: Optional[bool] = Field(default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]})
    interface: Optional[List[Interface]] = None
    range: Optional[List[Range]] = None
    model_config = ConfigDict(populate_by_name=True)


class CiscoOSPFModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    router_id: Optional[str] = Field(
        default=None,
        validation_alias="router-id",
        serialization_alias="router-id",
        json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospf"]},
    )
    reference_bandwidth: Optional[int] = Field(
        default=DEFAULT_OSPF_REFERENCE_BANDWIDTH,
        validation_alias="reference-bandwidth",
        serialization_alias="reference-bandwidth",
        json_schema_extra={"data_path": ["ospf", "auto-cost"], "vmanage_key": "reference-bandwidth"},
    )
    rfc1583: Optional[bool] = Field(True, json_schema_extra={"data_path": ["ospf", "compatible"]})
    originate: Optional[bool] = Field(default=None, json_schema_extra={"data_path": ["ospf", "default-information"]})
    always: Optional[bool] = Field(
        default=None, json_schema_extra={"data_path": ["ospf", "default-information", "originate"]}
    )
    metric: Optional[int] = Field(
        default=None, json_schema_extra={"data_path": ["ospf", "default-information", "originate"]}
    )
    metric_type: Optional[MetricType] = Field(
        default=None,
        validation_alias="metric-type",
        serialization_alias="metric-type",
        json_schema_extra={"vmanage_key": "metric-type", "data_path": ["ospf", "default-information", "originate"]},
    )
    external: Optional[int] = Field(
        default=DEFAULT_OSPF_EXTERNAL, json_schema_extra={"data_path": ["ospf", "distance"]}
    )
    inter_area: Optional[int] = Field(
        default=DEFAULT_OSPF_INTER_AREA,
        serialization_alias="inter-area",
        validation_alias="inter-area",
        json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "inter-area"},
    )
    intra_area: Optional[int] = Field(
        default=DEFAULT_OSPF_INTRA_AREA,
        serialization_alias="intra-area",
        validation_alias="intra-area",
        json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "intra-area"},
    )
    delay: Optional[int] = Field(DEFAULT_OSPF_DELAY, json_schema_extra={"data_path": ["ospf", "timers", "spf"]})
    initial_hold: Optional[int] = Field(
        default=DEFAULT_OSPF_INITIAL_HOLD,
        validation_alias="initial-hold",
        serialization_alias="initial-hold",
        json_schema_extra={"vmanage_key": "initial-hold", "data_path": ["ospf", "timers", "spf"]},
    )
    max_hold: Optional[int] = Field(
        default=DEFAULT_OSPF_MAX_HOLD,
        validation_alias="max-hold",
        serialization_alias="max-hold",
        json_schema_extra={"vmanage_key": "max-hold", "data_path": ["ospf", "timers", "spf"]},
    )
    redistribute: Optional[List[Redistribute]] = Field(
        default=None, json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospf"]}
    )
    router_lsa: Optional[List[RouterLsa]] = Field(
        default=None,
        validation_alias="router-lsa",
        serialization_alias="router-lsa",
        json_schema_extra={"vmanage_key": "router-lsa", "data_path": ["ospf", "max-metric"]},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        validation_alias="route-policy",
        serialization_alias="route-policy",
        json_schema_extra={"vmanage_key": "route-policy", "data_path": ["ospf"]},
    )
    area: Optional[List[Area]] = Field(default=None, json_schema_extra={"vmanage_key": "area", "data_path": ["ospf"]})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospf"
