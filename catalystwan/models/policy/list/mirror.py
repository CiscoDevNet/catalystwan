from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import MirrorListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class MirrorList(PolicyListBase):
    type: Literal["mirror"] = "mirror"
    entries: List[MirrorListEntry] = []


class MirrorListEditPayload(MirrorList, PolicyListId):
    pass


class MirrorListInfo(MirrorList, PolicyListInfo):
    pass
