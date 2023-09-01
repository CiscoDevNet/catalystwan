from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertBoolToStringModel


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
    hello_interval: Optional[int] = Field(1000, alias="hello-interval")
    multiplier: Optional[int] = 7
    pmtu_discovery: Optional[bool] = Field(True, alias="pmtu-discovery")
    dscp: Optional[int] = 48

    class Config:
        allow_population_by_field_name = True


class CiscoBFDModel(FeatureTemplate, ConvertBoolToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    multiplier: Optional[int] = 6
    poll_interval: Optional[int] = Field(600000, alias="poll-interval")
    default_dscp: Optional[int] = Field(48, alias="default-dscp")
    color: Optional[List[Color]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bfd"
