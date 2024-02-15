from ipaddress import IPv4Network
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class SecurityDataPrefixEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ip_prefix: Global[IPv4Network] = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")


class SecurityDataPrefixParcel(_ParcelBase):
    entries: List[SecurityDataPrefixEntry] = Field(validation_alias=AliasPath("data", "entries"))
