import logging
from datetime import datetime
from typing import List
from uuid import UUID

from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.models.configuration.config_migration import UX2Config
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.session import ManagerSession


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
