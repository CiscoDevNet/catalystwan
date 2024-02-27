# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class BaseURLListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str]


class BaseURLParcel(_ParcelBase):
    entries: List[BaseURLListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_url(self, pattern: str):
        self.entries.append(BaseURLListEntry(pattern=as_global(pattern)))


class URLAllowParcel(BaseURLParcel):
    parcel_type: str = Field(default="urlallowed", validation_alias="type", serialization_alias="type")


class URLBlockParcel(BaseURLParcel):
    parcel_type: str = Field(default="urlblocked", validation_alias="type", serialization_alias="type")
