from typing import List, Literal

from catalystwan.models.policy.lists_entries import IPSSignatureListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class IPSSignatureList(PolicyListBase):
    type: Literal["ipsSignature"] = "ipsSignature"
    entries: List[IPSSignatureListEntry] = []


class IPSSignatureListEditPayload(IPSSignatureList, PolicyListId):
    pass


class IPSSignatureListInfo(IPSSignatureList, PolicyListInfo):
    pass
