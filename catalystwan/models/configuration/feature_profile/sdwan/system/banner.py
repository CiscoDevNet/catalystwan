from __future__ import annotations

from typing import Literal, Union

from pydantic import ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase


class BannerParcel(_ParcelBase):
    type_: Literal["banner"] = Field(default="banner", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
    )
    login: Union[Variable, Global[str], Default[Literal[""]]] = Field(default="")
    motd: Union[Variable, Global[str], Default[Literal[""]]] = Field(default="")
