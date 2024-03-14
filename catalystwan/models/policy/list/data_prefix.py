# Copyright 2022 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class DataPrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ip_prefix: IPv4Network = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")


class DataPrefixList(PolicyListBase):
    type: Literal["dataPrefix"] = "dataPrefix"
    entries: List[DataPrefixListEntry] = []

    def add_prefix(self, ip_prefix: IPv4Network) -> None:
        self._add_entry(DataPrefixListEntry(ip_prefix=ip_prefix))


class DataPrefixListEditPayload(DataPrefixList, PolicyListId):
    pass


class DataPrefixListInfo(DataPrefixList, PolicyListInfo):
    pass
