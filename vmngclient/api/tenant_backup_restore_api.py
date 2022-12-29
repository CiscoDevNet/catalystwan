"""
Module for tenant backup and restore API
"""
import logging
import re
from pathlib import Path
from typing import Optional, Union

from vmngclient.api.task_status_api import TaskStatus
from vmngclient.dataclasses import TenantBackupRestore
from vmngclient.session import vManageSession
from vmngclient.utils.creation_tools import create_dataclass

logger = logging.getLogger(__name__)


class TenantBackupRestoreApi:
    """
    Class for handling tenant backup and restore

    Attributes:
        session: logged in API client session
    """

    def __init__(self, session: vManageSession) -> None:
        self.session = session

    def __str__(self) -> str:
        return str(self.session)

    def list_backups(self) -> TenantBackupRestore:
        """Returns a list of backup files stored on vManage
        tenant admin will see only his own tenant backupfiles
        provider will see all tenants backup files.

        Returns:
            list of filenames
        """
        response = self.session.get_json("/dataservice/tenantbackup/list")
        return create_dataclass(TenantBackupRestore, response)

    def export(self, timeout: int = 300) -> str:
        """Export tenant backup file

        Returns:
            filename on vManage server of exported tenant backup file
        """
        response = self.session.get_json("/dataservice/tenantbackup/export")
        task_status = TaskStatus(self.session)
        result = task_status.wait_for_completed(response["processId"], timeout, 5)
        string = re.search("""file location: (.*)""", result.activity[-1])
        assert string, "File locationa not found."
        return string.group(1)

    def delete(self, file: str) -> Union[dict, list]:
        """Delete tenant backup file

        Returns:
            http response for delete operation
        """
        url = f"/dataservice/tenantbackup/delete?fileName={file}"
        return self.session.delete(url).json()

    def delete_all(self) -> Union[dict, list]:
        return self.delete("all")

    def download(self, file: str, download_dir: Optional[Path] = None) -> Path:
        """Download tenant backup file

        Args:
            file: name of tenant backup file
            download_dir: download directory (defaults to current working directory)
        Returns:
            path to downloaded tenant backup file
        """

        if "/dataservice/tenantbackup/download/" not in file:
            tenant_id = file.split("_")[1]
            file = f"/dataservice/tenantbackup/download/{tenant_id}/{file}"

        download_dir = download_dir if download_dir else Path.cwd()
        download = download_dir / Path(file).name
        self.session.get_file(file, download)
        return download

    def import_backup(self, file: Path, timeout: int = 300) -> TaskStatus:
        """
        upload the specified file for tenant import,
        then poll the task until success or failure.
        Args:
            file: The path of the file to be upladed
        Returns:
        """

        url = "/dataservice/tenantbackup/import"
        files = {"file": (file.name, open(str(file), "rb"))}
        response = self.session.post(url, data={}, files=files)

        task_status = TaskStatus(self.session)
        result = task_status.wait_for_completed(response.json()['processId"], timeout, 5)
        return result
