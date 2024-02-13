from ipaddress import IPv6Address
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class IPv6PrefixListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ipv6_address: Global[IPv6Address] = Field(serialization_alias="ipv6Address", validation_alias="ipv6Address")
    ipv6_prefix_length: Global[int] = Field(serialization_alias="ipv6PrefixLength", validation_alias="ipv6PrefixLength")


class IPv6PrefixListParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.IPV6_PREFIX)
    entries: List[IPv6PrefixListEntry] = Field(validation_alias=AliasPath("data", "entries"))
