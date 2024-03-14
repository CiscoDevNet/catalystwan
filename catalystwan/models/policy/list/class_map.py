# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ClassMapListEntry(BaseModel):
    queue: IntStr = Field(ge=0, le=7)


class ClassMapList(PolicyListBase):
    type: Literal["class"] = "class"
    entries: List[ClassMapListEntry] = []

    def assign_queue(self, queue: int) -> None:
        # Class map list must have only one entry!
        entry = ClassMapListEntry(queue=queue)
        self._add_entry(entry, single=True)


class ClassMapListEditPayload(ClassMapList, PolicyListId):
    pass


class ClassMapListInfo(ClassMapList, PolicyListInfo):
    pass
