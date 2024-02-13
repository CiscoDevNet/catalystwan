from ipaddress import IPv4Address
from typing import List

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv4_address: Global[IPv4Address] = Field(serialization_alias="ipv4Address", validation_alias="ipv4Address")
    ipv4_prefix_length: Global[int] = Field(serialization_alias="ipv4PrefixLength", validation_alias="ipv4PrefixLength")


class PrefixListParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.PREFIX)
    entries: List[PrefixListEntry]
