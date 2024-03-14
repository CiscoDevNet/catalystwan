# Copyright 2022 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Interface
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class DataIPv6PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ipv6_prefix: IPv6Interface = Field(serialization_alias="ipv6Prefix", validation_alias="ipv6Prefix")


class DataIPv6PrefixList(PolicyListBase):
    type: Literal["dataIpv6Prefix"] = "dataIpv6Prefix"
    entries: List[DataIPv6PrefixListEntry] = []

    def add_prefix(self, ipv6_prefix: IPv6Interface) -> None:
        self._add_entry(DataIPv6PrefixListEntry(ipv6_prefix=ipv6_prefix))


class DataIPv6PrefixListEditPayload(DataIPv6PrefixList, PolicyListId):
    pass


class DataIPv6PrefixListInfo(DataIPv6PrefixList, PolicyListInfo):
    pass
