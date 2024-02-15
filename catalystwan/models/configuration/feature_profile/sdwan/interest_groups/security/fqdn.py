from typing import List

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class FQDNListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    pattern: Global[str] = Field(
        description="Ex: cisco.com, .*cisco.com, .*.cisco.com. Should not start with '*' or '+'"
    )


class FQDNDomainParcel(_ParcelBase):
    entries: List[FQDNListEntry] = Field(validation_alias=AliasPath("data", "entries"))
