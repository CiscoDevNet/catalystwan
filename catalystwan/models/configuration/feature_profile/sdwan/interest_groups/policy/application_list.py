from typing import List, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase


class ApplicationListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list: Global[str] = Field(serialization_alias="app", validation_alias="app")


class ApplicationFamilyListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list_family: Global[str] = Field(serialization_alias="appFamily", validation_alias="appFamily")


class ApplicationListParcel(_ParcelBase):
    entries: List[Union[ApplicationListEntry, ApplicationFamilyListEntry]] = Field(
        validation_alias=AliasPath("data", "entries")
    )
