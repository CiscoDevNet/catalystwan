from typing import List, Literal

from catalystwan.models.policy.lists_entries import AppProbeClassListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class AppProbeClassList(PolicyListBase):
    type: Literal["appProbe"] = "appProbe"
    entries: List[AppProbeClassListEntry] = []

    def assign_forwarding_class(self, name: str) -> AppProbeClassListEntry:
        # App probe class list must have only one entry!
        entry = AppProbeClassListEntry(forwarding_class=name)
        self._add_entry(entry, single=True)
        return entry


class AppProbeClassListEditPayload(AppProbeClassList, PolicyListId):
    pass


class AppProbeClassListInfo(AppProbeClassList, PolicyListInfo):
    pass
