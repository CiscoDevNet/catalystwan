# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.api.task_status_api import Task
from catalystwan.endpoints.tenant_management import (
    TenantBulkDeleteRequest,
    TenantManagement,
    TenantStatus,
    TenantUpdateRequest,
    vSmartPlacementUpdateRequest,
    vSmartTenantCapacity,
    vSmartTenantMap,
)
from catalystwan.models.tenant import Tenant

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession

from catalystwan.typed_list import DataSequence


class TenantManagementAPI:
    def __init__(self, session: ManagerSession):
        self.session = session
        self._endpoints = TenantManagement(session)

    def get(self) -> DataSequence[Tenant]:
        """Lists all the tenants on the vManage.

        In a multitenant vManage system, this API is only avaiable in the Provider view.

        Returns:
            DataSequence[TenantInfo]: List-like object containing tenant information
        """
        return self._endpoints.get_all_tenants()

    def create(self, tenants: List[Tenant]) -> Task:
        """Creates tenants on vManage

        Args:
            tenants (List[Tenant]): List of tenants to be created

        Returns:
            Task: Object representing tenant creation process
        """
        task_id = self._endpoints.create_tenant_async_bulk(tenants).id
        return Task(self.session, task_id)

    def update(self, tenant_update_request: TenantUpdateRequest) -> Tenant:
        """Updates Tenant on vManage

        Args:
            tenant_update_request (TenantUpdateRequest): Tenant attributes to be updated (must contain tenantId)

        Returns:
            Tenant: Updated tenant data
        """
        return self._endpoints.update_tenant(
            tenant_id=tenant_update_request.tenant_id, tenant_update_request=tenant_update_request
        )

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
        task_id = self._endpoints.delete_tenant_async_bulk(delete_request).id
        return Task(self.session, task_id)

    def get_statuses(self) -> DataSequence[TenantStatus]:
        """Gets tenant statuses from vManage

        Returns:
            DataSequence[TenantStatus]: List-like object containing tenants statuses
        """
        return self._endpoints.get_all_tenant_statuses()

    def get_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        """Gets tenant hosting capacity on vSmarts

        Returns:
            DataSequence[vSmartTenantCapacity]: List-like object containing tenant capacity information for each vSmart
        """
        return self._endpoints.get_tenant_hosting_capacity_on_vsmarts()

    def update_vsmart_placement(self, tenant_id: str, src_vsmart_uuid: str, dst_vsmart_uuid: str):
        """Updates vSmart placement

        Args:
            tenant_id (str): Tenant ID
            src_vsmart_uuid (str): Source vSmart uuid
            dst_vsmart_uuid (str): Destination vSmart uuid
        """
        self._endpoints.update_tenant_vsmart_placement(
            tenant_id=tenant_id,
            vsmart_placement_update_request=vSmartPlacementUpdateRequest(
                srcvSmartUuid=src_vsmart_uuid, destvSmartUuid=dst_vsmart_uuid
            ),
        )

    def get_vsmart_mapping(self) -> vSmartTenantMap:
        """Gets vSmart to tenant mapping

        Returns:
            vSmartTenantMap: Contains vSmart to tenant mapping
        """
        return self._endpoints.get_tenant_vsmart_mapping()

    def vsession_id(self, tenant_id: str) -> str:
        """Gets VSessionId for given tenant

        Args:
            tenant_id (str): Tenant ID

        Returns:
            str: Contains VSessionId for given tenant
        """
        return self._endpoints.vsession_id(tenant_id).vsessionid
