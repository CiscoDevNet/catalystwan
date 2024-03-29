# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Address, IPv6Network
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class IPv6DataPrefixEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv6_address: Global[IPv6Address] = Field(serialization_alias="ipv6Address", validation_alias="ipv6Address")
    ipv6_prefix_length: Global[int] = Field(serialization_alias="ipv6PrefixLength", validation_alias="ipv6PrefixLength")


class IPv6DataPrefixParcel(_ParcelBase):
    entries: List[IPv6DataPrefixEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ipv6_network: IPv6Network):
        self.entries.append(
            IPv6DataPrefixEntry(
                ipv6_address=as_global(ipv6_network.network_address),
                ipv6_prefix_length=as_global(ipv6_network.prefixlen),
            )
        )
