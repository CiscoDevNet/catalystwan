# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class SecurityApplicationListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list: Global[str] = Field(serialization_alias="app", validation_alias="app")


class SecurityApplicationFamilyListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list_family: Global[str] = Field(serialization_alias="appFamily", validation_alias="appFamily")


class SecurityApplicationListParcel(_ParcelBase):
    type_: Literal["security-localapp"] = Field(default="security-localapp", exclude=True)
    entries: List[Union[SecurityApplicationFamilyListEntry, SecurityApplicationListEntry]] = Field(
        default=[], validation_alias=AliasPath("data", "entries")
    )

    def add_application(self, application: str):
        self.entries.append(SecurityApplicationListEntry(app_list=as_global(application)))

    def add_application_family(self, application_family: str):
        self.entries.append(SecurityApplicationFamilyListEntry(app_list_family=as_global(application_family)))
