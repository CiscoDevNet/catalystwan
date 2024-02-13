from typing import List, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import TLOCColorEnum
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.object_list_type import PolicyObjectListType
from catalystwan.models.policy.lists_entries import PathPreferenceEnum


class Preference(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    color_preference: Global[List[TLOCColorEnum]] = Field(
        serialization_alias="colorPreference", validation_alias="colorPreference"
    )
    path_preference: Global[PathPreferenceEnum] = Field(
        serialization_alias="pathPreference", validation_alias="pathPreference"
    )


class PreferredColorGroupEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    primary_preference: Preference = Field(
        serialization_alias="primaryPreference", validation_alias="primaryPreference"
    )
    secondary_preference: Union[Preference, None] = Field(
        None, serialization_alias="secondaryPreference", validation_alias="secondaryPreference"
    )
    tertiary_preference: Union[Preference, None] = Field(
        None, serialization_alias="tertiaryPreference", validation_alias="tertiaryPreference"
    )

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PreferredColorGroupEntry":
        if not self.secondary_preference and self.tertiary_preference:
            raise ValueError("Preference Entry has to have a secondary prefrence when assigning tertiary preference.")
        return self


class PreferredColorGroupParcel(_ParcelBase):
    _payload_endpoint: PolicyObjectListType = PrivateAttr(default=PolicyObjectListType.PREFERRED_COLOR_GROUP)
    entries: List[PreferredColorGroupEntry] = Field(validation_alias=AliasPath("data", "entries"))
