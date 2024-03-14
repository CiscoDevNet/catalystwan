from typing import List, Literal

from catalystwan.models.policy.lists_entries import PolicerExceedAction, PolicerListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class PolicerList(PolicyListBase):
    type: Literal["policer"] = "policer"
    entries: List[PolicerListEntry] = []

    def police(self, burst: int, rate: int, exceed: PolicerExceedAction = "drop") -> None:
        # Policer list must have only single entry!
        entry = PolicerListEntry(burst=burst, exceed=exceed, rate=rate)
        self._add_entry(entry, single=True)


class PolicerListEditPayload(PolicerList, PolicyListId):
    pass


class PolicerListInfo(PolicerList, PolicyListInfo):
    pass
