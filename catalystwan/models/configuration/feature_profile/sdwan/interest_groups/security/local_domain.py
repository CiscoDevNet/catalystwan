from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class LocalDomainListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name_server: Global[str] = Field(
        serialization_alias="nameServer", validation_alias="nameServer", description="Ex: cisco.com, *.cisco.com"
    )


class LocalDomainParcel(_ParcelBase):
    entries: List[LocalDomainListEntry] = Field(validation_alias=AliasPath("data", "entries"))
