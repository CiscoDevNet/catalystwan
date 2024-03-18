from venv import logger

from catalystwan.exceptions import CatalystwanException
from catalystwan.utils.config_migration.creators.config_pusher import UX2ConfigRollback
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfileAPIFactory


class UX2ConfigReverter:
    def __init__(self, session) -> None:
        self._session = session

    def rollback(self, rollback_config: UX2ConfigRollback) -> bool:
        try:
            for cg_id in rollback_config.config_groups_ids:
                self._session.endpoints.configuration_group.delete_config_group(cg_id)
            for feature_profile_id, type_ in rollback_config.feature_profiles_ids:
                api = FeatureProfileAPIFactory.get_api(type_, self._session)
                if type_ == "policy-object":
                    continue
                api.delete_profile(feature_profile_id)  # type: ignore
        except CatalystwanException as e:
            logger.error(f"Error occured during config revert: {e}")
            return False
        return True
