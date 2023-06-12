from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from vmngclient.api.task_status_api import Task
from vmngclient.dataclasses import Device
from vmngclient.model.tenant import Tenant
from vmngclient.primitives.tenant_management import (
    TenantBulkDeleteRequest,
    TenantManagementPrimitives,
    TenantStatus,
    vSmartTenantCapacity,
    vSmartTenantMap,
)

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.typed_list import DataSequence


class TenantManagementAPI:
    def __init__(self, session: vManageSession):
        self.session = session
        self._primitives = TenantManagementPrimitives(session)

    def get_all(self, device_id: Optional[Device] = None) -> DataSequence[Tenant]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Returns:
            DataSequence[TenantInfo]: List-like object containing tenant information
        """
        return self._primitives.get_all_tenants()

    def create(self, tenants: List[Tenant]) -> Task:
        """Creates tenants on vManage

        Args:
            tenants (List[Tenant]): List of tenants to be created

        Returns:
            Task: Object representing tenant creation process
        """
        task_id = self._primitives.create_tenant_async_bulk(tenants).id
        return Task(self.session, task_id)

    def delete(self, tenant_id_list: List[str], password: Optional[str] = None) -> Task:
        """Deletes tenants on vManage

        Args:
            tenant_ids (List[str]): Tenant IDs to be deleted
            password (Optional[str]): Provider password if not provided current session password will be used

        Returns:
            Task: Object representing tenant deletion process
        """
        if password is None:
            password = self.session.password
        delete_request = TenantBulkDeleteRequest(tenantIdList=tenant_id_list, password=password)
        task_id = self._primitives.delete_tenant_async_bulk(delete_request).id
        return Task(self.session, task_id)

    def get_statuses(self) -> DataSequence[TenantStatus]:
        """Gets tenant statuses from vManage

        Returns:
            DataSequence[TenantStatus]: List-like object containing tenants statuses
        """
        return self._primitives.get_all_tenant_statuses()

    def get_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        """Gets tenant hosting capacity on vSmarts

        Returns:
            DataSequence[vSmartTenantCapacity]: List-like object containing tenant capacity information for each vSmart
        """
        return self._primitives.get_tenant_hosting_capacity_on_vsmarts()

    def get_vsmart_mapping(self) -> vSmartTenantMap:
        """Gets vSmart to tenant mapping

        Returns:
            vSmartTenantMap: Contains vSmart to tenant mapping
        """
        return self._primitives.get_tenant_vsmart_mapping()

    def vsession_id(self, tenant_id: str) -> str:
        """Gets VSessionId for given tenant

        Args:
            tenant_id (str): Tenant ID

        Returns:
            str: Contains VSessionId for given tenant
        """
        return self._primitives.vsession_id(tenant_id).vsessionid
