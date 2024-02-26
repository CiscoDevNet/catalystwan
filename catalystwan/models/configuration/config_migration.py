from typing import List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.api.template_api import DeviceTemplateInformation, FeatureTemplateInformation
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    CentralizedPolicy,
    LocalizedPolicy,
    SecurityPolicy,
)

AnyParcel = Annotated[
    Union[
        AnySystemParcel,
        AnyPolicyObjectParcel,
    ],
    Field(discriminator="type_"),
]


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    centralized_policies: List[CentralizedPolicy] = Field(
        default=[], serialization_alias="centralizedPolicies", validation_alias="centralizedPolicies"
    )
    localized_policies: List[LocalizedPolicy] = Field(
        default=[], serialization_alias="localizedPolicies", validation_alias="localizedPolicies"
    )
    security_policies: List[SecurityPolicy] = Field(
        default=[], serialization_alias="securityPolicies", validation_alias="securityPolicies"
    )
    policy_definitions: List[AnyPolicyDefinition] = Field(
        default=[], serialization_alias="policyDefinitions", validation_alias="policyDefinitions"
    )
    policy_lists: List[AnyPolicyList] = Field(
        default=[], serialization_alias="policyLists", validation_alias="policyLists"
    )


class UX1Templates(BaseModel):
    features: List[FeatureTemplateInformation] = Field(default=[])
    devices: List[DeviceTemplateInformation] = Field(default=[])


class ConfigGroupPreset(BaseModel):
    config_group_name: str = Field(serialization_alias="name", validation_alias="name")
    solution: Literal["sdwan"] = "sdwan"
    profile_parcels: List[AnyParcel] = Field(
        default=[], serialization_alias="profileParcels", validation_alias="profileParcels"
    )


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    # TODO: config group name
    config_group_presets: List[ConfigGroupPreset] = Field(
        default=[], serialization_alias="configGroupPresets", validation_alias="configGroupPresets"
    )
