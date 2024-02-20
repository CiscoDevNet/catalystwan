import logging
from typing import Callable

from catalystwan.models.configuration.config_migration import UX1Config, UX2Config
from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info("{task} {completed}/{total}")


def transform(ux1: UX1Config) -> UX2Config:
    ux2 = UX2Config()
    ux2.profile_parcels.extend([lst.to_policy_object_parcel() for lst in ux1.policies.policy_lists])
    return ux2


def collect_ux1_config(
    session: ManagerSession, progress_callback: Callable[[str, int, int], None] = log_progress
) -> UX1Config:
    ux1 = UX1Config()
    # Policies part
    policy_api = session.api.policy
    progress_callback("Collecting Policy Info", 3, 0)
    # centralized_policy_ids = [info.policy_id for info in policy_api.centralized.get()]
    for uid in [info.policy_id for info in policy_api.centralized.get()]:
        ux1.policies.centralized_policies.append(policy_api.centralized.get(id=uid))
    for uid in [info.policy_id for info in policy_api.localized.get()]:
        ux1.policies.localized_policies.append(policy_api.localized.get(id=uid))
    # Templates part
    # TODO
    return ux1


def push_ux2_config(session: ManagerSession) -> None:
    pass
