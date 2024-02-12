from ipaddress import IPv6Address
from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Ipv6Address(Global):
    value: IPv6Address


class Ipv6PrefixLength(Global):
    value: int


class IPv6PrefixListEntry(BaseModel):
    ipv6_address: Ipv6Address = Field(alias="ipv6Address")
    ipv6_prefix_length: Ipv6PrefixLength = Field(alias="ipv6PrefixLength")


class IPv6PrefixListData(BaseModel):
    entries: List[IPv6PrefixListEntry]


class IPv6PrefixListPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.IPV6_PREFIX)
    data = IPv6PrefixListData
