from typing import List, Literal

from catalystwan.models.policy.lists_entries import URLListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class URLAllowList(PolicyListBase):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry] = []


class URLAllowListEditPayload(URLAllowList, PolicyListId):
    pass


class URLAllowListInfo(URLAllowList, PolicyListInfo):
    pass


class URLBlockList(PolicyListBase):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry] = []


class URLBlockListEditPayload(URLBlockList, PolicyListId):
    pass


class URLBlockListInfo(URLBlockList, PolicyListInfo):
    pass
