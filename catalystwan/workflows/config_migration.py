import logging
from typing import Callable

from catalystwan.api.policy_api import POLICY_LIST_ENDPOINTS_MAP
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    ConfigGroupCreator,
    UX1Config,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.converters.feature_template import create_parcel_from_template
from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)

SUPPORTED_TEMPLATE_TYPES = ["cedge_aaa", "cedge_aaa"]


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info(f"{task} {completed}/{total}")


def transform(ux1: UX1Config) -> UX2Config:
    ux2 = UX2Config()
    for ft in ux1.templates.features:
        if ft.template_type in SUPPORTED_TEMPLATE_TYPES:
            ux2.profile_parcels.append(create_parcel_from_template(ft))
    # Policy Lists
    for policy_list in ux1.policies.policy_lists:
        if (parcel := policy_list.to_policy_object_parcel()) is not None:
            ux2.profile_parcels.append(parcel)
    return ux2


def collect_ux1_config(session: ManagerSession, progress: Callable[[str, int, int], None] = log_progress) -> UX1Config:
    ux1 = UX1Config()

    """Collect Policies"""
    policy_api = session.api.policy
    progress("Collecting Policy Info", 0, 3)

    centralized_policy_ids = [info.policy_id for info in policy_api.centralized.get()]
    progress("Collecting Policy Info", 1, 3)

    localized_policy_ids = [info.policy_id for info in policy_api.localized.get()]
    progress("Collecting Policy Info", 2, 3)

    policy_definition_types_and_ids = [
        (policy_type, info.definition_id) for policy_type, info in policy_api.definitions.get_all()
    ]
    progress("Collecting Policy Info", 3, 3)

    policy_list_types = POLICY_LIST_ENDPOINTS_MAP.keys()
    for i, policy_list_type in enumerate(policy_list_types):
        ux1.policies.policy_lists.extend(policy_api.lists.get(policy_list_type))
        progress("Collecting Policy Lists", i + 1, len(policy_list_types))

    for i, type_and_id in enumerate(policy_definition_types_and_ids):
        ux1.policies.policy_definitions.append(policy_api.definitions.get(*type_and_id))
        progress("Collecting Policy Definitions", i + 1, len(policy_definition_types_and_ids))

    for i, cpid in enumerate(centralized_policy_ids):
        ux1.policies.centralized_policies.append(policy_api.centralized.get(id=cpid))
        progress("Collecting Centralized Policies", i + 1, len(centralized_policy_ids))

    for i, lpid in enumerate(localized_policy_ids):
        ux1.policies.localized_policies.append(policy_api.localized.get(id=lpid))
        progress("Collecting Localized Policies", i + 1, len(localized_policy_ids))

    """Collect Templates"""
    template_api = session.api.templates
    progress("Collecting Templates Info", 0, 2)

    ux1.templates.features = [t for t in template_api.get_feature_templates()]
    progress("Collecting Templates Info", 1, 2)

    ux1.templates.devices = [t for t in template_api.get_device_templates()]
    progress("Collecting Templates Info", 2, 2)

    return ux1


def push_ux2_config(session: ManagerSession, config: UX2Config, logger: logging.Logger = logger) -> UX2ConfigPushResult:
    """
    Creates configuration group and pushes a UX2 configuration to the Cisco vManage.

    Args:
        session (ManagerSession): A valid Manager API session.
        config (UX2Config): The UX2 configuration to push.

    Returns:
        UX2ConfigPushResult

    Raises:
        ManagerHTTPError: If the configuration cannot be pushed.
    """

    try:
        config_group_creator = ConfigGroupCreator(session, config, logger)
        config_group = config_group_creator.create()
        feature_profiles = config_group.profiles  # noqa: F841
        for parcels in config.profile_parcels:
            # TODO: Create API that supports parcel creation on feature profiles
            # Example: session.api.parcels.create(parcels=parcels, feature_profiles=feature_profiles)
            pass

    except ManagerHTTPError as e:
        return UX2ConfigPushResult(status="failure", exception=e)

    return UX2ConfigPushResult(status="success", config_group=config_group)
