from ipaddress import IPv4Network
from typing import List, Literal, Optional

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import PrefixListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class PrefixList(PolicyListBase):
    type: Literal["prefix"] = "prefix"
    entries: List[PrefixListEntry] = []

    def add_prefix(self, prefix: IPv4Network, ge: Optional[int] = None, le: Optional[int] = None) -> None:
        self._add_entry(PrefixListEntry(ip_prefix=prefix, ge=ge, le=le))


class PrefixListEditPayload(PrefixList, PolicyListId):
    pass


class PrefixListInfo(PrefixList, PolicyListInfo):
    pass
