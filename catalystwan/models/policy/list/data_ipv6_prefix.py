from ipaddress import IPv6Interface
from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import DataIPv6PrefixListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class DataIPv6PrefixList(PolicyListBase):
    type: Literal["dataIpv6Prefix"] = "dataIpv6Prefix"
    entries: List[DataIPv6PrefixListEntry] = []

    def add_prefix(self, ipv6_prefix: IPv6Interface) -> None:
        self._add_entry(DataIPv6PrefixListEntry(ipv6_prefix=ipv6_prefix))


class DataIPv6PrefixListEditPayload(DataIPv6PrefixList, PolicyListId):
    pass


class DataIPv6PrefixListInfo(DataIPv6PrefixList, PolicyListInfo):
    pass
