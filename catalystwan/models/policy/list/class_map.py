from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import ClassMapListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


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
