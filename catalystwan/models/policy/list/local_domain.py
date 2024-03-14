from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import LocalDomainListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class LocalDomainList(PolicyListBase):
    type: Literal["localDomain"] = "localDomain"
    entries: List[LocalDomainListEntry] = []


class LocalDomainListEditPayload(LocalDomainList, PolicyListId):
    pass


class LocalDomainListInfo(LocalDomainList, PolicyListInfo):
    pass
