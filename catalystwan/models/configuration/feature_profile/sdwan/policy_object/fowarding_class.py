from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Queue(Global):
    value: int = Field(ge=0, le=9)


class QueueEntry(BaseModel):
    queue: Queue


class FowardingClassData(BaseModel):
    entries: List[QueueEntry]


class FowardingClassPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.CLASS)
    data: FowardingClassData
