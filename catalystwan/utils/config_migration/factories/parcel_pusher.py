from typing import Callable, Mapping

from catalystwan.api.feature_profile_api import FeatureProfileAPI
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.utils.config_migration.creators.strategy.parcels import ParcelPusher, SimpleParcelPusher

PARCEL_PUSHER_MAPPING: Mapping[ProfileType, Callable] = {
    "other": SimpleParcelPusher,
    "system": SimpleParcelPusher,
}


class ParcelPusherFactory:
    """
    Factory class for creating ParcelPusher instances.
    """

    @staticmethod
    def get_pusher(profile_type: ProfileType, api: FeatureProfileAPI) -> ParcelPusher:
        """
        Get the appropriate ParcelPusher instance based on the profile type.

        Args:
            profile_type (ProfileType): The type of the feature profile.
            api (FeatureProfileAPI): The API for interacting with feature profiles.

        Returns:
            ParcelPusher: The appropriate ParcelPusher instance.
        """
        pusher_class = PARCEL_PUSHER_MAPPING.get(profile_type)
        if pusher_class is None:
            raise ValueError(f"Invalid profile type: {profile_type}")
        return pusher_class(api)
