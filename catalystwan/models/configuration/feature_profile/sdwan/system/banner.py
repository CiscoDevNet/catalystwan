from __future__ import annotations

from typing import Literal, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default, as_global

EmptyString = Literal[""]


class BannerParcel(_ParcelBase):
    type_: Literal["banner"] = Field(default="banner", exclude=True)

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    login: Union[Variable, Global[str], Default[EmptyString], str] = Field(
        default=as_default("", EmptyString), validation_alias=AliasPath("data", "login")
    )
    motd: Union[Variable, Global[str], Default[EmptyString]] = Field(
        default=as_default("", EmptyString),
        validation_alias=AliasPath("data", "motd"),
        description="Message of the day",
    )

    def add_login(self, value: str):
        self.login = as_global(value)

    def add_motd(self, value: str):
        self.motd = as_global(value)
