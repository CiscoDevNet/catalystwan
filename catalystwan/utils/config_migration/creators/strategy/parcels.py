from typing import Dict, List
from uuid import UUID

from catalystwan.models.configuration.config_migration import TransformedParcel
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfile


class ParcelPusher:
    """
    Base class for pushing parcels to a feature profile.
    """

    def __init__(self, api: FeatureProfile):
        self.api = api

    def push(self, profile_uuid: UUID, parcel_uuids: List[UUID], mapping: Dict[UUID, TransformedParcel]):
        """
        Push parcels to the given feature profile.

        Args:
            profile_uuid (UUID): The UUID of the feature profile.
            parcel_uuids (List[UUID]): The list of parcel UUIDs to push.
            mapping (Dict[UUID, TransformedParcel]): The mapping of parcel UUIDs to transformed parcels.
        """
        raise NotImplementedError


class SimpleParcelPusher(ParcelPusher):
    """
    Simple implementation of ParcelPusher that creates parcels directly.
    """

    def push(self, profile_uuid: UUID, parcel_uuids: List[UUID], mapping: Dict[UUID, TransformedParcel]):
        # Parcels don't have references to other parcels, so we can create them directly
        for parcel_uuid in parcel_uuids:
            transformed_parcel = mapping[parcel_uuid]
            self.api.create_parcel(profile_uuid, transformed_parcel.parcel)  # type: ignore
