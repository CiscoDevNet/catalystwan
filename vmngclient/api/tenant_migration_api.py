from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional, overload

from packaging.version import Version  # type: ignore

from vmngclient.api.task_status_api import Task, TaskResult
from vmngclient.model.tenant import Tenant

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


def _get_file_name_from_export_task_result(task_result: TaskResult) -> str:
    filepath = re.search("""file location: (.*)""", task_result.sub_tasks_data[0].activity[-1])
    assert filepath, "File location not found."
    return Path(filepath.group(1)).name


class TenantMigrationAPI:
    """Set of methods used in tenant migration"""

    def __init__(self, session: vManageSession):
        self.session = session

    @overload
    def export_tenant(
        self, *, desc: str, name: str, subdomain: str, org_name: str, wan_edge_forecast: Optional[int]
    ) -> Task:
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance.

        Args:
            desc (str): A description of the tenant. Up to 256 alphanumeric characters.
            name (str): Unique name for the tenant in the multitenant deployment.
            subdomain (str): Fully qualified sub-domain name of the tenant.
            org_name (str): Name of the tenant organization. The organization name is case-sensitive.
            wan_edge_forecast (int): Forecasted number of WAN Edges for given tenant.
        Returns:
            Task: object representing initiated export process
        """
        ...

    @overload
    def export_tenant(self, *, tenant: Tenant) -> Task:
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance.

        Args:
            tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name

        Returns:
            Task: object representing initiated export process
        """
        ...

    def export_tenant(self, **kwargs) -> Task:
        tenant = kwargs.get("tenant", None)
        if tenant is None:
            tenant = Tenant.parse_obj(**kwargs)
        if self.session.api_version < Version("20.6"):
            tenant.wan_edge_forecast = None
        process_id = self.session.primitives.tenant_migration.export_tenant_data(tenant).process_id
        return Task(self.session, process_id)

    def download(self, download_path: Path, remote_filename: str = "default.tar.gz"):
        """Download exported single-tenant deployment and configuration data from a Cisco vManage instance
        to a local file system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            remote_filename (str): path to exported tenant migration file on vManage
        """
        tenant_data = self.session.primitives.tenant_migration.download_tenant_data(remote_filename)
        open(download_path, "wb").write(tenant_data)

    @overload
    def collect(
        self,
        download_path: Path,
        timeout: int = 300,
        *,
        desc: str,
        name: str,
        subdomain: str,
        org_name: str,
        wan_edge_forecast: Optional[int],
    ):
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance then
        waits for export to complete and downloads tenant data to a local file system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            timeout (int): timeout for wait until export task is completed in seconds
            desc (str): A description of the tenant. Up to 256 alphanumeric characters.
            name (str): Unique name for the tenant in the multitenant deployment.
            subdomain (str): Fully qualified sub-domain name of the tenant.
            org_name (str): Name of the tenant organization. The organization name is case-sensitive.
            wan_edge_forecast (int): Forecasted number of WAN Edges for given tenant.
        """
        ...

    @overload
    def collect(self, download_path: Path, timeout: int = 300, *, tenant: Tenant):
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance then
        waits for export to complete and downloads tenant data to a local file system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            timeout (int): timeout for wait until export task is completed in seconds
            tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name
        """
        ...

    def collect(self, download_path: Path, timeout: int = 300, **kwargs):
        export_task = self.export_tenant(**kwargs)
        export_result = export_task.wait_for_completed(timeout_seconds=timeout)
        remote_filename = _get_file_name_from_export_task_result(export_result)
        return self.download(download_path, remote_filename)

    def import_tenant(self, path: Path) -> Task:
        """Imports the single-tenant deployment and configuration data into multi-tenant vManage instance.

        Args:
            path (Path): full path to previously exported single-tenant data file

        Returns:
            Task: object representing initiated import process
        """
        process_id = self.session.primitives.tenant_migration.import_tenant_data(open(path, "rb")).process_id
        return Task(self.session, process_id)
