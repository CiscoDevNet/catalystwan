# Copyright 2023 Cisco Systems, Inc. and its affiliates

"""
Module for apidocs/#/Tenant Backup Restore
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

from catalystwan.api.task_status_api import SubTaskData, Task

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

logger = logging.getLogger(__name__)


class TenantBackupRestoreAPI:
    """
    Class for tenant backup and restore

    Scope:
        Provider-as-tenant or tenant

    Attributes:
        session (ManagerSession): logged in API client session

    Example usage:
        from catalystwan.api.tenant_backup_restore_api import TenantBackupRestoreAPI
        from catalystwan.session import create_manager_session


        tenant_session = create_manager_session(
             tenant_domain, tenantadmin, password, port)
        provider_tenant_session = create_manager_session(
            domain, admin, password, port, subdomain=tenant_domain)

        tenant_backup_restore = TenantBackupRestoreAPI(tenant_session)
        provider_backup_restore = TenantBackupRestoreAPI(provider_tenant_session)

        file_name = tenant_backup_restore.export()
        file_list = provider_backup_restore.list()
        file = tenant_backup_restore.download(file_name)
        status = provider_backup_restore.import_file(file)
        deleted_list = tenant_backup_restore.delete(file_name)
        deleted_list = provider_backup_restore.delete_all()
    """

    def __init__(self, session: ManagerSession) -> None:
        self.session = session

    def list(self) -> list:
        """Return a list of backup files stored on vManage

        Returns:
            list of filenames

        Example usage:
            fileList = ProviderBackupRestore.list()
        """
        return self.session.get_json("/dataservice/tenantbackup/list")["backup_files"]

    def export(self, timeout: int = 300) -> str:
        """Export tenant backup file from DB to vManage storage

        Args:
            timeout: Max polling time for task (default: 300 seconds)

        Returns:
            str: filename of exported tenant backup file stored on vManage

        Example usage:
            fileName = ProviderBackupRestore.export()
        """
        response = self.session.get_json("/dataservice/tenantbackup/export")
        status = Task(self.session, response["processId"]).wait_for_completed(timeout_seconds=timeout)
        string = re.search("""file location: (.*)""", status.sub_tasks_data[0].activity[-1])
        assert string, "File location not found."
        return string.group(1)

    def delete(self, file: str) -> List[str]:
        """Delete tenant backup file

        Args:
            file (str): device ID (usually system-ip)

        Returns:
            http response for delete operation

        Example usage:
            message = ProviderBackupRestore.delete(fileName)
        """
        url = f"/dataservice/tenantbackup/delete?fileName={file}"
        return self.session.delete(url).json()["Deleted"]

    def delete_all(self) -> List[str]:
        """Delete all tenant backup files

        Returns:
            http response for delete operation

        Example usage:
            message = ProviderBackupRestore.delete_all()
        """
        return self.delete("all")

    def download(self, file: str, download_dir: Optional[Path] = None) -> Path:
        """Download tenant backup file

        Args:
            file: full path or base name of tenant backup file
            download_dir: download directory (defaul: current working directory)

        Returns:
            Path to downloaded tenant backup file

        Example usage:
            file = ProviderBackupRestore.download(fileName)
        """

        if "/dataservice/tenantbackup/download/" not in file:
            tenant_id = file.split("_")[1]
            file = f"/dataservice/tenantbackup/download/{tenant_id}/{file}"

        download_dir = download_dir if download_dir else Path.cwd()
        download = download_dir / Path(file).name
        self.session.get_file(file, download)
        return download

    def import_file(self, file: Path, timeout: int = 300) -> SubTaskData:
        """Upload the file for tenant import to the DB and poll for Success

        Args:
            file: The path of the file to be upladed
            timeout: Max polling time for task (default: 300 seconds)

        Returns:
            TaskStatus object with Success and Activity messages

        Example usage:
             status = ProviderBackupRestore.import_file(file)
        """

        url = "/dataservice/tenantbackup/import"
        files = {"file": (file.name, open(str(file), "rb"))}
        response = self.session.post(url, data={}, files=files)
        return (
            Task(self.session, response.json()["processId"])
            .wait_for_completed(timeout_seconds=timeout)
            .sub_tasks_data[0]
        )
