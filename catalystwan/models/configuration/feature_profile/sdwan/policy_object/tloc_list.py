from ipaddress import IPv4Address
from typing import List, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import TLOCColorEnum
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType
from catalystwan.models.policy.lists_entries import EncapEnum


class TlocEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tloc: Global[IPv4Address]
    color: Global[TLOCColorEnum]
    encapsulation: Global[EncapEnum] = Field(serialization_alias="encap", validation_alias="encap")
    preference: Optional[Global[str]] = None

    @field_validator("preference")
    @classmethod
    def ensure_correct_preference_value(cls, v: Global):
        if not v:
            return v
        if 0 < int(v.value) < 4_294_967_295:
            raise ValueError('"value" not in range 0 - 4 294 967 295 (2 ** 32 - 1)')
        return v


class TlocParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.TLOC)
    entries: List[TlocEntry] = Field(validation_alias=AliasPath("data", "entries"))
