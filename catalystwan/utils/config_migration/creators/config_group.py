from dataclasses import dataclass
from typing import Dict, List
from uuid import UUID

from catalystwan.models.configuration.config_migration import (
    TransformedConfigGroup,
    TransformedFeatureProfile,
    TransformedParcel,
)
from catalystwan.models.configuration.profile_type import ProfileType


@dataclass
class UX2ConfigMap:
    config_group_map: Dict[UUID, TransformedConfigGroup]
    feature_profile_map: Dict[UUID, TransformedFeatureProfile]
    parcel_map: Dict[UUID, TransformedParcel]


@dataclass
class UX2ConfigRollback:
    config_groups_ids: List[UUID]
    feature_profiles_ids: List[UUID, ProfileType]
