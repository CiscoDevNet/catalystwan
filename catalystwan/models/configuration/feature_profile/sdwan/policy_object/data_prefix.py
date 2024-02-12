from ipaddress import IPv4Address
from typing import List

from pydantic import BaseModel, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class Ipv4Address(Global):
    value: IPv4Address


class Ipv4PrefixLength(Global):
    value: int


class DataPrefixEntry(BaseModel):
    ipv4_address: Ipv4Address = Field(alias="ipv4Address")
    ipv4_prefix_length: Ipv4PrefixLength = Field(alias="ipv4PrefixLength")


class DataPrefixData(BaseModel):
    entries: List[DataPrefixEntry]


class DataPrefixPayload(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.DATA_PREFIX)
    data = DataPrefixData
