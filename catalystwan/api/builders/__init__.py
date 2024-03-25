from __future__ import annotations

from typing import TYPE_CHECKING

from .feature_profiles.feature_profile_builder_factory import FeatureProfileBuilderFactory

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class BuilderAPI:
    def __init__(self, session: ManagerSession):
        self.feature_profiles = FeatureProfileBuilderFactory(session=session)
