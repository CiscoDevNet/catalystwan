from typing import List

from pydantic import AliasPath, BaseModel, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class FowardingClassQueueEntry(BaseModel):
    queue: Global[str]

    @field_validator("queue")
    @classmethod
    def check_burst(cls, queue: Global):
        assert 0 <= int(queue.value) <= 7
        return queue


class FowardingClassParcel(_ParcelBase):
    entries: List[FowardingClassQueueEntry] = Field(validation_alias=AliasPath("data", "entries"))
