from ipaddress import IPv4Network
from typing import List, Literal

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import DataPrefixListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class DataPrefixList(PolicyListBase):
    type: Literal["dataPrefix"] = "dataPrefix"
    entries: List[DataPrefixListEntry] = []

    def add_prefix(self, ip_prefix: IPv4Network) -> None:
        self._add_entry(DataPrefixListEntry(ip_prefix=ip_prefix))


class DataPrefixListEditPayload(DataPrefixList, PolicyListId):
    pass


class DataPrefixListInfo(DataPrefixList, PolicyListInfo):
    pass
