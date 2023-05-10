from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional, overload

from packaging.version import Version  # type: ignore

from vmngclient.api.task_status_api import Task, TaskResult
from vmngclient.model.tenant import Tenant

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


def get_file_name_from_export_task_result(task_result: TaskResult) -> str:
    filepath = re.search("""file location: (.*)""", task_result.sub_tasks_data[0].activity[-1])
    assert filepath, "File location not found."
    return Path(filepath.group(1)).name


class TenantMigrationAPI:
    """Set of methods used in tenant migration"""

    def __init__(self, session: vManageSession):
        self.session = session

    @overload
    def export(self, *, desc: str, name: str, subdomain: str, org_name: str, wan_edge_forecast: Optional[int]) -> Task:
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance.

        Args:
            desc (str): A description of the tenant. Up to 256 alphanumeric characters.
            name (str): Unique name for the tenant in the multitenant deployment.
            subdomain (str): Fully qualified sub-domain name of the tenant.
            org_name (str): Name of the tenant organization. The organization name is case-sensitive.
            wan_edge_forecast (int): Forecasted number of WAN Edges for given tenant
        Returns:
            Task: object representing initiated export process
        """
        ...

    @overload
    def export(self, *, tenant: Tenant) -> Task:
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance.

        Args:
            tenant (Tenant): Tenant object containig required fields: desc, name, subdomain, org_name

        Returns:
            Task: object representing initiated export process
        """
        ...

    def export(self, **kwargs) -> Task:
        tenant = kwargs.get("tenant", None)
        if tenant is None:
            tenant = Tenant.parse_obj(**kwargs)
        if self.session.api_version < Version("20.6"):
            tenant.wan_edge_forecast = None
        process_id = self.session.primitives.tenant_migration.export_tenant_data(tenant).process_id
        return Task(self.session, process_id)

    def download(self, download_path: Path, remote_filename: Optional[str]):
        """Download exported single-tenant deployment and configuration data from a Cisco vManage instance
        to a local file system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
        """
        tenant_data = self.session.primitives.tenant_migration.download_tenant_data(remote_filename)
        open(download_path, "wb").write(tenant_data)

    @overload
    def collect(self, download_path: Path, timeout: int = 300, *, desc: str, name: str, subdomain: str, org_name: str):
        """Exports the single-tenant deployment and configuration data from a Cisco vManage instance then
        waits for export to complete and downloads tenant data to a local file system.

        Args:
            download_path (Path): full download path containing a filename eg.: Path("/home/user/tenant-export.tar.gz")
            timeout (int): timeout for wait until export task is completed in seconds
            desc (str): A description of the tenant. Up to 256 alphanumeric characters.
            name (str): Unique name for the tenant in the multitenant deployment.
            subdomain (str): Fully qualified sub-domain name of the tenant.
            org_name (str): Name of the tenant organization. The organization name is case-sensitive.
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
        export_task = self.export(**kwargs)
        export_result = export_task.wait_for_completed(timeout_seconds=timeout)
        remote_filename = get_file_name_from_export_task_result(export_result)
        return self.download(download_path, remote_filename)
