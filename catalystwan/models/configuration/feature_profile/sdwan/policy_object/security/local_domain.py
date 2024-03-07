# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class LocalDomainListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name_server: Global[str] = Field(
        serialization_alias="nameServer", validation_alias="nameServer", description="Ex: cisco.com, *.cisco.com"
    )


class LocalDomainParcel(_ParcelBase):
    type_: Literal["security-localdomain"] = Field(default="security-localdomain", exclude=True)
    entries: List[LocalDomainListEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def from_local_domains(self, domains: List[str]):
        for domain in domains:
            self.entries.append(LocalDomainListEntry(name_server=as_global(domain)))
