from __future__ import annotations

from typing import List, Optional

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
from vmngclient.session import vManageSession
from vmngclient.typed_list import DataSequence


class TenantManagementAPI:
    def __init__(self, session: vManageSession):
        self.session = session
        self.primitives = TenantManagementPrimitives(session)

    def get_all(self, device_id: Optional[Device] = None) -> DataSequence[Tenant]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Args:
            device_id: Lists all tenants associated with a vSmart.

        Returns:
            DataSequence[TenantInfo]
        """

        if device_id:
            raise NotImplementedError()

        return self.primitives.get_all_tenants()

    def create(self, tenants: List[Tenant]) -> Task:
        task_id = self.primitives.create_tenant_async_bulk(tenants).id
        return Task(self.session, task_id)

    def delete(self, delete_request: TenantBulkDeleteRequest) -> Task:
        task_id = self.primitives.delete_tenant_async_bulk(delete_request).id
        return Task(self.session, task_id)

    def get_statuses(self) -> DataSequence[TenantStatus]:
        return self.primitives.get_all_tenant_statuses()

    def get_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        return self.primitives.get_tenant_hosting_capacity_on_vsmarts()

    def get_vsmart_mapping(self) -> vSmartTenantMap:
        return self.primitives.get_tenant_vsmart_mapping()

    def vsession_id(self, tenant_id: str) -> str:
        return self.primitives.vsession_id(tenant_id).vsessionid
