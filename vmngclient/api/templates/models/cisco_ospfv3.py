import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel, ConvertIPToStringModel


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


class Redistribute(ConvertBoolToStringModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(vmanage_key="route-policy")
    dia: Optional[bool] = True

    class Config:
        allow_population_by_field_name = True


class AdType(str, Enum):
    ON_STARTUP = "on-startup"


class RouterLsa(BaseModel):
    ad_type: AdType = Field(vmanage_key="ad-type")
    time: int

    class Config:
        allow_population_by_field_name = True


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


class Interface(BaseModel):
    name: str
    hello_interval: Optional[int] = Field(10, vmanage_key="hello-interval")
    dead_interval: Optional[int] = Field(40, vmanage_key="dead-interval")
    retransmit_interval: Optional[int] = Field(5, vmanage_key="retransmit-interval")
    cost: Optional[int]
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[bool] = Field(False, vmanage_key="passive-interface")
    type: Type = Field(data_path=["authentication"])
    authentication_key: str = Field(vmanage_key="authentication-key", data_path=["authentication"])
    spi: Optional[int] = Field(data_path=["authentication", "ipsec"])

    class Config:
        allow_population_by_field_name = True


class Range(BaseModel):
    address: ipaddress.IPv4Interface
    cost: Optional[int]
    no_advertise: Optional[bool] = Field(False, vmanage_key="no-advertise")

    class Config:
        allow_population_by_field_name = True


class Area(ConvertBoolToStringModel):
    a_num: int = Field(vmanage_key="a-num")
    stub: Optional[bool] = Field(vmanage_key="no-summary", data_path=["stub"])
    nssa: Optional[bool] = Field(vmanage_key="no-summary", data_path=["nssa"])
    translate: Optional[Translate] = Field(data_path=["nssa"])
    normal: Optional[bool]
    interface: Optional[List[Interface]]
    range: Optional[List[Range]]

    class Config:
        allow_population_by_field_name = True


class RedistributeV6(BaseModel):
    protocol: Protocol
    route_policy: Optional[str] = Field(vmanage_key="route-policy")

    class Config:
        allow_population_by_field_name = True


class InterfaceV6(BaseModel):
    name: str
    hello_interval: Optional[int] = Field(10, vmanage_key="hello-interval")
    dead_interval: Optional[int] = Field(40, vmanage_key="dead-interval")
    retransmit_interval: Optional[int] = Field(5, vmanage_key="retransmit-interval")
    cost: Optional[int]
    network: Optional[Network] = Network.BROADCAST
    passive_interface: Optional[bool] = Field(False, vmanage_key="passive-interface")
    type: Type = Field(data_path=["authentication"])
    authentication_key: str = Field(vmanage_key="authentication-key", data_path=["authentication"])
    spi: Optional[int] = Field(data_path=["authentication", "ipsec"])

    class Config:
        allow_population_by_field_name = True


class RangeV6(BaseModel):
    address: ipaddress.IPv6Interface
    cost: Optional[int]
    no_advertise: Optional[bool] = Field(False, vmanage_key="no-advertise")

    class Config:
        allow_population_by_field_name = True


class AreaV6(ConvertBoolToStringModel):
    a_num: int = Field(vmanage_key="a-num")
    stub: Optional[bool] = Field(vmanage_key="no-summary", data_path=["stub"])
    nssa: Optional[bool] = Field(vmanage_key="no-summary", data_path=["nssa"])
    translate: Optional[Translate] = Field(data_path=["nssa"])
    normal: Optional[bool]
    interface: Optional[List[InterfaceV6]]
    range: Optional[List[RangeV6]]

    class Config:
        allow_population_by_field_name = True


class CiscoOspfv3Model(FeatureTemplate, ConvertIPToStringModel, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    router_id_v4: Optional[ipaddress.IPv4Address] = Field(
        vmanage_key="router-id", data_path=["ospfv3", "address-family", "ipv4"]
    )
    reference_bandwidth_v4: Optional[int] = Field(
        100,
        vmanage_key="reference-bandwidth",
        data_path=["ospfv3", "address-family", "ipv4", "auto-cost"],
    )
    rfc1583_v4: Optional[bool] = Field(
        True, vmanage_key="rfc1583", data_path=["ospfv3", "address-family", "ipv4", "compatible"]
    )
    originate_v4: Optional[bool] = Field(
        vmanage_key="originate", data_path=["ospfv3", "address-family", "ipv4", "default-information"]
    )
    always_v4: Optional[bool] = Field(
        vmanage_key="always",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv4",
            "default-information",
            "originate",
        ],
    )
    metric_v4: Optional[int] = Field(
        vmanage_key="metric",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv4",
            "default-information",
            "originate",
        ],
    )
    metric_type_v4: Optional[MetricType] = Field(
        vmanage_key="metric-type",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv4",
            "default-information",
            "originate",
        ],
    )
    external_v4: Optional[int] = Field(
        110, vmanage_key="external", data_path=["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"]
    )
    inter_area_v4: Optional[int] = Field(
        110,
        vmanage_key="inter-area",
        data_path=["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
    )
    intra_area_v4: Optional[int] = Field(
        110,
        vmanage_key="intra-area",
        data_path=["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
    )
    delay_v4: Optional[int] = Field(
        200, vmanage_key="delay", data_path=["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"]
    )
    initial_hold_v4: Optional[int] = Field(
        1000,
        vmanage_key="initial-hold",
        data_path=["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
    )
    max_hold_v4: Optional[int] = Field(
        10000,
        vmanage_key="max-hold",
        data_path=["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
    )
    distance_v4: Optional[int] = Field(
        110, vmanage_key="distance", data_path=["ospfv3", "address-family", "ipv4", "distance-ipv4"]
    )
    name_v4: Optional[str] = Field(vmanage_key="name", data_path=["ospfv3", "address-family", "ipv4", "table-map"])
    filter_v4: Optional[bool] = Field(vmanage_key="filter", data_path=["ospfv3", "address-family", "ipv4", "table-map"])
    redistribute_v4: Optional[List[Redistribute]] = Field(
        vmanage_key="redistribute", data_path=["ospfv3", "address-family", "ipv4"]
    )
    router_lsa_v4: Optional[List[RouterLsa]] = Field(
        vmanage_key="router-lsa", data_path=["ospfv3", "address-family", "ipv4", "max-metric"]
    )
    area_v4: Optional[List[Area]] = Field(vmanage_key="area", data_path=["ospfv3", "address-family", "ipv4"])
    router_id_v6: Optional[ipaddress.IPv4Address] = Field(
        vmanage_key="router-id", data_path=["ospfv3", "address-family", "ipv6"]
    )
    reference_bandwidth_v6: Optional[int] = Field(
        100,
        vmanage_key="reference-bandwidth",
        data_path=["ospfv3", "address-family", "ipv6", "auto-cost"],
    )
    rfc1583_v6: Optional[bool] = Field(
        True, vmanage_key="rfc1583", data_path=["ospfv3", "address-family", "ipv6", "compatible"]
    )
    originate_v6: Optional[bool] = Field(
        vmanage_key="originate", data_path=["ospfv3", "address-family", "ipv6", "default-information"]
    )
    always_v6: Optional[bool] = Field(
        vmanage_key="always",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv6",
            "default-information",
            "originate",
        ],
    )
    metric_v6: Optional[int] = Field(
        vmanage_key="metric",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv6",
            "default-information",
            "originate",
        ],
    )
    metric_type_v6: Optional[MetricType] = Field(
        vmanage_key="metric-type",
        data_path=[
            "ospfv3",
            "address-family",
            "ipv6",
            "default-information",
            "originate",
        ],
    )
    external_v6: Optional[int] = Field(
        110, vmanage_key="external", data_path=["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"]
    )
    inter_area_v6: Optional[int] = Field(
        110,
        vmanage_key="inter-area",
        data_path=["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
    )
    intra_area_v6: Optional[int] = Field(
        110,
        vmanage_key="intra-area",
        data_path=["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
    )
    delay_v6: Optional[int] = Field(
        200, vmanage_key="delay", data_path=["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"]
    )
    initial_hold_v6: Optional[int] = Field(
        1000,
        vmanage_key="initial-hold",
        data_path=["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
    )
    max_hold_v6: Optional[int] = Field(
        10000,
        vmanage_key="max-hold",
        data_path=["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
    )
    distance_v6: Optional[int] = Field(
        110, vmanage_key="distance", data_path=["ospfv3", "address-family", "ipv6", "distance-ipv6"]
    )
    name_v6: Optional[str] = Field(vmanage_key="name", data_path=["ospfv3", "address-family", "ipv6", "table-map"])
    filter_v6: Optional[bool] = Field(vmanage_key="filter", data_path=["ospfv3", "address-family", "ipv6", "table-map"])
    redistribute_v6: Optional[List[RedistributeV6]] = Field(
        vmanage_key="redistribute", data_path=["ospfv3", "address-family", "ipv6"]
    )
    router_lsa_v6: Optional[List[RouterLsa]] = Field(
        vmanage_key="router-lsa", data_path=["ospfv3", "address-family", "ipv6", "max-metric"]
    )
    area_v6: Optional[List[AreaV6]] = Field(vmanage_key="area", data_path=["ospfv3", "address-family", "ipv6"])

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospfv3"
