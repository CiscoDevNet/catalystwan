# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class FowardingClassQueueEntry(BaseModel):
    queue: Global[str]

    @field_validator("queue")
    @classmethod
    def check_burst(cls, queue: Global):
        assert 0 <= int(queue.value) <= 7
        return queue


class FowardingClassParcel(_ParcelBase):
    type_: Literal["class"] = Field(default="class", exclude=True)
    entries: List[FowardingClassQueueEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_queue(self, queue: int):
        self.entries.append(FowardingClassQueueEntry(queue=as_global(str(queue))))
