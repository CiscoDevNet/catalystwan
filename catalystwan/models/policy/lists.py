# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Any, List, Literal, Optional, Set

from pydantic import BaseModel, Field

from catalystwan.models.common import InterfaceType
from catalystwan.models.policy.lists_entries import ZoneListEntry


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


class ZoneList(PolicyListBase):
    type: Literal["zone"] = "zone"
    entries: List[ZoneListEntry] = []

    def assign_vpns(self, vpns: Set[int]) -> None:
        self.entries = [ZoneListEntry(vpn=(vpn, None)) for vpn in vpns]

    def assign_interfaces(self, ifs: Set[InterfaceType]) -> None:
        self.entries = [ZoneListEntry(interface=interface) for interface in ifs]
