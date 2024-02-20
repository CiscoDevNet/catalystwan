from typing import List

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.template_api import DeviceTemplateInformation, FeatureTemplateInformation
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    CentralizedPolicy,
    LocalizedPolicy,
    SecurityPolicy,
)


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


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    config_groups: List[ConfigGroup] = Field(
        default=[], serialization_alias="configurationGroups", validation_alias="configurationGroups"
    )
    policy_groups: List[ConfigGroup] = Field(
        default=[], serialization_alias="policyGroups", validation_alias="policyGroups"
    )
    feature_profiles: List[FeatureProfileCreationPayload] = Field(
        default=[], serialization_alias="featureProfiles", validation_alias="featureProfiles"
    )
    profile_parcels: List[AnyPolicyObjectParcel] = Field(
        default=[], serialization_alias="profileParcels", validation_alias="profileParcels"
    )
