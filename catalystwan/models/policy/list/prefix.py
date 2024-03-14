# Copyright 2022 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ip_prefix: IPv4Network = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")
    ge: Optional[IntStr] = Field(default=None, ge=0, le=32)
    le: Optional[IntStr] = Field(default=None, ge=0, le=32)


class PrefixList(PolicyListBase):
    type: Literal["prefix"] = "prefix"
    entries: List[PrefixListEntry] = []

    def add_prefix(self, prefix: IPv4Network, ge: Optional[int] = None, le: Optional[int] = None) -> None:
        self._add_entry(PrefixListEntry(ip_prefix=prefix, ge=ge, le=le))


class PrefixListEditPayload(PrefixList, PolicyListId):
    pass


class PrefixListInfo(PrefixList, PolicyListInfo):
    pass
