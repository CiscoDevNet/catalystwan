from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import TLOCColorEnum


class MapItem(BaseModel):
    color: Global[TLOCColorEnum]
    dscp: Global[int]

    @field_validator("dscp")
    @classmethod
    def check_rate(cls, dscp: Global):
        assert 0 <= int(dscp.value) <= 63
        return dscp


class AppProbeEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    map: List[MapItem]
    forwarding_class_name: Global[str] = Field(
        serialization_alias="forwardingClass", validation_alias="forwardingClass"
    )


class AppProbeParcel(_ParcelBase):
    entries: List[AppProbeEntry] = Field(validation_alias=AliasPath("data", "entries"))
