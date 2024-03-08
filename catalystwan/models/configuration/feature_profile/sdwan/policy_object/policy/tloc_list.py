# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import TLOCColor

EncapType = Literal[
    "ipsec",
    "gre",
]


class TlocEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tloc: Global[IPv4Address]
    color: Global[TLOCColor]
    encapsulation: Global[EncapType] = Field(serialization_alias="encap", validation_alias="encap")
    preference: Optional[Global[str]] = None

    @field_validator("preference")
    @classmethod
    def ensure_correct_preference_value(cls, v: Global):
        if not v:
            return v
        if not (0 <= int(v.value) < 4_294_967_295):
            raise ValueError('"preference" not in range 0 - 4 294 967 295 (2 ** 32 - 1)')
        return v


class TlocParcel(_ParcelBase):
    type_: Literal["tloc"] = Field(default="tloc", exclude=True)
    entries: List[TlocEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_entry(
        self, tloc: IPv4Address, color: TLOCColor, encapsulation: EncapType, preference: Optional[str] = None
    ):
        self.entries.append(
            TlocEntry(
                tloc=as_global(tloc),
                color=as_global(color, TLOCColor),
                encapsulation=as_global(encapsulation, EncapType),
                preference=as_global(preference) if preference is not None else None,
            )
        )
