from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, IPvAnyAddress

from vmngclient.primitives import APIPrimitiveBase, Versions, View
from vmngclient.typed_list import DataSequence
from vmngclient.utils.session_type import ProviderAsTenantView, ProviderView


class MTEdge(BaseModel):
    uuid: str
    configured_hostname: Optional[str] = Field(alias="configuredHostname")
    configured_system_ip: Optional[IPvAnyAddress] = Field(alias="configuredSystemIP")
    management_system_ip: Optional[IPvAnyAddress] = Field(alias="managementSystemIP")
    device_model: Optional[str] = Field(alias="deviceModel")
    device_type: Optional[str] = Field(alias="deviceType")


class TenantVPNMap(BaseModel):
    tenant_vpn: int = Field(alias="tenantVPN")
    device_vpn: int = Field(alias="deviceVPN")


class Tenant(BaseModel):
    name: str
    org_name: str = Field(alias="orgName")
    subdomain: str = Field(alias="subDomain")
    flake_id: Optional[int] = Field(alias="flakeId")
    vbond_address: Optional[str] = Field(alias="vBondAddress")
    edge_connector_system_ip: Optional[str] = Field(alias="edgeConnectorSystemIp")
    edge_connector_enable: Optional[bool] = Field(alias="edgeConnectorEnable")
    vsmarts: List[str] = Field(alias="vSmarts", default=[])
    wan_edge_forecast: Optional[int] = Field(alias="wanEdgeForecast")
    saml_sp_info: Optional[str] = Field(alias="samlSpInfo")
    idp_map: Union[Dict, str, None] = Field(alias="idpMap")
    config_db_cluster_service_name: Optional[str] = Field(alias="configDBClusterServiceName")
    old_idp_map: Union[Dict, str, None] = Field(alias="oldIdpMap")
    created_at: Optional[datetime] = Field(alias="createdAt")
    rid: Optional[int] = Field(alias="@rid")
    edge_connector_tunnel_interface_name: Optional[str] = Field(alias="edgeConnectorTunnelInterfaceName")
    tenant_id: Optional[str] = Field(alias="tenantId")
    sp_metadata: Optional[str] = Field(alias="spMetadata")
    state: Optional[str]
    wan_edge_present: Optional[int] = Field(alias="wanEdgePresent")
    desc: Optional[str]
    mt_edge: Optional[List[MTEdge]] = Field(alias="mtEdge")
    mt_edge_count: Optional[int] = Field(alias="mtEdgeCount")
    tenant_vpn_map: Optional[List[TenantVPNMap]] = Field(alias="tenantVPNmap")
    tenant_provider_vpn_count: Optional[int] = Field(alias="tenantProviderVPNCount")


class TenantDeleteRequest(BaseModel):
    password: str


class TenantBulkDeleteRequest(TenantDeleteRequest):
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


class MultitenantAPIsProviderAPI(APIPrimitiveBase):
    @View({ProviderView})
    def create_tenant(self, tenant: Tenant) -> Tenant:
        response = self.post("/tenant", payload=tenant)
        return response.dataobj(Tenant, None)

    @View({ProviderView})
    def create_tenant_async(self, tenant: Tenant) -> TenantTaskId:
        response = self.post("/tenant/async", payload=tenant)
        return response.dataobj(TenantTaskId, None)

    @Versions(">=20.4")
    @View({ProviderView})
    def create_tenant_async_bulk(self, tenants: List[Tenant]) -> TenantTaskId:
        response = self.post("/tenant/bulk/async", payload=tenants)
        return response.dataobj(TenantTaskId, None)

    @View({ProviderView})
    def delete_tenant(self, delete_request: TenantDeleteRequest, tenant_id: str):
        self.post(f"/tenant/{tenant_id}/delete", payload=delete_request)

    @Versions(">=20.4")
    @View({ProviderView})
    def delete_tenant_async_bulk(self, delete_request: TenantBulkDeleteRequest) -> TenantTaskId:
        response = self.delete("/tenant/bulk/async", payload=delete_request)
        return response.dataobj(TenantTaskId, None)

    def delete_tenant_backup(self):
        # DELETE /tenantbackup/delete
        ...

    def download_existing_backup_file(self):
        # GET /tenantbackup/download/{path}
        ...

    def export_tenant_backup(self):
        # GET /tenantbackup/export
        ...

    def force_status_collection(self):
        # POST /tenantstatus/force
        ...

    @View({ProviderView})
    def get_all_tenant_statuses(self):
        self.get("/tenantstatus").dataseq(TenantStatus)

    @View({ProviderView})
    def get_all_tenants(self) -> DataSequence[Tenant]:
        return self.get("/tenant").dataseq(Tenant)

    @View({ProviderView})
    def get_tenant(self, tenant_id: str) -> Tenant:
        return self.get(f"/tenant/{tenant_id}").dataobj(Tenant, None)

    @View({ProviderView})
    def get_tenant_hosting_capacity_on_vsmarts(self) -> DataSequence[vSmartTenantCapacity]:
        return self.get("/tenant/vsmart/capacity").dataseq(vSmartTenantCapacity)

    @View({ProviderView})
    def get_tenant_vsmart_mapping(self) -> vSmartTenantMap:
        return self.get("/tenant/vsmart").dataobj(vSmartTenantMap, None)

    def import_tenant_backup(self):
        # POST /tenantbackup/import
        ...

    def list_tenant_backup(self):
        # GET /tenantbackup/list
        ...

    def switch_tenant(self):
        # POST /tenant/{tenantId}/switch
        ...

    def tenantv_smart_mt_migrate(self):
        # POST /tenant/vsmart-mt/migrate
        ...

    def update_tenant(self):
        # PUT /tenant/{tenantId}
        ...

    def update_tenant_vsmart_placement(self):
        # PUT /tenant/{tenantId}/vsmart
        ...

    @View({ProviderAsTenantView})
    def vsession_id(self, tenant_id: str):
        return self.post(f"/tenant/{tenant_id}/vsessionid").dataobj(vSessionId, None)
