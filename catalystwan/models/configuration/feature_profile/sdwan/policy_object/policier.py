from enum import Enum
from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class PolicerExceedActionEnum(str, Enum):
    DROP = "drop"
    REMARK = "remark"


class Burst(Global):
    value: int = Field(ge=15000, le=10_000_000)


class Exceed(Global):
    value: str


class Rate(Global):
    value: int = Field(ge=8, le=100_000_000_000)


class PolicierEntry(BaseModel):
    burst: Burst
    exceed: Exceed
    rate: Rate


class PolicierData(BaseModel):
    entries: List[PolicierEntry]


class PolicierPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.POLICER)
    data: PolicierData
