import logging
from typing import Any, Callable, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from catalystwan.api.policy_api import POLICY_LIST_ENDPOINTS_MAP
from catalystwan.endpoints.configuration_group import ConfigGroup, ConfigGroupCreationPayload
from catalystwan.models.configuration.config_migration import UX1Config, UX2Config
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.converters.feature_template import create_parcel_from_template
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert_all as convert_policy_lists
from catalystwan.utils.config_migration.creators.config_group import ConfigGroupCreator
from catalystwan.utils.config_migration.device_templates import flatten_general_templates

logger = logging.getLogger(__name__)

SUPPORTED_TEMPLATE_TYPES = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    "cisco_bfd",
    "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    "bgp",
    "cisco_bgp",
    "cisco_thousandeyes",
    "ucse",
    "dhcp",
    "cisco_dhcp_server",
]

FEATURE_PROFILE_SYSTEM = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    "cisco_bfd",
    "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    "bgp",
    "cisco_bgp",
]

FEATURE_PROFILE_TRANSPORT = [
    "dhcp",
    "cisco_dhcp_server",
]

FEATURE_PROFILE_OTHER = [
    "cisco_thousandeyes",
    "ucse",
]


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info(f"{task} {completed}/{total}")


class IdModel(BaseModel):
    type: str
    childs: Optional[List[UUID]] = None
    id: UUID
    model: Any


def transform2(ux1: UX1Config) -> Any:
    ux2 = UX2Config()
    # Create Feature Profiles and Config Group
    for dt in ux1.templates.device_templates:
        templates = flatten_general_templates(dt.general_templates)

        # Create Feature Profiles
        fp_system_uuid = uuid4()
        fp_system = IdModel(
            type="feature_profile_system",
            id=fp_system_uuid,
            model=FeatureProfileCreationPayload(
                name="system",
                description="system",
            ),
        )
        fp_transport_uuid = uuid4()
        fp_transport = IdModel(
            type="feature_profile_transport",
            id=fp_transport_uuid,
            model=FeatureProfileCreationPayload(
                name="transport",
                description="transport",
            ),
        )

        fp_other_uuid = uuid4()
        fp_other = IdModel(
            type="feature_profile_other",
            id=fp_other_uuid,
            model=FeatureProfileCreationPayload(
                name="other",
                description="other",
            ),
        )

        for template in templates:
            # Those feature templates IDs are real UUIDs and are used to map to the feature profiles
            if template.templateType in FEATURE_PROFILE_SYSTEM:
                fp_system.childs.append(template.templateId)
            elif template.templateType in FEATURE_PROFILE_TRANSPORT:
                fp_transport.childs.append(template.templateId)
            elif template.templateType in FEATURE_PROFILE_OTHER:
                fp_other.childs.append(template.templateId)

        cg = IdModel(
            type="config_group",
            id=uuid4(),
            childs=[fp_system_uuid, fp_transport_uuid, fp_other_uuid],
            model=ConfigGroupCreationPayload(
                name=dt.template_name,
                description=dt.template_description,
                solution="sdwan",
                profiles=[],
            ),
        )
        # Add to UX2
        ux2.feature_profiles.append(fp_system)
        ux2.feature_profiles.append(fp_transport)
        ux2.feature_profiles.append(fp_other)
        ux2.config_groups.append(cg)

    for ft in ux1.templates.feature_templates:
        if ft.template_type in SUPPORTED_TEMPLATE_TYPES:
            model = create_parcel_from_template(ft)
            # Using real UUIDs for the parcels. So creation overhead is reducted and they aleary mapp to the feature profiles
            ux2.profile_parcels.append(IdModel(type=model._get_parcel_type(), id=ft.id, model=model))


def transform(ux1: UX1Config) -> UX2Config:
    ux2 = UX2Config()
    # Feature Templates
    for ft in ux1.templates.feature_templates:
        if ft.template_type in SUPPORTED_TEMPLATE_TYPES:
            model = create_parcel_from_template(ft)
            ux2.profile_parcels.append(IdModel(type=model._get_parcel_type(), id=ft.id, model=model))
    # Policy Lists
    ux2.profile_parcels.extend(convert_policy_lists(ux1.policies.policy_lists).output)
    return ux2


def collect_ux1_config(session: ManagerSession, progress: Callable[[str, int, int], None] = log_progress) -> UX1Config:
    ux1 = UX1Config()

    """Collect Policies"""
    policy_api = session.api.policy

    progress("Collecting Policy Info", 0, 1)
    policy_definition_types_and_ids = [
        (policy_type, info.definition_id) for policy_type, info in policy_api.definitions.get_all()
    ]
    progress("Collecting Policy Info", 1, 1)

    policy_list_types = POLICY_LIST_ENDPOINTS_MAP.keys()
    for i, policy_list_type in enumerate(policy_list_types):
        ux1.policies.policy_lists.extend(policy_api.lists.get(policy_list_type))
        progress("Collecting Policy Lists", i + 1, len(policy_list_types))

    for i, type_and_id in enumerate(policy_definition_types_and_ids):
        ux1.policies.policy_definitions.append(policy_api.definitions.get(*type_and_id))
        progress("Collecting Policy Definitions", i + 1, len(policy_definition_types_and_ids))

    progress("Collecting Centralized Policies", 0, 1)
    ux1.policies.centralized_policies = [item for item in policy_api.centralized.get()]
    progress("Collecting Centralized Policies", 1, 1)

    progress("Collecting Localized Policies", 0, 1)
    ux1.policies.localized_policies = [item for item in policy_api.localized.get()]
    progress("Collecting Localized Policies", 1, 1)

    progress("Collecting Security Policies", 0, 1)
    ux1.policies.security_policies = [item for item in policy_api.security.get()]
    progress("Collecting Security Policies", 1, 1)

    """Collect Templates"""
    template_api = session.api.templates
    progress("Collecting Templates Info", 0, 2)

    ux1.templates.feature_templates = [t for t in template_api.get_feature_templates()]
    progress("Collecting Feature Templates", 1, 2)

    device_templates_ids = [t.id for t in template_api.get_device_templates()]
    for i, dtid in enumerate(device_templates_ids):
        ux1.templates.device_templates.append(template_api.get_device_template(dtid))
        progress("Collecting Device Templates", i + 1, len(device_templates_ids))

    return ux1


def push_ux2_config(session: ManagerSession, config: UX2Config) -> ConfigGroup:
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

    config_group_creator = ConfigGroupCreator(session, config, logger)
    config_group = config_group_creator.create()
    feature_profiles = config_group.profiles  # noqa: F841
    for parcels in config.profile_parcels:
        # TODO: Create API that supports parcel creation on feature profiles
        # Example: session.api.parcels.create(parcels=parcels, feature_profiles=feature_profiles)
        pass

    return config_group
