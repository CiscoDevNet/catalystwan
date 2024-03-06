# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

DEFAULT_BFD_COLOR_MULTIPLIER = 7
DEFAULT_BFD_DSCP = 48
DEFAULT_BFD_HELLO_INTERVAL = 1000
DEFAULT_BFD_POLL_INTERVAL = 600000
DEFAULT_BFD_MULTIPLIER = 6


class ColorType(str, Enum):
    DEFAULT = "default"
    MPLS = "mpls"
    METRO_ETHERNET = "metro-ethernet"
    BIZ_INTERNET = "biz-internet"
    PUBLIC_INTERNET = "public-internet"
    LTE = "lte"
    THREEG = "3g"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    CUSTOM1 = "custom1"
    CUSTOM2 = "custom2"
    CUSTOM3 = "custom3"
    PRIVATE1 = "private1"
    PRIVATE2 = "private2"
    PRIVATE3 = "private3"
    PRIVATE4 = "private4"
    PRIVATE5 = "private5"
    PRIVATE6 = "private6"


class Color(FeatureTemplateValidator):
    color: ColorType
    hello_interval: Optional[int] = Field(
        DEFAULT_BFD_HELLO_INTERVAL, json_schema_extra={"vmanage_key": "hello-interval"}
    )
    multiplier: Optional[int] = DEFAULT_BFD_COLOR_MULTIPLIER
    pmtu_discovery: Optional[BoolStr] = Field(default=True, json_schema_extra={"vmanage_key": "pmtu-discovery"})
    dscp: Optional[int] = DEFAULT_BFD_DSCP
    model_config = ConfigDict(populate_by_name=True)


class CiscoBFDModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    multiplier: Optional[int] = Field(DEFAULT_BFD_MULTIPLIER, json_schema_extra={"data_path": ["app-route"]})
    poll_interval: Optional[int] = Field(
        DEFAULT_BFD_POLL_INTERVAL, json_schema_extra={"vmanage_key": "poll-interval", "data_path": ["app-route"]}
    )
    default_dscp: Optional[int] = Field(DEFAULT_BFD_DSCP, json_schema_extra={"vmanage_key": "default-dscp"})
    color: Optional[List[Color]] = None

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bfd"
