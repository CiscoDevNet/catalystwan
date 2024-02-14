from typing import List

from pydantic import AliasPath, BaseModel, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import TLOCColorEnum


class ColorEntry(BaseModel):
    color: Global[TLOCColorEnum]


class ColorParcel(_ParcelBase):
    entries: List[ColorEntry] = Field(validation_alias=AliasPath("data", "entries"))
