# Copyright 2022 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from catalystwan.models.common import EncapType, IntStr, TLOCColor
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class TLOCListEntry(BaseModel):
    tloc: IPv4Address
    color: TLOCColor
    encap: EncapType
    preference: Optional[IntStr] = Field(default=None, ge=0, le=2**32 - 1)


class TLOCList(PolicyListBase):
    type: Literal["tloc"] = "tloc"
    entries: List[TLOCListEntry] = []

    def add_tloc(self, tloc: IPv4Address, color: TLOCColor, encap: EncapType, preference: Optional[int] = None) -> None:
        self.entries.append(TLOCListEntry(tloc=tloc, color=color, encap=encap, preference=preference))


class TLOCListEditPayload(TLOCList, PolicyListId):
    pass


class TLOCListInfo(TLOCList, PolicyListInfo):
    pass
