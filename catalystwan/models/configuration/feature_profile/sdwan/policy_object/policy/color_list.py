from typing import List

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor


class ColorEntry(BaseModel):
    color: Global[TLOCColor]


class ColorParcel(_ParcelBase):
    entries: List[ColorEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_color(self, color: TLOCColor):
        self.entries.append(ColorEntry(color=as_global(color, TLOCColor)))
