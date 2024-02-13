from typing import List, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType


class ApplicationListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list: Global[str] = Field(serialization_alias="app", validation_alias="app")


class ApplicationFamilyListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    app_list_family: Global[str] = Field(serialization_alias="appFamily", validation_alias="appFamily")


class ApplicationListParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.APP_LIST)
    entries: List[Union[ApplicationListEntry, ApplicationFamilyListEntry]] = Field(
        validation_alias=AliasPath("data", "entries")
    )
