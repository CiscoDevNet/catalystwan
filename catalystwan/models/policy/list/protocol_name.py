from typing import List, Literal

from catalystwan.models.policy.lists_entries import ProtocolNameListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ProtocolNameList(PolicyListBase):
    type: Literal["protocolName"] = "protocolName"
    entries: List[ProtocolNameListEntry] = []


class ProtocolNameListEditPayload(ProtocolNameList, PolicyListId):
    pass


class ProtocolNameListInfo(ProtocolNameList, PolicyListInfo):
    pass
