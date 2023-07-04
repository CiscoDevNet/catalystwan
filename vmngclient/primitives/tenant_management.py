# mypy: disable-error-code="empty-body"
from typing import Dict, List

from pydantic import BaseModel, Field

from vmngclient.model.tenant import Tenant
from vmngclient.primitives import APIPrimitiveBase, post, request, versions, view
from vmngclient.typed_list import DataSequence
from vmngclient.utils.session_type import ProviderAsTenantView, ProviderView


class TenantDeleteRequest(BaseModel):
    password: str


class TenantBulkDeleteRequest(BaseModel):
    password: str
    tenant_id_list: List[str] = Field(alias="tenantIdList")


class TenantTaskId(BaseModel):
    id: str


class CertificatesStatus(BaseModel):
    invalid: int
    warning: int
    revoked: int


class ControlStatus(BaseModel):
    control_up: int = Field(alias="controlUp")
    partial: int
    control_down: int = Field(alias="controlDown")


class SiteHealth(BaseModel):
    full_connectivity: int = Field(alias="fullConnectivity")
    partial_connectivity: int = Field(alias="partialConnectivity")
    no_connectivity: int = Field(alias="noConnectivity")


class vEdgeHealth(BaseModel):
    normal: int
    warning: int
    error: int


class vSmartStatus(BaseModel):
    up: int
    down: int


class TenantStatus(BaseModel):
    tenant_id: str = Field(alias="tenantId")
    tenant_name: str = Field(alias="tenantName")
    control_status: ControlStatus = Field(alias="controlStatus")
    site_health: SiteHealth = Field(alias="siteHealth")
    vedge_health: vEdgeHealth = Field(alias="vEdgeHealth")
    vsmart_status: vSmartStatus = Field(alias="vSmartStatus")


class vSmartTenantCapacity(BaseModel):
    vsmart_uuid: str = Field(alias="vSmartUuid")
    total_tenant_capacity: int = Field(alias="totalTenantCapacity")
    current_tenant_count: int = Field(alias="currentTenantCount")


class vSmartTenantMap(BaseModel):
    data: Dict[str, List[Tenant]]


class vSessionId(BaseModel):
    vsessionid: str = Field(alias="VSessionId")


class TenantManagementPrimitives(APIPrimitiveBase):
    @view({ProviderView})
    def create_tenant(self, tenant: Tenant) -> Tenant:
        response = self._post("/tenant", payload=tenant)
        return response.dataobj(Tenant, None)

    @view({ProviderView})
    def create_tenant_async(self, tenant: Tenant) -> TenantTaskId:
        response = self._post("/tenant/async", payload=tenant)
        return response.dataobj(TenantTaskId, None)

    @versions(">=20.4")
    @view({ProviderView})
    @request(post, "/tenant/bulk/async")
    def create_tenant_async_bulk(self, payload: List[Tenant]) -> TenantTaskId:
        ...

    @view({ProviderView})
    def delete_tenant(self, delete_request: TenantDeleteRequest, tenant_id: str):
        self._post(f"/tenant/{tenant_id}/delete", payload=delete_request)

    @versions(">=20.4")
    @view({ProviderView})
    def delete_tenant_async_bulk(self, delete_request: TenantBulkDeleteRequest) -> TenantTaskId:
        response = self._delete("/tenant/bulk/async", payload=delete_request)
        return response.dataobj(TenantTaskId, None)

    def force_status_collection(self):
        # POST /tenantstatus/force
        ...

    @view({ProviderView, ProviderAsTenantView})
    def get_all_tenant_statuses(self) -> DataSequence[TenantStatus]:
        return self._get("/tenantstatus").dataseq(TenantStatus)

    @view({ProviderView, ProviderAsTenantView})
    def get_all_tenants(self) -> DataSequence[Tenant]:
        return self._get("/tenant").dataseq(Tenant)

    @view({ProviderView, ProviderAsTenantView})
    def get_tenant(self, tenant_id: str) -> Tenant:
        return self._get(f"/tenant/{tenant_id}").dataobj(Tenant, None)

    @view({ProviderView})
    def get_tenant_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        return self._get("/tenant/vsmart/capacity").dataseq(vSmartTenantCapacity)

    @view({ProviderView, ProviderAsTenantView})
    def get_tenant_vsmart_mapping(self) -> vSmartTenantMap:
        return self._get("/tenant/vsmart").dataobj(vSmartTenantMap, None)

    def switch_tenant(self):
        # POST /tenant/{tenantId}/switch
        ...

    def tenant_vsmart_mt_migrate(self):
        # POST /tenant/vsmart-mt/migrate
        ...

    def update_tenant(self):
        # PUT /tenant/{tenantId}
        ...

    def update_tenant_vsmart_placement(self):
        # PUT /tenant/{tenantId}/vsmart
        ...

    @view({ProviderView})
    def vsession_id(self, tenant_id: str) -> vSessionId:
        return self._post(f"/tenant/{tenant_id}/vsessionid").dataobj(vSessionId, None)
