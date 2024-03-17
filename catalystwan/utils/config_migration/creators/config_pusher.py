from dataclasses import dataclass
from typing import Dict, List, Tuple, cast
from uuid import UUID
from venv import logger

from catalystwan.endpoints.configuration_group import ProfileId
from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.config_migration import TransformedFeatureProfile, TransformedParcel, UX2Config
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfileAPIFactory
from catalystwan.utils.config_migration.factories.parcel_pusher import ParcelPusherFactory


@dataclass
class ConfigurationMapping:
    feature_profile_map: Dict[UUID, TransformedFeatureProfile]
    parcel_map: Dict[UUID, TransformedParcel]


class UX2ConfigRollback:
    def __init__(self) -> None:
        self.config_groups_ids: List[UUID] = []
        self.feature_profiles_ids: List[Tuple[UUID, ProfileType]] = []

    def add_config_group(self, config_group_id: UUID) -> None:
        self.config_groups_ids.append(config_group_id)

    def add_feature_profile(self, feature_profile_id: UUID, profile_type: ProfileType) -> None:
        self.feature_profiles_ids.append((feature_profile_id, profile_type))


class UX2ConfigPusher:
    def __init__(self, session: ManagerSession, ux2_config: UX2Config) -> None:
        self._session = session
        self._config_map = self._create_config_map(ux2_config)
        self._config_rollback = UX2ConfigRollback()
        self._ux2_config = ux2_config

    def _create_config_map(self, ux2_config: UX2Config) -> ConfigurationMapping:
        return ConfigurationMapping(
            feature_profile_map={item.header.origin: item for item in ux2_config.feature_profiles},
            parcel_map={item.header.origin: item for item in ux2_config.profile_parcels},
        )

    def push(self) -> UX2ConfigRollback:
        try:
            self._create_config_groups()
        except CatalystwanException as e:
            logger.error(f"Error occured during config push: {e}")
        return self._config_rollback

    def _create_config_groups(self):
        for transformed_config_group in self._ux2_config.config_groups:
            config_group_payload = transformed_config_group.config_group
            config_group_payload.profiles = self._create_feature_profile_and_parcels(
                transformed_config_group.header.subelements
            )
            cg_id = self._session.endpoints.configuration_group.create_config_group(config_group_payload).id
            self._config_rollback.add_config_group(cg_id)

    def _create_feature_profile_and_parcels(self, feature_profiles_ids: List[UUID]) -> List[ProfileId]:
        config_group_profiles = []
        for feature_profile_id in feature_profiles_ids:
            transformed_feature_profile = self._config_map.feature_profile_map[feature_profile_id]
            profile_type = cast(ProfileType, transformed_feature_profile.header.type)
            api = FeatureProfileAPIFactory.get_api(profile_type, self._session)
            name = transformed_feature_profile.feature_profile.name
            description = transformed_feature_profile.feature_profile.description
            if profile_type == "policy-object":
                # TODO: Get default policy profile
                continue
            created_profile_id = api.create_profile(name, description).id  # type: ignore
            config_group_profiles.append(ProfileId(id=created_profile_id))
            self._create_parcels(api, created_profile_id, profile_type, transformed_feature_profile.header.subelements)
            self._config_rollback.add_feature_profile(created_profile_id, profile_type)
        return config_group_profiles

    def _create_parcels(self, api, profile_uuid, profile_type, parcels_uuids):
        pusher = ParcelPusherFactory.get_pusher(profile_type, api)
        pusher.push(profile_uuid, parcels_uuids, self._config_map.parcel_map)
