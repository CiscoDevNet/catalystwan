from typing import List, Literal

from catalystwan.models.policy.lists_entries import ASPathListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ASPathList(PolicyListBase):
    type: Literal["asPath"] = "asPath"
    entries: List[ASPathListEntry] = []


class ASPathListEditPayload(ASPathList, PolicyListId):
    pass


class ASPathListInfo(ASPathList, PolicyListInfo):
    pass
