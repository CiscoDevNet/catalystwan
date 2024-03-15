import logging
from typing import Callable, List, Literal, Tuple
from uuid import UUID, uuid4

from catalystwan.api.policy_api import POLICY_LIST_ENDPOINTS_MAP
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.models.configuration.config_migration import (
    TransformedConfigGroup,
    TransformedFeatureProfile,
    TransformedParcel,
    TransformHeader,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.converters.feature_template import create_parcel_from_template
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert as convert_policy_list
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
    # "bgp",
    # "cisco_bgp",
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
    # "bgp",
    # "cisco_bgp",
]

FEATURE_PROFILE_TRANSPORT = ["dhcp", "cisco_dhcp_server", "dhcp-server"]

FEATURE_PROFILE_OTHER = [
    "cisco_thousandeyes",
    "ucse",
]


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info(f"{task} {completed}/{total}")


def transform(ux1: UX1Config) -> UX2Config:
    ux2 = UX2Config()
    # Create Feature Profiles and Config Group
    for dt in ux1.templates.device_templates:
        templates = flatten_general_templates(dt.general_templates)

        # Create Feature Profiles
        fp_system_uuid = uuid4()
        transformed_fp_system = TransformedFeatureProfile(
            header=TransformHeader(
                type="system",
                origin=fp_system_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_system",
                description="system",
            ),
        )
        fp_transport_uuid = uuid4()
        transformed_fp_transport = TransformedFeatureProfile(
            header=TransformHeader(
                type="transport",
                origin=fp_transport_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_transport",
                description="transport",
            ),
        )
        fp_other_uuid = uuid4()
        transformed_fp_other = TransformedFeatureProfile(
            header=TransformHeader(
                type="other",
                origin=fp_other_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_other",
                description="other",
            ),
        )

        for template in templates:
            # Those feature templates IDs are real UUIDs and are used to map to the feature profiles
            if template.templateType in FEATURE_PROFILE_SYSTEM:
                transformed_fp_system.header.subelements.add(UUID(template.templateId))
            elif template.templateType in FEATURE_PROFILE_TRANSPORT:
                transformed_fp_transport.header.subelements.add(UUID(template.templateId))
            elif template.templateType in FEATURE_PROFILE_OTHER:
                transformed_fp_other.header.subelements.add(UUID(template.templateId))

        transformed_cg = TransformedConfigGroup(
            header=TransformHeader(
                type="config_group",
                origin=dt.id,
                subelements=set([fp_system_uuid, fp_transport_uuid, fp_other_uuid]),
            ),
            config_group=ConfigGroupCreationPayload(
                name=dt.template_name,
                description=dt.template_description,
                solution="sdwan",
                profiles=[],
            ),
        )
        # Add to UX2
        ux2.feature_profiles.append(transformed_fp_system)
        ux2.feature_profiles.append(transformed_fp_transport)
        ux2.feature_profiles.append(transformed_fp_other)
        ux2.config_groups.append(transformed_cg)

    for ft in ux1.templates.feature_templates:
        if ft.template_type in SUPPORTED_TEMPLATE_TYPES:
            parcel = create_parcel_from_template(ft)
            transformed_parcel = TransformedParcel(
                header=TransformHeader(
                    type=parcel._get_parcel_type(),
                    origin=UUID(ft.id),
                ),
                parcel=parcel,
            )
            # Add to UX2. We can indentify the parcels as subelements of the feature profiles by the UUIDs
            ux2.profile_parcels.append(transformed_parcel)

    # Policy Lists
    for policy_list in ux1.policies.policy_lists:
        policy_parcel = convert_policy_list(policy_list)
        if policy_parcel is not None:
            header = TransformHeader(type=policy_parcel._get_parcel_type(), origin=policy_list.list_id)
            ux2.profile_parcels.append(TransformedParcel(header=header, parcel=policy_parcel))
        else:
            logger.warning(f"{policy_list.type} {policy_list.list_id} {policy_list.name} was not converted")
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


def push_ux2_config(
    session: ManagerSession, config: UX2Config, progress: Callable[[str, int, int], None] = log_progress
):
    # Create mapping from origin ids
    # do dataclass
    mapping = {
        "config_group": {item.header.origin: item for item in config.config_groups},
        "feature_profile": {item.header.origin: item for item in config.feature_profiles},
        "profile_parcels": {item.header.origin: item for item in config.profile_parcels},
    }
    rollback_config_groups_ids: List[UUID] = []
    rollback_feature_profiles_ids: List[Tuple[UUID, Literal["system", "other", "transport"]]] = []

    try:
        for config_group in config.config_groups:
            config_group_profiles = []

            for feature_profile_id in config_group.header.subelements:
                feature_profile = mapping["feature_profile"][feature_profile_id]

                if feature_profile.header.type == "system":
                    # Feature Profile System Parcels don't have references to other parcels so we can create them directly
                    system_api = session.api.sdwan_feature_profiles.system

                    feature_profile_system = system_api.create_profile(
                        name=feature_profile.feature_profile.name,
                        description=feature_profile.feature_profile.description,
                    )
                    config_group_profiles.append(feature_profile_system)
                    rollback_feature_profiles_ids.append((feature_profile_system.id, "system"))

                    logger.info(
                        f"Creating Feature Profile {feature_profile_system.id} {feature_profile.feature_profile.name}"
                    )
                    logger.info(
                        f"Subelements Feature Profile {feature_profile_system.id} {feature_profile.header.subelements}"
                    )

                    for parcel_id in feature_profile.header.subelements:
                        logger.info(f"Creating Parcel {parcel_id} in Feature Profile {feature_profile_system.id}")

                        parcel = mapping["profile_parcels"][parcel_id]
                        system_api.create_parcel(feature_profile_system.id, parcel.parcel)

                elif feature_profile.header.type == "other":
                    # Feature Profile Other Parcels don't have references to other parcels so we can create them directly
                    other_api = session.api.sdwan_feature_profiles.other

                    feature_profile_other = other_api.create_profile(
                        name=feature_profile.feature_profile.name,
                        description=feature_profile.feature_profile.description,
                    )
                    config_group_profiles.append(feature_profile_other)
                    rollback_feature_profiles_ids.append((feature_profile_other.id, "other"))

                    for parcel_id in feature_profile.header.subelements:
                        parcel = mapping["profile_parcels"][parcel_id]
                        other_api.create_parcel(feature_profile_other.id, parcel.parcel)

                elif feature_profile.header.type == "transport":
                    # Feature Profile Transport Parcels have references to other parcels so we need to create them in order
                    pass

            # Create Config Group and add created Feature Profiles
            config_group_payload = config_group.config_group
            config_group_payload.profiles = config_group_profiles
            cg_id = session.endpoints.configuration_group.create_config_group(config_group_payload).id
            rollback_config_groups_ids.append(cg_id)

    except Exception as e:
        logger.error(f"Error pushing UX2 config: {e}")
        rollback_ux2_config(session, rollback_config_groups_ids, rollback_feature_profiles_ids)
        raise e

    return rollback_config_groups_ids, rollback_feature_profiles_ids


def rollback_ux2_config(
    session: ManagerSession,
    rollback_config_groups_ids: List[UUID],
    rollback_feature_profiles_ids: List[Tuple[UUID, Literal["system", "other", "transport"]]],
):
    for cg_id in rollback_config_groups_ids:
        session.endpoints.configuration_group.delete_config_group(cg_id)

    for feature_profile_id, type in rollback_feature_profiles_ids:
        if type == "system":
            session.api.sdwan_feature_profiles.system.delete_profile(feature_profile_id)
        elif type == "other":
            session.api.sdwan_feature_profiles.other.delete_profile(feature_profile_id)
        elif type == "transport":
            pass
        else:
            print(f"Unknown feature profile type {type}")
