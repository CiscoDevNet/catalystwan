from typing import List, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor
from catalystwan.models.configuration.feature_profile.converters.recast import (
    DefaultGlobalBool,
    DefaultGlobalColorLiteral,
)

DEFAULT_BFD_COLOR_MULTIPLIER = as_global(7)
DEFAULT_BFD_DSCP = as_global(48)
DEFAULT_BFD_HELLO_INTERVAL = as_global(1000)
DEFAULT_BFD_POLL_INTERVAL = as_global(600000)
DEFAULT_BFD_MULTIPLIER = as_global(6)


class Color(BaseModel):
    color: Union[DefaultGlobalColorLiteral, Global[TLOCColor]]
    hello_interval: Optional[Global[int]] = Field(
        default=DEFAULT_BFD_HELLO_INTERVAL, validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    multiplier: Optional[Global[int]] = DEFAULT_BFD_COLOR_MULTIPLIER
    pmtu_discovery: Optional[Union[DefaultGlobalBool, Global[bool]]] = Field(
        default=as_global(True), validation_alias="pmtuDiscovery", serialization_alias="pmtuDiscovery"
    )
    dscp: Optional[Global[int]] = DEFAULT_BFD_DSCP
    model_config = ConfigDict(populate_by_name=True)


class BFD(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    multiplier: Optional[Global[int]] = Field(
        default=DEFAULT_BFD_MULTIPLIER, validation_alias=AliasPath("data", "multiplier")
    )
    poll_interval: Optional[Global[int]] = Field(
        default=DEFAULT_BFD_POLL_INTERVAL, validation_alias=AliasPath("data", "pollInterval")
    )
    default_dscp: Optional[Global[int]] = Field(
        default=DEFAULT_BFD_DSCP, validation_alias=AliasPath("data", "defaultDscp")
    )
    colors: Optional[List[Color]] = Field(default=None, validation_alias=AliasPath("data", "colors"))
