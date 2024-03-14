# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Any, List, Literal, Optional, Set, Tuple

from pydantic import BaseModel, Field

from catalystwan.models.common import InterfaceType
from catalystwan.models.policy.lists_entries import URLListEntry, VPNListEntry, ZoneListEntry


class PolicyListBase(BaseModel):
    name: str = Field(
        pattern="^[a-zA-Z0-9_-]{1,32}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 32 characters",
    )
    description: Optional[str] = "Desc Not Required"
    entries: List[Any]

    def _add_entry(self, entry: Any, single: bool = False) -> None:
        if self.entries and single:
            self.entries[0] = entry
            del self.entries[1:]
        else:
            self.entries.append(entry)


class VPNList(PolicyListBase):
    type: Literal["vpn"] = "vpn"
    entries: List[VPNListEntry] = []

    def add_vpns(self, vpns: Set[int]):
        for vpn in vpns:
            self._add_entry(VPNListEntry(vpn=(vpn, None)))

    def add_vpn_range(self, vpn_range: Tuple[int, int]):
        self._add_entry(VPNListEntry(vpn=vpn_range))


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=(vpn, None)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]


class URLAllowList(PolicyListBase):
    type: Literal["urlWhiteList"] = "urlWhiteList"
    entries: List[URLListEntry] = []


class URLBlockList(PolicyListBase):
    type: Literal["urlBlackList"] = "urlBlackList"
    entries: List[URLListEntry] = []
