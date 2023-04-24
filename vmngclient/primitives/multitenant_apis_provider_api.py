from typing import List, Optional

from pydantic import BaseModel, Field

from vmngclient.primitives import APIPrimitiveBase
from vmngclient.typed_list import DataSequence


class Tenant(BaseModel):
    flake_id: Optional[int] = Field(alias="flakeId")
    org_name: Optional[str] = Field(alias="orgName")
    saml_sp_info: Optional[str] = Field(alias="samlSpInfo")
    idp_map: Optional[str] = Field(alias="idpMap")
    sub_domain: Optional[str] = Field(alias="subDomain")
    vbond_address: Optional[str] = Field(alias="vBondAddress")
    config_db_cluster_service_name: Optional[str] = Field(alias="configDBClusterServiceName")
    edge_connector_system_ip: Optional[str] = Field(alias="edgeConnectorSystemIp")
    edge_connector_enable: Optional[bool] = Field(alias="edgeConnectorEnable")
    v_smarts: List[str] = Field(alias="vSmarts", default=[])
    old_idp_map: Optional[str] = Field(alias="oldIdpMap")
    created_at: Optional[int] = Field(alias="createdAt")
    rid: Optional[int] = Field(alias="@rid")
    edge_connector_tunnel_interface_name: Optional[str] = Field(alias="edgeConnectorTunnelInterfaceName")
    name: Optional[str]
    tenant_id: Optional[str] = Field(alias="tenantId")
    wan_edge_forecast: Optional[str] = Field(alias="wanEdgeForecast")
    sp_metadata: Optional[str] = Field(alias="spMetadata")
    state: Optional[str]
    wan_edge_present: Optional[int] = Field(alias="wanEdgePresent")
    desc: Optional[str]


class MultitenantAPIsProviderAPI(APIPrimitiveBase):
    def create_tenant(self):
        # POST /tenant
        ...

    def create_tenant_async(self):
        # POST /tenant/async
        ...

    def create_tenant_async_bulk(self):
        # POST /tenant/bulk/async
        ...

    def delete_tenant(self):
        # POST /tenant/{tenantId}/delete
        ...

    def delete_tenant_async_bulk(self):
        # DELETE /tenant/bulk/async
        ...

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

    def get_all_tenant_statuses(self):
        # GET /tenantstatus
        ...

    def get_all_tenants(self) -> DataSequence[Tenant]:
        return self.get("/tenant").dataseq(Tenant)

    def get_tenant(self):
        # GET /tenant/{tenantId}
        ...

    def get_tenant_hosting_capacity_onv_smarts(self):
        # GET /tenant/vsmart/capacity
        ...

    def get_tenantv_smart_mapping(self):
        # GET /tenant/vsmart
        ...

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

    def update_tenantv_smart_placement(self):
        # PUT /tenant/{tenantId}/vsmart
        ...

    def v_session_id(self):
        # POST /tenant/{tenantId}/vsessionid
        ...
