from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class URLAllowListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str]


class URLAllowParcel(_ParcelBase):
    entries: List[URLAllowListEntry] = Field(validation_alias=AliasPath("data", "entries"))
    parcel_type: str = Field(default="urlallowed", validation_alias="type", serialization_alias="type")
