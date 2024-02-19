from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class FQDNListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str] = Field(
        description="Ex: cisco.com, .*cisco.com, .*.cisco.com. Should not start with '*' or '+'"
    )


class FQDNDomainParcel(_ParcelBase):
    entries: List[FQDNListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def from_fqdns(self, fqdns: List[str]):
        for fqdn in fqdns:
            self.entries.append(FQDNListEntry(pattern=as_global(fqdn)))
