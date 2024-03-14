# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Set

from catalystwan.models.common import InterfaceType
from catalystwan.models.policy.lists_entries import ZoneListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=(vpn, None)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]


class ZoneListEditPayload(ZoneList, PolicyListId):
    pass


class ZoneListInfo(ZoneList, PolicyListInfo):
    pass
