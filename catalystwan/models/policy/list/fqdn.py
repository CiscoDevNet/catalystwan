# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class FQDNListEntry(BaseModel):
    pattern: str


class FQDNList(PolicyListBase):
    type: Literal["fqdn"] = "fqdn"
    entries: List[FQDNListEntry] = []


class FQDNListEditPayload(FQDNList, PolicyListId):
    pass


class FQDNListInfo(FQDNList, PolicyListInfo):
    pass
