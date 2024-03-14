from ipaddress import IPv4Address
from typing import List, Literal, Optional

from catalystwan.models.common import EncapType, TLOCColor
from catalystwan.models.policy.lists import PolicyListBase
from catalystwan.models.policy.lists_entries import TLOCListEntry
from catalystwan.models.policy.policy_list import PolicyListId, PolicyListInfo


class TLOCList(PolicyListBase):
    type: Literal["tloc"] = "tloc"
    entries: List[TLOCListEntry] = []

    def add_tloc(self, tloc: IPv4Address, color: TLOCColor, encap: EncapType, preference: Optional[int] = None) -> None:
        self.entries.append(TLOCListEntry(tloc=tloc, color=color, encap=encap, preference=preference))


class TLOCListEditPayload(TLOCList, PolicyListId):
    pass


class TLOCListInfo(TLOCList, PolicyListInfo):
    pass
