# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class MetricType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


class Protocol(str, Enum):
    BGP = "bgp"
    CONNECTED = "connected"
    EIGRP = "eigrp"
    ISIS = "isis"
    LISP = "lisp"
    NAT_ROUTE = "nat-route"
    OMP = "omp"
    STATIC = "static"


class Redistribute(FeatureTemplateValidator):
    protocol: Protocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    dia: Optional[BoolStr] = True
    model_config = ConfigDict(populate_by_name=True)


class AdType(str, Enum):
    ON_STARTUP = "on-startup"


class RouterLsa(FeatureTemplateValidator):
    ad_type: AdType = Field(json_schema_extra={"vmanage_key": "ad-type"})
    time: int
    model_config = ConfigDict(populate_by_name=True)


class Translate(str, Enum):
    ALWAYS = "always"


class Network(str, Enum):
    BROADCAST = "broadcast"
    POINT_TO_POINT = "point-to-point"
    NON_BROADCAST = "non-broadcast"
    POINT_TO_MULTIPOINT = "point-to-multipoint"


class Type(str, Enum):
    MD5 = "md5"
    SHA1 = "sha1"


class Interface(FeatureTemplateValidator):
    name: str
    hello_interval: Optional[int] = Field(10, json_schema_extra={"vmanage_key": "hello-interval"})
    dead_interval: Optional[int] = Field(40, json_schema_extra={"vmanage_key": "dead-interval"})
    retransmit_interval: Optional[int] = Field(5, json_schema_extra={"vmanage_key": "retransmit-interval"})
    cost: Optional[int] = None
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "passive-interface"})
    type: Type = Field(json_schema_extra={"data_path": ["authentication"]})
    authentication_key: str = Field(
        json_schema_extra={"vmanage_key": "authentication-key", "data_path": ["authentication"]}
    )
    spi: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["authentication", "ipsec"]})
    model_config = ConfigDict(populate_by_name=True)


class Range(FeatureTemplateValidator):
    address: ipaddress.IPv4Interface
    cost: Optional[int] = None
    no_advertise: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "no-advertise"})
    model_config = ConfigDict(populate_by_name=True)


class Area(FeatureTemplateValidator):
    a_num: int = Field(json_schema_extra={"vmanage_key": "a-num"})
    stub: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]}
    )
    nssa: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]}
    )
    translate: Optional[Translate] = Field(default=None, json_schema_extra={"data_path": ["nssa"]})
    normal: Optional[BoolStr] = None
    interface: Optional[List[Interface]] = None
    range: Optional[List[Range]] = None
    model_config = ConfigDict(populate_by_name=True)


class RedistributeV6(FeatureTemplateValidator):
    protocol: Protocol
    route_policy: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "route-policy"})
    model_config = ConfigDict(populate_by_name=True)


class InterfaceV6(FeatureTemplateValidator):
    name: str
    hello_interval: Optional[int] = Field(10, json_schema_extra={"vmanage_key": "hello-interval"})
    dead_interval: Optional[int] = Field(40, json_schema_extra={"vmanage_key": "dead-interval"})
    retransmit_interval: Optional[int] = Field(5, json_schema_extra={"vmanage_key": "retransmit-interval"})
    cost: Optional[int] = None
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "passive-interface"})
    type: Type = Field(json_schema_extra={"data_path": ["authentication"]})
    authentication_key: str = Field(
        json_schema_extra={"vmanage_key": "authentication-key", "data_path": ["authentication"]}
    )
    spi: Optional[int] = Field(default=None, json_schema_extra={"data_path": ["authentication", "ipsec"]})
    model_config = ConfigDict(populate_by_name=True)


class RangeV6(FeatureTemplateValidator):
    address: ipaddress.IPv6Interface
    cost: Optional[int] = None
    no_advertise: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "no-advertise"})
    model_config = ConfigDict(populate_by_name=True)


class AreaV6(FeatureTemplateValidator):
    a_num: int = Field(json_schema_extra={"vmanage_key": "a-num"})
    stub: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]}
    )
    nssa: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]}
    )
    translate: Optional[Translate] = Field(default=None, json_schema_extra={"data_path": ["nssa"]})
    normal: Optional[BoolStr] = None
    interface: Optional[List[InterfaceV6]] = None
    range: Optional[List[RangeV6]] = None
    model_config = ConfigDict(populate_by_name=True)


class CiscoOspfv3Model(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    router_id_v4: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospfv3", "address-family", "ipv4"]}
    )
    reference_bandwidth_v4: Optional[int] = Field(
        100,
        json_schema_extra={
            "vmanage_key": "reference-bandwidth",
            "data_path": ["ospfv3", "address-family", "ipv4", "auto-cost"],
        },
    )
    rfc1583_v4: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "rfc1583", "data_path": ["ospfv3", "address-family", "ipv4", "compatible"]},
    )
    originate_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "originate",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information"],
        },
    )
    always_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "always",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
    )
    metric_v4: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
    )
    metric_type_v4: Optional[MetricType] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric-type",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
    )
    external_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "external",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
        },
    )
    inter_area_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "inter-area",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
        },
    )
    intra_area_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "intra-area",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
        },
    )
    delay_v4: Optional[int] = Field(
        200,
        json_schema_extra={
            "vmanage_key": "delay",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
    )
    initial_hold_v4: Optional[int] = Field(
        1000,
        json_schema_extra={
            "vmanage_key": "initial-hold",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
    )
    max_hold_v4: Optional[int] = Field(
        10000,
        json_schema_extra={
            "vmanage_key": "max-hold",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
    )
    distance_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "distance",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4"],
        },
    )
    name_v4: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "name", "data_path": ["ospfv3", "address-family", "ipv4", "table-map"]},
    )
    filter_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "filter", "data_path": ["ospfv3", "address-family", "ipv4", "table-map"]},
    )
    redistribute_v4: Optional[List[Redistribute]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospfv3", "address-family", "ipv4"]},
    )
    router_lsa_v4: Optional[List[RouterLsa]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "router-lsa",
            "data_path": ["ospfv3", "address-family", "ipv4", "max-metric"],
        },
    )
    area_v4: Optional[List[Area]] = Field(
        default=None, json_schema_extra={"vmanage_key": "area", "data_path": ["ospfv3", "address-family", "ipv4"]}
    )
    router_id_v6: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospfv3", "address-family", "ipv6"]}
    )
    reference_bandwidth_v6: Optional[int] = Field(
        100,
        json_schema_extra={
            "vmanage_key": "reference-bandwidth",
            "data_path": ["ospfv3", "address-family", "ipv6", "auto-cost"],
        },
    )
    rfc1583_v6: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "rfc1583", "data_path": ["ospfv3", "address-family", "ipv6", "compatible"]},
    )
    originate_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "originate",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information"],
        },
    )
    always_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "always",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
    )
    metric_v6: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
    )
    metric_type_v6: Optional[MetricType] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric-type",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
    )
    external_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "external",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
    )
    inter_area_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "inter-area",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
    )
    intra_area_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "intra-area",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
    )
    delay_v6: Optional[int] = Field(
        200,
        json_schema_extra={
            "vmanage_key": "delay",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
    )
    initial_hold_v6: Optional[int] = Field(
        1000,
        json_schema_extra={
            "vmanage_key": "initial-hold",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
    )
    max_hold_v6: Optional[int] = Field(
        10000,
        json_schema_extra={
            "vmanage_key": "max-hold",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
    )
    distance_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "distance",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6"],
        },
    )
    name_v6: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "name", "data_path": ["ospfv3", "address-family", "ipv6", "table-map"]},
    )
    filter_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "filter", "data_path": ["ospfv3", "address-family", "ipv6", "table-map"]},
    )
    redistribute_v6: Optional[List[RedistributeV6]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospfv3", "address-family", "ipv6"]},
    )
    router_lsa_v6: Optional[List[RouterLsa]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "router-lsa",
            "data_path": ["ospfv3", "address-family", "ipv6", "max-metric"],
        },
    )
    area_v6: Optional[List[AreaV6]] = Field(
        default=None, json_schema_extra={"vmanage_key": "area", "data_path": ["ospfv3", "address-family", "ipv6"]}
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospfv3"
