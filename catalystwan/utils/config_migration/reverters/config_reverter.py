from typing import Callable
from venv import logger

from catalystwan.exceptions import CatalystwanException
from catalystwan.utils.config_migration.creators.config_pusher import UX2ConfigRollback
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfileAPIFactory


class UX2ConfigReverter:
    def __init__(self, session) -> None:
        self._session = session

    def rollback(self, rollback_config: UX2ConfigRollback, progress: Callable[[str, int, int], None]) -> bool:
        try:
            for i, cg_id in enumerate(rollback_config.config_group_ids):
                self._session.endpoints.configuration_group.delete_config_group(cg_id)
                progress("Removing Configuration Groups", i + 1, len(rollback_config.config_group_ids))
            for i, feature_profile_entry in enumerate(rollback_config.feature_profile_ids):
                feature_profile_id, type_ = feature_profile_entry
                api = FeatureProfileAPIFactory.get_api(type_, self._session)
                if type_ == "policy-object":
                    continue
                api.delete_profile(feature_profile_id)  # type: ignore
                progress("Removing Feature Profiles", i + 1, len(rollback_config.feature_profile_ids))
        except CatalystwanException as e:
            logger.error(f"Error occured during config revert: {e}")
            return False
        return True
