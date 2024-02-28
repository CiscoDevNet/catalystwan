from __future__ import annotations

from typing import Literal, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default


class BannerParcel(_ParcelBase):
    type_: Literal["banner"] = Field(default="banner", exclude=True)

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    login: Union[Variable, Global[str], Default[Literal[""]]] = Field(
        default=as_default(""), validation_alias=AliasPath("data", "login")
    )
    motd: Union[Variable, Global[str], Default[Literal[""]]] = Field(
        default=as_default(""), validation_alias=AliasPath("data", "motd")
    )
