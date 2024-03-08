# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class ApplicationListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list: Global[str] = Field(serialization_alias="app", validation_alias="app")


class ApplicationFamilyListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list_family: Global[str] = Field(serialization_alias="appFamily", validation_alias="appFamily")


class ApplicationListParcel(_ParcelBase):
    type_: Literal["app-list"] = Field(default="app-list", exclude=True)
    entries: List[Union[ApplicationListEntry, ApplicationFamilyListEntry]] = Field(
        default=[], validation_alias=AliasPath("data", "entries")
    )

    def add_application(self, application: str):
        self.entries.append(ApplicationListEntry(app_list=as_global(application)))

    def add_application_family(self, application_family: str):
        self.entries.append(ApplicationFamilyListEntry(app_list_family=as_global(application_family)))
