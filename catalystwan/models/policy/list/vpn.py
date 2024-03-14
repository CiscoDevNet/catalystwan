from typing import List, Literal, Set, Tuple

from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import VPNListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class VPNList(PolicyListBase):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry] = []

    def add_vpns(self, vpns: Set[int]):
        for vpn in vpns:
            self._add_entry(VPNListEntry(vpn=(vpn, None)))

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        self._add_entry(VPNListEntry(vpn=vpn_range))


class VPNListEditPayload(VPNList, PolicyListId):
    pass


class VPNListInfo(VPNList, PolicyListInfo):
    pass
