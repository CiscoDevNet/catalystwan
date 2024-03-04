# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Dict, List, Optional

from pydantic.v1 import BaseModel, Field

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions, view
from catalystwan.models.tenant import Tenant
from catalystwan.typed_list import DataSequence
from catalystwan.utils.session_type import ProviderAsTenantView, ProviderView


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


class TenantUpdateRequest(BaseModel):
    tenant_id: str = Field(alias="tenantId")
    subdomain: str = Field(alias="subDomain")
    desc: str
    wan_edge_forecast: Optional[int] = Field(alias="wanEdgeForecast")
    edge_connector_enable: Optional[bool] = Field(alias="edgeConnectorEnable")
    edge_connector_system_ip: Optional[str] = Field(alias="edgeConnectorSystemIp")
    edge_connector_tunnel_interface_name: Optional[str] = Field(alias="edgeConnectorTunnelInterfaceName")

    @classmethod
    def from_tenant(cls, tenant: Tenant) -> "TenantUpdateRequest":
        """Creates payload for tenant update from existing tenant data obtained by GET

        Args:
            tenant (Tenant): Tenant to be updated

        Raises:
            TypeError: When provided tenant is missing ID

        Returns:
            TenantUpdateRequest: Tenant attributes suitable for PUT request
        """
        if not tenant.tenant_id:
            raise TypeError("tenantId required for update request")
        return TenantUpdateRequest(
            tenantId=tenant.tenant_id,
            desc=tenant.desc,
            subDomain=tenant.subdomain,
            wanEdgeForecast=tenant.wan_edge_forecast,
            edgeConnectorEnable=tenant.edge_connector_enable,
            edgeConnectorSystemIp=tenant.edge_connector_system_ip,
            edgeConnectorTunnelInterfaceName=tenant.edge_connector_tunnel_interface_name,
        )


class vSmartPlacementUpdateRequest(BaseModel):
    src_vsmart_uuid: str = Field(alias="srcvSmartUuid")
    dest_vsmart_uuid: str = Field(alias="destvSmartUuid")


class vSmartTenantCapacity(BaseModel):
    vsmart_uuid: str = Field(alias="vSmartUuid")
    total_tenant_capacity: int = Field(alias="totalTenantCapacity")
    current_tenant_count: int = Field(alias="currentTenantCount")


class vSmartTenantMap(BaseModel):
    data: Dict[str, List[Tenant]]


class vSessionId(BaseModel):
    vsessionid: str = Field(alias="VSessionId")


class TenantManagement(APIEndpoints):
    @view({ProviderView})
    @post("/tenant")
    def create_tenant(self, payload: Tenant) -> Tenant:
        ...

    @view({ProviderView})
    @post("/tenant/async")
    def create_tenant_async(self, payload: Tenant) -> TenantTaskId:
        ...

    @versions(">=20.4")
    @view({ProviderView})
    @post("/tenant/bulk/async")
    def create_tenant_async_bulk(self, payload: List[Tenant]) -> TenantTaskId:
        ...

    @view({ProviderView})
    @delete("/tenant/{tenant_id}/delete")
    def delete_tenant(self, tenant_id: str, payload: TenantDeleteRequest) -> None:
        ...

    @versions(">=20.4")
    @view({ProviderView})
    @delete("/tenant/bulk/async")
    def delete_tenant_async_bulk(self, payload: TenantBulkDeleteRequest) -> TenantTaskId:
        ...

    def force_status_collection(self):
        # POST /tenantstatus/force
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenantstatus", "data")
    def get_all_tenant_statuses(self) -> DataSequence[TenantStatus]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant", "data")
    def get_all_tenants(self) -> DataSequence[Tenant]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant/{tenant_id}")
    def get_tenant(self, tenant_id: str) -> Tenant:
        ...

    @view({ProviderView})
    @get("/tenant/vsmart/capacity", "data")
    def get_tenant_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        ...

    @view({ProviderView, ProviderAsTenantView})
    @get("/tenant/vsmart")
    def get_tenant_vsmart_mapping(self) -> vSmartTenantMap:
        ...

    def switch_tenant(self):
        # POST /tenant/{tenantId}/switch
        ...

    def tenant_vsmart_mt_migrate(self):
        # POST /tenant/vsmart-mt/migrate
        ...

    @view({ProviderView})
    @put("/tenant/{tenant_id}")
    def update_tenant(self, tenant_id: str, payload: TenantUpdateRequest) -> Tenant:
        ...

    @view({ProviderView})
    @put("/tenant/{tenant_id}/vsmart")
    def update_tenant_vsmart_placement(self, tenant_id: str, payload: vSmartPlacementUpdateRequest) -> None:
        ...

    @view({ProviderView})
    @post("/tenant/{tenant_id}/vsessionid")
    def vsession_id(self, tenant_id: str) -> vSessionId:
        ...
