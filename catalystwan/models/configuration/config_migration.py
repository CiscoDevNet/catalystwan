import logging
from datetime import datetime
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.api.template_api import DeviceTemplateInformation, FeatureTemplateInformation
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.policy import (
    AnyPolicyDefinition,
    AnyPolicyList,
    CentralizedPolicy,
    LocalizedPolicy,
    SecurityPolicy,
)
from catalystwan.session import ManagerSession

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
    profile_parcels: List[AnyParcel] = Field(
        default=[], serialization_alias="profileParcels", validation_alias="profileParcels"
    )


class UX2ConfigPushResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: Literal["success", "failure"]
    config_group: Optional[ConfigGroup] = None
    exception: Optional[ManagerHTTPError] = None


class ConfigGroupCreator:
    """
    Creates a configuration group and attach feature profiles for migrating UX1 templates to UX2.
    """

    def __init__(self, session: ManagerSession, config: UX2Config, logger: logging.Logger):
        """
        Args:
            session (ManagerSession): A valid Manager API session.
            config (UX2Config): The UX2 configuration to migrate.
            logger (logging.Logger): A logger for logging messages.
        """
        self.session = session
        self.config = config
        self.logger = logger
        self.profile_ids: List[UUID] = []

    def create(self) -> ConfigGroup:
        """
        Creates a configuration group and attach feature profiles for migrating UX1 templates to UX2.

        Returns:
            ConfigGroup: The created configuration group.
        """
        self.created_at = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self._create_sdwan_system_feature_profile()
        self._create_sdwan_policy_objects_feature_profile()
        config_group_id = self._create_configuration_group()
        return self.session.api.config_group.get(config_group_id)  # type: ignore[return-value]

    def _create_sdwan_system_feature_profile(self):
        """
        Creates a SDWAN System Feature Profile for migrating UX1 Templates to UX2.

        Args:
            session (ManagerSession): A valid Manager API session.
            name (str): The name of the SDWAN System Feature Profile.

        Returns:
            UUID: The ID of the created SDWAN System Feature Profile.

        Raises:
            ManagerHTTPError: If the SDWAN System Feature Profile cannot be created.
        """
        system_name = f"MIGRATION_SDWAN_SYSTEM_FEATURE_PROFILE_{self.created_at}"
        profile_system = FeatureProfileCreationPayload(
            name=system_name, description="Profile for migrating UX1 Templates to UX2"
        )
        system_id = self.session.endpoints.configuration_feature_profile.create_sdwan_system_feature_profile(
            profile_system
        ).id
        self.logger.info(f"Created SDWAN System Feature Profile {system_name} with ID: {system_id}")
        self.profile_ids.append(system_id)

    def _create_sdwan_policy_objects_feature_profile(self):
        """
        Creates a SDWAN Policy Objects Feature Profile for migrating UX1 Policies to UX2.

        Args:
            session (ManagerSession): A valid Manager API session.
            name (str): The name of the SDWAN Policy Objects Feature Profile.

        Returns:
            UUID: The ID of the created SDWAN Policy Objects Feature Profile.

        Raises:
            ManagerHTTPError: If the SDWAN Policy Objects Feature Profile cannot be created.
        """
        policy_objects_name = f"MIGRATION_SDWAN_POLICY_OBJECTS_FEATURE_PROFILE_{self.created_at}"
        # TODO: Find a way to create a policy object profile
        # for now there is no API or UI for creating a policy object profile
        profile_policy_objects = FeatureProfileCreationPayload(  # noqa: F841
            name=policy_objects_name, description="Profile for migrating UX1 Policies to UX2"
        )

        # Using default profile name for SDWAN Policy Objects Feature Profile
        policy_object_id = (
            ConfigurationFeatureProfile(self.session)
            .get_sdwan_feature_profiles()
            .filter(profile_name="Default_Policy_Object_Profile")
            .single_or_default()
        ).profile_id
        self.logger.info(
            f"Created SDWAN Policy Object Feature Profile {policy_objects_name} with ID: {policy_object_id}"
        )
        self.profile_ids.append(policy_object_id)

    def _create_configuration_group(self):
        """
        Creates a configuration group and attach feature profiles for migrating UX1 templates to UX2.

        Args:
            session (ManagerSession): A valid Manager API session.
            name (str): The name of the configuration group.
            profile_ids (List[UUID]): The IDs of the feature profiles to include in the configuration group.

        Returns:
            UUID: The ID of the created configuration group.

        Raises:
            ManagerHTTPError: If the configuration cannot be pushed.
        """
        config_group_name = f"SDWAN_CONFIG_GROUP_{self.created_at}"
        config_group_id = self.session.api.config_group.create(
            name=config_group_name,
            description="SDWAN Config Group created for migrating UX1 Templates to UX2",
            solution="sdwan",
            profile_ids=self.profile_ids,
        ).id
        self.logger.info(f"Created SDWAN Configuration Group {config_group_name} with ID: {config_group_id}")
        return config_group_id
