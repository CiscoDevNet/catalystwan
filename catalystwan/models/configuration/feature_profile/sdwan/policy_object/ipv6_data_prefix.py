from ipaddress import IPv6Address
from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Ipv6Address(Global):
    value: IPv6Address


class Ipv6PrefixLength(Global):
    value: int


class IPv6DataPrefixEntry(BaseModel):
    ipv6_address: Ipv6Address = Field(alias="ipv6Address")
    ipv6_prefix_length: Ipv6PrefixLength = Field(alias="ipv6PrefixLength")


class IPv6DataPrefixData(BaseModel):
    entries: List[IPv6DataPrefixEntry]


class IPv6DataPrefixPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.DATA_IPV6_PREFIX)
    data: IPv6DataPrefixData
