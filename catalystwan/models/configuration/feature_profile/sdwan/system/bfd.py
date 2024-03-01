from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor


class Color(BaseModel):
    color: Global[TLOCColor]
    hello_interval: Optional[Global[int]] = Field(
        default=as_global(1000), validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    multiplier: Optional[Global[int]] = as_global(7)
    pmtu_discovery: Optional[Global[bool]] = Field(
        default=as_global(True), validation_alias="pmtuDiscovery", serialization_alias="pmtuDiscovery"
    )
    dscp: Optional[Global[int]] = as_global(48)
    model_config = ConfigDict(populate_by_name=True)


class BFDParcel(_ParcelBase):
    type_: Literal["bfd"] = Field(default="bfd", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    multiplier: Optional[Global[int]] = Field(default=as_global(6), validation_alias=AliasPath("data", "multiplier"))
    poll_interval: Optional[Global[int]] = Field(
        default=as_global(600000),
        validation_alias=AliasPath("data", "pollInterval"),
        description="Poll Interval (In Millisecond)",
    )
    default_dscp: Optional[Global[int]] = Field(
        default=as_global(48),
        validation_alias=AliasPath("data", "defaultDscp"),
        description="DSCP Values for BFD Packets (decimal)",
    )
    colors: Optional[List[Color]] = Field(default=None, validation_alias=AliasPath("data", "colors"))

    def set_muliplier(self, value: int):
        self.multiplier = as_global(value)

    def set_poll_interval(self, value: int):
        self.poll_interval = as_global(value)

    def set_default_dscp(self, value: int):
        self.default_dscp = as_global(value)

    def add_color(
        self,
        color: TLOCColor,
        hello_interval: int = 1000,
        multiplier: int = 7,
        pmtu_discovery: bool = True,
        dscp: int = 48,
    ):
        if not self.colors:
            self.colors = []
        self.colors.append(
            Color(
                color=Global[TLOCColor](value=color),
                hello_interval=as_global(hello_interval),
                multiplier=as_global(multiplier),
                pmtu_discovery=as_global(pmtu_discovery),
                dscp=as_global(dscp),
            )
        )
