from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from packaging.version import Version  # type: ignore

from vmngclient.api.task_status_api import Task, TaskResult
from vmngclient.endpoints.tenant_migration import ImportInfo, MigrationFile, MigrationTokenQueryParams
from vmngclient.exceptions import TenantMigrationExportFileNotFound
from vmngclient.model.tenant import TenantExport

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


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

    def export_tenant(self, tenant: TenantExport) -> ExportTask:
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
        to a local file system. Should be executed on migration origin.

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
