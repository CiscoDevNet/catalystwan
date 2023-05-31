from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from vmngclient.api.task_status_api import Task
from vmngclient.dataclasses import Device
from vmngclient.model.tenant import Tenant

if TYPE_CHECKING:
    from vmngclient.session import vManageSession

from vmngclient.typed_list import DataSequence


class TenantManagementAPI:
    def __init__(self, session: vManageSession):
        self.session = session

    def get_tenants(self, device_id: Optional[Device] = None) -> DataSequence[Tenant]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Args:
            device_id: Lists all tenants associated with a vSmart.

        Returns:
            DataSequence[TenantInfo]
        """

        if device_id:
            raise NotImplementedError()

        return self.session.primitives.tenant_management.get_all_tenants()

    def create_tenants(self, tenants: List[Tenant]) -> Task:
        task_id = self.session.primitives.tenant_management.create_tenant_async_bulk(tenants).id
        return Task(self.session, task_id)
