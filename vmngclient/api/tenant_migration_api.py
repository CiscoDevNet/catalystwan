from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from packaging.version import Version  # type: ignore

from vmngclient.api.task_status_api import Task, TaskResult
from vmngclient.endpoints.tenant_migration import ImportInfo, MigrationFile, MigrationTokenQueryParams
from vmngclient.model.tenant import MigrationTenant, Tenant

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


def _get_file_name_from_export_task_result(task_result: TaskResult) -> str:
    filepath = re.search("""file location: (.*)""", task_result.sub_tasks_data[0].activity[-1])
    assert filepath, "File location not found."
    return Path(filepath.group(1)).name


class ImportTask(Task):
    def __init__(self, session: vManageSession, import_info: ImportInfo):
        super().__init__(session, import_info.process_id)
        self.import_info = import_info


class TenantMigrationAPI:
    """Set of methods used in tenant migration"""

    def __init__(self, session: vManageSession):
        self.session = session

    def export_tenant(self, tenant: Tenant) -> Task:
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance.
        Should be executed on migrated single-tenant system.

        Args:
            tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name

        Returns:
            Task: object representing initiated export process
        """
        process_id = self.session.endpoints.tenant_migration.export_tenant_data(tenant).process_id
        return Task(self.session, process_id)

    def download(self, download_path: Path, remote_filename: str = "default.tar.gz"):
        """Download exported single-tenant deployment and configuration data from a Cisco vManage instance
        to a local file system. Should be executed on migrated single-tenant system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            remote_filename (str): path to exported tenant migration file on vManage
        """
        tenant_data = self.session.endpoints.tenant_migration.download_tenant_data(remote_filename)
        with open(download_path, "wb") as file:
            file.write(tenant_data)

    def import_tenant(self, import_file: Path, migration_key: Optional[str] = None) -> ImportTask:
        """Imports the single-tenant deployment and configuration data into multi-tenant vManage instance.
        Should be executed on target multi-tenant system.

        Args:
            import_file (Path): full path to previously exported single-tenant data file
            migration_key (str): migration key (required starting from 20.13)

        Returns:
            ImportTask: object representing initiated import process
        """
        import_file_payload = MigrationFile(data=open(import_file, "rb"))
        if self.session.api_version >= Version("20.13") and migration_key is not None:
            import_info = self.session.endpoints.tenant_migration.import_tenant_data_with_key(
                import_file_payload, migration_key
            )
        else:
            import_info = self.session.endpoints.tenant_migration.import_tenant_data(import_file_payload)
        return ImportTask(self.session, import_info)

    def store_token(self, migration_id: str, download_path: Path):
        """Stores migration token as text file for given migration identifier.
        Should be executed on target multi-tenant system.

        Args:
            migration_id (str): migration identifier (it is obtained after import tenant task is finished)
            download_path (Path): full download path containing a filename eg.: Path("/home/user/import-token.txt")
        """
        params = MigrationTokenQueryParams(migrationId=migration_id)
        token = self.session.endpoints.tenant_migration.get_migration_token(params)
        with open(download_path, "w") as file:
            file.write(token)

    def migrate_network(self, token_file: Path) -> Task:
        """Starts migration procedure on single-tenant system.

        Args:
            token_file (Path): full path to previously stored text file with import token.

        Returns:
            Task: object representing initiated migration process
        """
        with open(token_file, "r") as file:
            token = file.read()
        process_id = self.session.endpoints.tenant_migration.migrate_network(token).process_id
        return Task(self.session, process_id)


def st_to_mt(st_api: TenantMigrationAPI, mt_api: TenantMigrationAPI, workdir: Path, tenant: MigrationTenant):
    """Performs single-tenant migration to multi-tenant environment procedure according to:
    https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b
    1. Export the single-tenant deployment and configuration data from a Cisco vManage instance controlling the overlay.
    2. Check the status of the data export task in Cisco vManage. Download the data when the task succeeds.
    3. On a multitenant Cisco vManage instance, import the data exported from the single-tenant overlay.
    4. Obtain the migration token using the token URL obtained in response to the API call in Step 3.
    5. On the single-tenant Cisco vManage instance, initiate the migration of the overlay to the multitenant deployment.

    Args:
        st_api (TenantMigrationAPI): TenantMigrationAPI created with session to migrated single-tenant vManage instance
        mt_api (TenantMigrationAPI): TenantMigrationAPI created with session to target multi-tenant vManage instance
        workdir (Path): directory to store migration artifacts (token and export file)
        tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name
    """
    migration_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    migration_file_prefix = f"{tenant.name}-{st_api.session.server_name}-{migration_timestamp}"
    export_path = workdir / f"{migration_file_prefix}.tar.gz"
    token_path = workdir / f"{migration_file_prefix}.token"
    migration_key = tenant.migration_key

    logger.info(f"1/5 Exporting {tenant.name} ...")
    export_task = st_api.export_tenant(tenant=tenant)
    export_result = export_task.wait_for_completed()
    remote_filename = _get_file_name_from_export_task_result(export_result)

    logger.info(f"2/5 Downloading {remote_filename} to {export_path} ...")
    st_api.download(export_path, remote_filename)

    logger.info(f"3/5 Importing {export_path} ...")
    import_task = mt_api.import_tenant(export_path, migration_key)

    logger.info("4/5 Obtaining migration token ...")
    import_task.wait_for_completed()
    migration_id = import_task.import_info.migration_token_query_params.migration_id
    mt_api.store_token(migration_id, token_path)

    logger.info(f"5/5 Initiating network migration: {migration_id}, using token file: {token_path} ...")
    migrate_task = st_api.migrate_network(token_path)
    migrate_task.wait_for_completed()
    logger.info(f"5/5 {tenant.name} migration completed successfully!")


def mt_to_st(st_api: TenantMigrationAPI, mt_api: TenantMigrationAPI, workdir: Path, tenant: MigrationTenant):
    """Performs single-tenant migration to multi-tenant environment procedure according to:
    https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/system-interface/vedge-20-x/systems-interfaces-book/sdwan-multitenancy.html#concept_sjj_jmm_z4b
    1. Export the MT deployment and configuration data from a Cisco vManage instance controlling the overlay.
    2. Check the status of the data export task in Cisco vManage. Download the data when the task succeeds.
    3. On a ST Cisco vManage instance, import the data exported from the MT tenant data.
    4. Obtain the migration token using the token URL obtained in response to the API call in Step 3.
    5. On the MT tenant Cisco vManage instance, initiate the migration of the overlay to the ST deployment.

    Args:
        st_api (TenantMigrationAPI): TenantMigrationAPI created with session to target single-tenant vManage instance
        mt_api (TenantMigrationAPI): TenantMigrationAPI created with session to source multi-tenant vManage instance
        workdir (Path): directory to store migration artifacts (token and export file)
        tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name
    """
    migration_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    migration_file_prefix = f"{tenant.name}-{st_api.session.server_name}-{migration_timestamp}"
    export_path = workdir / f"{migration_file_prefix}.tar.gz"
    token_path = workdir / f"{migration_file_prefix}.token"
    migration_key = tenant.migration_key

    logger.info(f"1/5 Exporting {tenant.name} ...")
    export_task = mt_api.export_tenant(tenant=tenant)
    export_result = export_task.wait_for_completed()
    remote_filename = _get_file_name_from_export_task_result(export_result)

    logger.info(f"2/5 Downloading {remote_filename} to {export_path} ...")
    mt_api.download(export_path, remote_filename)

    logger.info(f"3/5 Importing {export_path} ...")
    import_task = st_api.import_tenant(export_path, migration_key)

    logger.info("4/5 Obtaining migration token ...")
    import_task.wait_for_completed()
    migration_id = import_task.import_info.migration_token_query_params.migration_id
    st_api.store_token(migration_id, token_path)

    logger.info(f"5/5 Initiating network migration: {migration_id}, using token file: {token_path} ...")
    migrate_task = mt_api.migrate_network(token_path)
    migrate_task.wait_for_completed()
    logger.info(f"5/5 {tenant.name} migration completed successfully!")
