# Copyright 2022 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Interface
from typing import List, Literal, Optional

from catalystwan.models.policy.lists_entries import IPv6PrefixListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class IPv6PrefixList(PolicyListBase):
    type: Literal["ipv6prefix"] = "ipv6prefix"
    entries: List[IPv6PrefixListEntry] = []

    def add_prefix(self, prefix: IPv6Interface, ge: Optional[int] = None, le: Optional[int] = None) -> None:
        self._add_entry(IPv6PrefixListEntry(ipv6_prefix=prefix, ge=ge, le=le))


class IPv6PrefixListEditPayload(IPv6PrefixList, PolicyListId):
    pass


class IPv6PrefixListInfo(IPv6PrefixList, PolicyListInfo):
    pass
