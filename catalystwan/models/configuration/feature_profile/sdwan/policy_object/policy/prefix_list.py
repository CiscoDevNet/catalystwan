# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network
from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_address: Global[IPv4Address] = Field(serialization_alias="ipv4Address", validation_alias="ipv4Address")
    ipv4_prefix_length: Global[int] = Field(serialization_alias="ipv4PrefixLength", validation_alias="ipv4PrefixLength")


class PrefixListParcel(_ParcelBase):
    type_: Literal["prefix"] = Field(default="prefix", exclude=True)
    entries: List[PrefixListEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ipv4_network: IPv4Network):
        self.entries.append(
            PrefixListEntry(
                ipv4_address=as_global(ipv4_network.network_address),
                ipv4_prefix_length=as_global(ipv4_network.prefixlen),
            )
        )
