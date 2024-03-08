# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor


class AppProbeMapItem(BaseModel):
    color: Global[TLOCColor]
    dscp: Global[int]

    @field_validator("dscp")
    @classmethod
    def check_rate(cls, dscp: Global):
        assert 0 <= int(dscp.value) <= 63
        return dscp


class AppProbeEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    map: List[AppProbeMapItem] = Field(default=[])
    forwarding_class_name: Global[str] = Field(
        serialization_alias="forwardingClass", validation_alias="forwardingClass"
    )


class AppProbeParcel(_ParcelBase):
    type_: Literal["app-probe"] = Field(default="app-probe", exclude=True)
    entries: List[AppProbeEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_fowarding_class(self, forwarding_class_name: str):
        self.entries.append(
            AppProbeEntry(
                forwarding_class_name=as_global(forwarding_class_name),
            )
        )

    def add_map(self, color: TLOCColor, dscp: int):
        entry = self.entries[0]
        entry.map.append(AppProbeMapItem(color=as_global(color, TLOCColor), dscp=as_global(dscp)))
