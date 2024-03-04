# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from packaging.version import Version  # type: ignore

from catalystwan.api.tenant_migration_api import TenantMigrationAPI
from catalystwan.endpoints.troubleshooting_tools.device_connectivity import NPingRequest
from catalystwan.exceptions import TenantMigrationPreconditionsError
from catalystwan.models.tenant import TenantExport
from catalystwan.session import ManagerSession, create_manager_session
from catalystwan.utils.personality import Personality
from catalystwan.utils.session_type import SessionType

logger = logging.getLogger(__name__)


def raise_or_log_precondition_check(msg: str, raises: bool) -> None:
    if raises:
        raise TenantMigrationPreconditionsError(msg)
    logger.warning(msg)


def check_control_connectivity_from_edge_devices(session: ManagerSession, host: str, attempts: int = 2) -> bool:
    """Checks that all edge devices can reach specified host using ping on transport VPN 0 which carries control traffic

    Args:
        session (ManagerSession): Session logged as device owner user
        host (str): IP address or domain name to ping to
        attempts (int, optional): Number of attempts. Defaults to 2.

    Returns:
        bool: True only if all devices can reach specified host
    """
    conn_status_by_device_id: Dict[str, bool] = {}
    edge_devices = session.api.devices.get_reachable_devices(personality=Personality.EDGE)
    if not edge_devices:
        logger.warning("No edge devices found to perform connectivity check!")
        return False
    for edge in edge_devices:
        logger.info(f"Checking {edge.id} can reach {host}...")
        conn_status_by_device_id[edge.id] = False
        for _ in range(attempts):
            ping_request = NPingRequest(host=host, vpn="0")
            ping_result = session.endpoints.troubleshooting_tools.device_connectivity.nping_device(
                edge.id, ping_request
            )
            if ping_result.loss_percentage < 50.0:
                conn_status_by_device_id[edge.id] = True
                break
    logger.info(f"Connectivity status to host: {host} by device:\n{conn_status_by_device_id}")
    return all(conn_status_by_device_id.values())


def migration_preconditions_check(
    origin_session: ManagerSession,
    target_session: ManagerSession,
    tenant: TenantExport,
    validator: str,
    raises: bool,
) -> bool:
    """Perform precondition checks prior tenant migration

    Args:
        origin_session (ManagerSession): session to migration origin
        target_session (ManagerSession): session to migration target
        tenant (MigrationTenant): Tenant object containig required fields: desc, name, subdomain, org_name
        validator (str): Target Validator (VBOND) IP address or domain name
        raises (bool): When true precondition check will raise, when false only warning will be logged

    Returns:
        bool: true only when all preconditions pass
    """
    problems: List[str] = []
    # Check if both platforms uses same build version
    logger.info("Checking if both platform versions match...")
    if target_session._platform_version != origin_session._platform_version:
        problems.append(
            f"Migration source and target expect to have same platform version but found "
            f"origin: {origin_session._platform_version} "
            f"target: {target_session._platform_version}",
        )
    # Export Params check
    logger.info("Performing export parameters checks...")
    if origin_session.api_version >= Version("20.13"):
        if tenant.is_destination_overlay_mt is None or tenant.migration_key is None:
            problems.append("'isDestinationOverlayMT' and 'migrationKey' must be provided using >= 20.13")
    # Target checks
    logger.info("Performing target checks...")
    target_org = target_session.endpoints.configuration_settings.get_organizations().first().org
    # Checks for MT target
    if target_session.session_type == SessionType.PROVIDER:
        if origin_session.api_version >= Version("20.13"):
            if not tenant.is_destination_overlay_mt:
                problems.append("Migrating to MT using >= 20.13 but 'isDestinationOverlayMT' is not set")
        if origin_session.session_type != SessionType.SINGLE_TENANT:
            problems.append(
                "Migration to MT (using provider) is expected to be initiated from ST (using single tenant)"
            )
        if not tenant.org_name.startswith(target_org):
            problems.append(f"Provided '{tenant.org_name}' but target organization is '{target_org}'")

    # Checks for ST target
    elif target_session.session_type == SessionType.SINGLE_TENANT:
        if target_session.api_version < Version("20.13"):
            problems.append("Migration to ST not supported prior 20.13")
        if tenant.is_destination_overlay_mt is True:
            problems.append("Migrating to ST but 'isDestinationOverlayMT' is set to True")
        if origin_session.session_type != SessionType.PROVIDER:
            problems.append(
                "Migration to ST (using single tenant) is expected to be initiated from MT (using provider)"
            )
        if tenant.org_name != target_org:
            problems.append(f"Provided '{tenant.org_name}' but target organization is '{target_org}'")
    else:
        problems.append(
            f"Migration target is expected to be executed as single tenant or provider "
            f"but found: {target_session.session_type}"
        )

    # Check if migrated devices can access target VBOND/Validator
    logger.info("Checking if migrated devices can reach target validator...")
    conn_check = False
    if origin_session.session_type == SessionType.PROVIDER:
        with create_manager_session(
            url=origin_session.url,
            username=origin_session.username,
            password=origin_session.password,
            port=origin_session.port,
            subdomain=tenant.subdomain,
            logger=origin_session.logger,
        ) as provider_as_tenant_session:
            conn_check = check_control_connectivity_from_edge_devices(provider_as_tenant_session, validator)
    else:
        conn_check = check_control_connectivity_from_edge_devices(origin_session, validator)
    if not conn_check:
        problems.append(f"Migrated devices cannot reach validator: {validator}")

    # Generate error message
    if problems:
        problem_lines = "\n".join(problems)
        message = f"Found {len(problems)} problems in precondition check for migration:\n{problem_lines}"
        raise_or_log_precondition_check(message, raises)
        return False
    logger.info("Preconditions checks for tenant migration succeeded!")
    return True


def migration_workflow(
    origin_session: ManagerSession,
    target_session: ManagerSession,
    workdir: Path,
    tenant: TenantExport,
    validator: str,
    raises: bool = True,
):
    """Performs migration from origin sdwan instance to target sdwan instance based on:
    https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b
    0. Perform pre-condition checks
    1. Export the deployment and configuration data from origin Cisco vManage instance controlling the overlay.
    2. Check the status of the data export task in Cisco vManage. Download the data when the task succeeds.
    3. On a target Cisco vManage instance, import the data exported from the origin overlay.
    4. Collect migration token using the token URL obtained in response to the API call in Step 3.
    5. On origin Cisco vManage instance, initiate the migration of the overlay to target deployment.

    Args:
        origin_session (ManagerSession): session to migration origin
        target_session (ManagerSession): session to migration target
        workdir (Path): directory to store migration artifacts (token and export file)
        tenant (MigrationTenant): Tenant object containig required fields: desc, name, subdomain, org_name
        validator (str): Target Validator (VBOND) IP address or domain name
        raises (bool): When true precondition check will raise, when false only warning will be logged
    """
    workdir.mkdir(parents=True, exist_ok=True)
    logger.info("0/5 Performing pre-checks ...")
    migration_preconditions_check(origin_session, target_session, tenant, validator, raises)
    origin_api = TenantMigrationAPI(origin_session)
    target_api = TenantMigrationAPI(target_session)
    migration_timestamp = datetime.now().strftime("%Y%m%d%H%M")
    migration_file_prefix = f"{tenant.name}-{origin_api.session.server_name}-{migration_timestamp}"
    export_path = workdir / f"{migration_file_prefix}.tar.gz"
    token_path = workdir / f"{migration_file_prefix}.token"

    logger.info(f"1/5 Exporting {tenant.name} ...")
    export_task = origin_api.export_tenant(tenant=tenant)
    remote_filename = export_task.wait_for_file()

    logger.info(f"2/5 Downloading {remote_filename} to {export_path} ...")
    origin_api.download(export_path, remote_filename)

    logger.info(f"3/5 Importing {export_path} ...")
    import_task = target_api.import_tenant(export_path, tenant.migration_key)

    logger.info("4/5 Obtaining migration token ...")
    import_task.wait_for_completed()
    migration_id = import_task.import_info.migration_token_query_params.migration_id
    target_api.store_token(migration_id, token_path)

    logger.info(f"5/5 Initiating network migration: {migration_id}, using token file: {token_path} ...")
    migrate_task = origin_api.migrate_network(token_path)
    migrate_task.wait_for_completed()
    logger.info(f"5/5 {tenant.name} migration completed successfully!")
