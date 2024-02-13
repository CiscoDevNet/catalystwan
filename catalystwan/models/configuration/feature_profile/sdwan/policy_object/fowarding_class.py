from typing import List

from pydantic import AliasPath, BaseModel, Field, PrivateAttr, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class QueueEntry(BaseModel):
    queue: Global[int]

    @field_validator("queue")
    @classmethod
    def check_burst(cls, queue: Global):
        assert 0 <= int(queue.value) <= 9
        return queue


class FowardingClassParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.CLASS)
    entries: List[QueueEntry] = Field(validation_alias=AliasPath("data", "entries"))
