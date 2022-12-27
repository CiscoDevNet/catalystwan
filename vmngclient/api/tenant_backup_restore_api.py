"""
Module for handling tenant backup and restore
"""
from pathlib import Path
from typing import Optional, Union

# from vmngclient.api.task_status_api import TaskStatus
from vmngclient.dataclasses import TenantBackupRestore
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.operation_status import OperationStatus, OperationStatusId


class TenantBackupRestoreApi:
    """
    Class for handling tenant backup and restore

    Attributes:
        session: logged in API client session
    """

    exit_statuses = [OperationStatus.SUCCESS.value,
                     OperationStatus.FAILURE.value]
    exit_statuses_ids = [OperationStatusId.SUCCESS.value,
                         OperationStatusId.FAILURE.value]

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def list_backups(self):
        """Returns a list of backup files stored on vManage
        tenant admin will see only his own tenant backupfiles
        provider will see all tenants backup files.

        Returns:
            list of filenames
        """
        response = self.session.get_json("/dataservice/tenantbackup/list")
        return create_dataclass(TenantBackupRestore, response)

    def export(self) -> str:
        """Export tenant backup file

        Returns:
            filename on vManage server of exported tenant backup file
        """
        response = self.session.get_json("/dataservice/tenantbackup/export")
        # task_status = TaskStatus(self.session)
        # result = task_status.wait_for_completed(5, 3000,
        #                               self.exit_statuses,
        #                               self.exit_statuses_ids,
        #                               response['processId'])
        return str(response)

    def delete(self, file_name) -> Union[dict, list]:
        """Delete tenant backup file

        Returns:
            http response for delete operation
        """

        url = f"/dataservice/tenantbackup/delete?fileName={file_name}"
        return self.session.delete(url).json()

    def delete_all(self) -> Union[dict, list]:
        return self.delete("all")

    def download(self, file_name: str, download_dir: Optional[Path] = None) -> Path:
        """Download tenant backup file

        Args:
            file_name: name of tenant backup file
            download_dir: download directory (defaults to current working directory)
        Returns:
            path to downloaded tenant backup file
        """

        download_dir = download_dir if download_dir else Path.cwd()
        download_path = download_dir / file_name
        tenant_id = file_name.split("_")[1]
        url = f"/dataservice/tenantbackup/download/{tenant_id}/{file_name}"
        response = self.session.get_file(url, download_path)
        return download_path

    def import_backup(self, filename: Path):
        """
        upload the specified file for tenant import,
        then poll the task until success or failure.
        Args:
            filename: The path of the file to be upladed
        Returns:
        """
        # Upload the file
        url = "/dataservice/tenantbackup/import"
        files = {"file": (filename.name, open(str(filename), "rb"))}
        response = self.session.post(url, data={}, files=files)
        # task_status = TaskStatus(self.session)
        # result = task_status.wait_for_completed(5, 3000,
        #                               self.exit_statuses,
        #                               self.exit_statuses_ids,
        #                               response.json()['processId'])
        return response
