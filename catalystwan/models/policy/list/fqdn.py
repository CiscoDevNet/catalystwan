from typing import List, Literal

from catalystwan.models.policy.lists_entries import FQDNListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class FQDNList(PolicyListBase):
    type: Literal["fqdn"] = "fqdn"
    entries: List[FQDNListEntry] = []


class FQDNListEditPayload(FQDNList, PolicyListId):
    pass


class FQDNListInfo(FQDNList, PolicyListInfo):
    pass
