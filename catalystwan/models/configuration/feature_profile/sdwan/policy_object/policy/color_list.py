# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor


class ColorEntry(BaseModel):
    color: Global[TLOCColor]


class ColorParcel(_ParcelBase):
    type_: Literal["color"] = Field(default="color", exclude=True)
    entries: List[ColorEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_color(self, color: TLOCColor):
        self.entries.append(ColorEntry(color=as_global(color, TLOCColor)))
