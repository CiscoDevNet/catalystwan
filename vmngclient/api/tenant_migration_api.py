from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from packaging.version import Version  # type: ignore

from vmngclient.api.task_status_api import Task, TaskResult
from vmngclient.endpoints.tenant_migration import ImportInfo, MigrationFile, MigrationTokenQueryParams
from vmngclient.exceptions import TenantMigrationExportFileNotFound, TenantMigrationPreconditionsError
from vmngclient.model.tenant import MigrationTenant, Tenant
from vmngclient.utils.session_type import SessionType

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


def raise_or_log_precondition_check(msg: str, raises: bool) -> None:
    if raises:
        raise TenantMigrationPreconditionsError(msg)
    logger.warning(msg)


class ExportTask(Task):
    def __init__(self, session: vManageSession, task_id: str):
        super().__init__(session, task_id)

    @staticmethod
    def get_file_name_from_export_task_result(task_result: TaskResult) -> str:
        filepath = re.search("""file location: (.*)""", task_result.sub_tasks_data[0].activity[-1])
        if not filepath:
            raise TenantMigrationExportFileNotFound("Client cannot find export file name in export task result")
        return Path(filepath.group(1)).name

    def wait_for_file(self) -> str:
        task_result = super().wait_for_completed()
        return self.get_file_name_from_export_task_result(task_result)


class ImportTask(Task):
    def __init__(self, session: vManageSession, import_info: ImportInfo):
        super().__init__(session, import_info.process_id)
        self.import_info = import_info


class TenantMigrationAPI:
    """Set of methods used in tenant migration"""

    def __init__(self, session: vManageSession):
        self.session = session

    def export_tenant(self, tenant: Tenant) -> ExportTask:
        """Exports the deployment and configuration data from a Cisco vManage instance.
        Should be executed on migration origin.

        Args:
            tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name

        Returns:
            Task: object representing initiated export process
        """
        process_id = self.session.endpoints.tenant_migration.export_tenant_data(tenant).process_id
        return ExportTask(self.session, process_id)

    def download(self, download_path: Path, remote_filename: str = "default.tar.gz"):
        """Download exported deployment and configuration data from a Cisco vManage instance
        to a local file system. Should be executed on migration target.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            remote_filename (str): path to exported tenant migration file on vManage
        """
        tenant_data = self.session.endpoints.tenant_migration.download_tenant_data(remote_filename)
        with open(download_path, "wb") as file:
            file.write(tenant_data)

    def import_tenant(self, import_file: Path, migration_key: Optional[str] = None) -> ImportTask:
        """Imports the deployment and configuration data into multi-tenant vManage instance.
        Should be executed on migration target.

        Args:
            import_file (Path): full path to previously exported data file
            migration_key (str): migration key (required starting from 20.13)

        Returns:
            ImportTask: object representing initiated import process
        """
        import_file_payload = MigrationFile(import_file)
        if self.session.api_version >= Version("20.13") and migration_key is not None:
            import_info = self.session.endpoints.tenant_migration.import_tenant_data_with_key(
                import_file_payload, migration_key
            )
        else:
            import_info = self.session.endpoints.tenant_migration.import_tenant_data(import_file_payload)
        return ImportTask(self.session, import_info)

    def store_token(self, migration_id: str, download_path: Path):
        """Stores migration token as text file for given migration identifier.
        Should be executed on migration target.

        Args:
            migration_id (str): migration identifier (it is obtained after import tenant task is finished)
            download_path (Path): full download path containing a filename eg.: Path("/home/user/import-token.txt")
        """
        params = MigrationTokenQueryParams(migrationId=migration_id)
        token = self.session.endpoints.tenant_migration.get_migration_token(params)
        with open(download_path, "w") as file:
            file.write(token)

    def migrate_network(self, token_file: Path) -> Task:
        """Starts migration procedure on migration origin.

        Args:
            token_file (Path): full path to previously stored text file with import token.

        Returns:
            Task: object representing initiated migration process
        """
        with open(token_file, "r") as file:
            token = file.read()
        process_id = self.session.endpoints.tenant_migration.migrate_network(token).process_id
        return Task(self.session, process_id)


def migration_preconditions_check(
    origin_session: vManageSession, target_session: vManageSession, tenant: MigrationTenant, raises: bool
) -> bool:
    """Perform precondition checks prior tenant migration

    Args:
        origin_session (vManageSession): session to migration origin
        target_session (vManageSession): session to migration target
        tenant (MigrationTenant): Tenant object containig required fields: desc, name, subdomain, org_name
        raises (bool): When true precondition check will raise, when false only warning will be logged

    Returns:
        bool: true only when all preconditions pass
    """
    problems: List[str] = []
    target_org = target_session.endpoints.configuration_settings.get_organizations().first().org
    if target_session.session_type == SessionType.PROVIDER:
        if not tenant.is_destination_overlay_mt:
            problems.append("Migrating to MT but 'isDestinationOverlayMT' is not set")
        if origin_session.session_type != SessionType.SINGLE_TENANT:
            problems.append(
                "Migration to MT (using provider) is expected to be initiated from ST (using single tenant)"
            )
        if not tenant.org_name.startswith(target_org):
            problems.append(f"Provided '{tenant.org_name}' but target organization is '{target_org}'")
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

    if target_session.api_version != origin_session.api_version:
        problems.append(
            f"Migration source and target expect to have same version but found "
            f"origin: {origin_session.api_version} "
            f"target: {target_session.api_version}",
        )
    if problems:
        problem_lines = "\n".join(problems)
        message = f"Found {len(problems)} problems in precondition check for migration:\n{problem_lines}"
        raise_or_log_precondition_check(message, raises)
        return False
    return True


def migration_workflow(
    origin_session: vManageSession,
    target_session: vManageSession,
    workdir: Path,
    tenant: MigrationTenant,
    raises: bool = True,
):
    """Performs migration from origin sdwan instance to target sdwan instance based on:
    https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b
    1. Export the deployment and configuration data from origin Cisco vManage instance controlling the overlay.
    2. Check the status of the data export task in Cisco vManage. Download the data when the task succeeds.
    3. On a target Cisco vManage instance, import the data exported from the origin overlay.
    4. Collect migration token using the token URL obtained in response to the API call in Step 3.
    5. On origin Cisco vManage instance, initiate the migration of the overlay to target deployment.

    Args:
        origin_session (vManageSession): session to migration origin
        target_session (vManageSession): session to migration target
        workdir (Path): directory to store migration artifacts (token and export file)
        tenant (MigrationTenant): Tenant object containig required fields: desc, name, subdomain, org_name
        raises (bool): When true precondition check will raise, when false only warning will be logged
    """
    migration_preconditions_check(origin_session, target_session, tenant, raises)
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
