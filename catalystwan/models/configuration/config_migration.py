# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Set, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.api.templates.device_template.device_template import DeviceTemplate
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyServiceParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import AnyTransportParcel
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo, AnyPolicyListInfo
from catalystwan.models.policy.centralized import CentralizedPolicyInfo
from catalystwan.models.policy.localized import LocalizedPolicyInfo
from catalystwan.models.policy.security import AnySecurityPolicyInfo

AnyParcel = Annotated[
    Union[AnySystemParcel, AnyPolicyObjectParcel, AnyServiceParcel, AnyOtherParcel, AnyTransportParcel],
    Field(discriminator="type_"),
]


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    centralized_policies: List[CentralizedPolicyInfo] = Field(
        default=[], serialization_alias="centralizedPolicies", validation_alias="centralizedPolicies"
    )
    localized_policies: List[LocalizedPolicyInfo] = Field(
        default=[], serialization_alias="localizedPolicies", validation_alias="localizedPolicies"
    )
    security_policies: List[AnySecurityPolicyInfo] = Field(
        default=[], serialization_alias="securityPolicies", validation_alias="securityPolicies"
    )
    policy_definitions: List[AnyPolicyDefinitionInfo] = Field(
        default=[], serialization_alias="policyDefinitions", validation_alias="policyDefinitions"
    )
    policy_lists: List[AnyPolicyListInfo] = Field(
        default=[], serialization_alias="policyLists", validation_alias="policyLists"
    )


class UX1Templates(BaseModel):
    feature_templates: List[FeatureTemplateInformation] = Field(
        default=[], serialization_alias="featureTemplates", validation_alias="featureTemplates"
    )
    device_templates: List[DeviceTemplate] = Field(
        default=[], serialization_alias="deviceTemplates", validation_alias="deviceTemplates"
    )


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()


class TransformHeader(BaseModel):
    type: str = Field(
        description="Needed to push item to specific endpoint."
        "Type discriminator is not present in many UX2 item payloads"
    )
    origin: UUID = Field(description="Original UUID of converted item")
    subelements: Set[UUID] = Field(default_factory=set)


class TransformedTopologyGroup(BaseModel):
    header: TransformHeader
    topology_group: TopologyGroup


class TransformedConfigGroup(BaseModel):
    header: TransformHeader
    config_group: ConfigGroupCreationPayload


class TransformedFeatureProfile(BaseModel):
    header: TransformHeader
    feature_profile: FeatureProfileCreationPayload


class TransformedParcel(BaseModel):
    header: TransformHeader
    parcel: AnyParcel


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    topology_groups: List[TransformedTopologyGroup] = Field(
        default=[], serialization_alias="topologyGroups", validation_alias="topologyGroups"
    )
    config_groups: List[TransformedConfigGroup] = Field(
        default=[], serialization_alias="configurationGroups", validation_alias="configurationGroups"
    )
    policy_groups: List[TransformedConfigGroup] = Field(
        default=[], serialization_alias="policyGroups", validation_alias="policyGroups"
    )
    feature_profiles: List[TransformedFeatureProfile] = Field(
        default=[], serialization_alias="featureProfiles", validation_alias="featureProfiles"
    )
    profile_parcels: List[TransformedParcel] = Field(
        default=[], serialization_alias="profileParcels", validation_alias="profileParcels"
    )


class UX2ConfigRollback(BaseModel):
    config_group_ids: List[UUID] = Field(
        default_factory=list, serialization_alias="ConfigGroupIds", validation_alias="ConfigGroupIds"
    )
    feature_profile_ids: List[Tuple[UUID, ProfileType]] = Field(
        default_factory=list, serialization_alias="FeatureProfileIds", validation_alias="FeatureProfileIds"
    )

    def add_config_group(self, config_group_id: UUID) -> None:
        self.config_group_ids.append(config_group_id)

    def add_feature_profile(self, feature_profile_id: UUID, profile_type: ProfileType) -> None:
        self.feature_profile_ids.append((feature_profile_id, profile_type))
