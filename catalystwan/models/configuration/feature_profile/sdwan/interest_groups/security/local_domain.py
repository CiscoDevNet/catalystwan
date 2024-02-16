from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class LocalDomainListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name_server: Global[str] = Field(
        serialization_alias="nameServer", validation_alias="nameServer", description="Ex: cisco.com, *.cisco.com"
    )


class LocalDomainParcel(_ParcelBase):
    entries: List[LocalDomainListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_local_domain(self, domain: str):
        self.entries.append(LocalDomainListEntry(name_server=as_global(domain)))
