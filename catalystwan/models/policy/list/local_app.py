from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import LocalAppListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class LocalAppList(PolicyListBase):
    type: Literal["localApp"] = "localApp"
    entries: List[LocalAppListEntry] = []


class LocalAppListEditPayload(LocalAppList, PolicyListId):
    pass


class LocalAppListInfo(LocalAppList, PolicyListInfo):
    pass
