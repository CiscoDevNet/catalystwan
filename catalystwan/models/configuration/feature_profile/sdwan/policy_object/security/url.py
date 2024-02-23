from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class BaseURLListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str]


class BaseURLParcel(_ParcelBase):
    type_: Literal["security-urllist"] = Field(default="security-urllist", exclude=True)
    entries: List[BaseURLListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_url(self, pattern: str):
        self.entries.append(BaseURLListEntry(pattern=as_global(pattern)))


class URLAllowParcel(BaseURLParcel):
    type_: Literal["security-urllist"] = Field(default="security-urllist", exclude=True)
    parcel_type: Literal["urlallowed"] = Field(
        default="urlallowed", validation_alias="type", serialization_alias="type"
    )


class URLBlockParcel(BaseURLParcel):
    type_: Literal["security-urllist"] = Field(default="security-urllist", exclude=True)
    parcel_type: Literal["urlblocked"] = Field(
        default="urlblocked", validation_alias="type", serialization_alias="type"
    )
