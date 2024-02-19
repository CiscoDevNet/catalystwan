from ipaddress import IPv4Network
from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class SecurityDataPrefixEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    ip_prefix: Global[IPv4Network] = Field(serialization_alias="ipPrefix", validation_alias="ipPrefix")


class SecurityDataPrefixParcel(_ParcelBase):
    entries: List[SecurityDataPrefixEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_prefix(self, ip_prefix: IPv4Network):
        self.entries.append(SecurityDataPrefixEntry(ip_prefix=as_global(ip_prefix)))
