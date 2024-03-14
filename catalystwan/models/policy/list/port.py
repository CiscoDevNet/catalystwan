from typing import List, Literal

from catalystwan.models.policy.lists_entries import PortListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class PortList(PolicyListBase):
    type: Literal["port"] = "port"
    entries: List[PortListEntry] = []


class PortListEditPayload(PortList, PolicyListId):
    pass


class PortListInfo(PortList, PolicyListInfo):
    pass
