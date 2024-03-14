# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from catalystwan.models.policy.lists_entries import LocalDomainListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class LocalDomainList(PolicyListBase):
    type: Literal["localDomain"] = "localDomain"
    entries: List[LocalDomainListEntry] = []


class LocalDomainListEditPayload(LocalDomainList, PolicyListId):
    pass


class LocalDomainListInfo(LocalDomainList, PolicyListInfo):
    pass
