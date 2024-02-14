from ipaddress import IPv4Address
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_address: Global[IPv4Address] = Field(serialization_alias="ipv4Address", validation_alias="ipv4Address")
    ipv4_prefix_length: Global[int] = Field(serialization_alias="ipv4PrefixLength", validation_alias="ipv4PrefixLength")


class PrefixListParcel(_ParcelBase):
    entries: List[PrefixListEntry] = Field(validation_alias=AliasPath("data", "entries"))
