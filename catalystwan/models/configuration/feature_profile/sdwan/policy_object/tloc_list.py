from enum import Enum
from ipaddress import IPv4Address
from typing import List, Optional

from pydantic import BaseModel, Field, PrivateAttr, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.color_list import ColorType
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Encapsulation(str, Enum):
    IPSEC = "ipsec"
    GRE = "gre"


class Preference(Global):
    value: str = Field(description="Number in range 0-4294967295")  # 2 ** 32 - 1

    @field_validator("value")
    @classmethod
    def ensure_correct_value(cls, v: str):
        if 0 < int(v) < 4_294_967_295:
            raise ValueError('"value" not in range 0 - 4 294 967 295 (2 ** 32 - 1)')
        return v


class TlocIPv4Address(Global):
    value: IPv4Address


class TlocEntry(BaseModel):
    tloc: TlocIPv4Address
    color: ColorType
    encapsulation: Encapsulation = Field(alias="encap")
    preference: Optional[Preference] = None


class TlocData(_ParcelBase):
    entries: List[TlocEntry]


class TlocPayload(BaseModel):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.TLOC)
    data: TlocData
