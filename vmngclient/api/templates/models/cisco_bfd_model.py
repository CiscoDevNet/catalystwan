from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel

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


class Color(ConvertBoolToStringModel):
    color: ColorType
    hello_interval: Optional[int] = Field(DEFAULT_BFD_HELLO_INTERVAL, alias="hello-interval")
    multiplier: Optional[int] = DEFAULT_BFD_COLOR_MULTIPLIER
    pmtu_discovery: Optional[bool] = Field(True, alias="pmtu-discovery")
    dscp: Optional[int] = DEFAULT_BFD_DSCP
    model_config = ConfigDict(populate_by_name=True)


class CiscoBFDModel(FeatureTemplate, ConvertBoolToStringModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    multiplier: Optional[int] = DEFAULT_BFD_MULTIPLIER
    poll_interval: Optional[int] = Field(DEFAULT_BFD_POLL_INTERVAL, alias="poll-interval")
    default_dscp: Optional[int] = Field(DEFAULT_BFD_DSCP, alias="default-dscp")
    color: Optional[List[Color]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bfd"
