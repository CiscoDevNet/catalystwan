from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType
from catalystwan.models.policy.lists_entries import PolicerExceedActionEnum


class PolicierEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    burst: Global[str]
    exceed: Global[PolicerExceedActionEnum]
    rate: Global[str]

    @field_validator("burst")
    @classmethod
    def check_burst(cls, burst_str: Global):
        assert 15000 <= int(burst_str.value) <= 10_000_000
        return burst_str

    @field_validator("rate")
    @classmethod
    def check_rate(cls, rate_str: Global):
        assert 8 <= int(rate_str.value) <= 100_000_000_000
        return rate_str


class PolicierParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.POLICER)
    entries: List[PolicierEntry] = Field(validation_alias=AliasPath("data", "entries"))
