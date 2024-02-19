from typing import List

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColorEnum


class ColorEntry(BaseModel):
    color: Global[TLOCColorEnum]


class ColorParcel(_ParcelBase):
    entries: List[ColorEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_color(self, color: TLOCColorEnum):
        self.entries.append(ColorEntry(color=as_global(color)))
