from ipaddress import IPv6Address, IPv6Network
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class IPv6PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv6_address: Global[IPv6Address] = Field(serialization_alias="ipv6Address", validation_alias="ipv6Address")
    ipv6_prefix_length: Global[int] = Field(serialization_alias="ipv6PrefixLength", validation_alias="ipv6PrefixLength")


class IPv6PrefixListParcel(_ParcelBase):
    entries: List[IPv6PrefixListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ipv6_network: IPv6Network):
        self.entries.append(
            IPv6PrefixListEntry(
                ipv6_address=as_global(ipv6_network.network_address),
                ipv6_prefix_length=as_global(ipv6_network.prefixlen),
            )
        )
