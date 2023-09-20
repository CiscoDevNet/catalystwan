from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress


class MTEdge(BaseModel):
    uuid: str
    configured_hostname: Optional[str] = Field(None, alias="configuredHostname")
    configured_system_ip: Optional[IPvAnyAddress] = Field(None, alias="configuredSystemIP")
    management_system_ip: Optional[IPvAnyAddress] = Field(None, alias="managementSystemIP")
    device_model: Optional[str] = Field(None, alias="deviceModel")
    device_type: Optional[str] = Field(None, alias="deviceType")


class TenantVPNMap(BaseModel):
    tenant_vpn: int = Field(alias="tenantVPN")
    device_vpn: int = Field(alias="deviceVPN")


class Tenant(BaseModel):
    name: str
    desc: str
    org_name: str = Field(alias="orgName")
    subdomain: str = Field(alias="subDomain")
    flake_id: Optional[int] = Field(None, alias="flakeId")
    vbond_address: Optional[str] = Field(None, alias="vBondAddress")
    edge_connector_system_ip: Optional[str] = Field(None, alias="edgeConnectorSystemIp")
    edge_connector_enable: Optional[bool] = Field(None, alias="edgeConnectorEnable")
    vsmarts: Optional[List[str]] = Field(None, alias="vSmarts")
    wan_edge_forecast: Optional[int] = Field(None, alias="wanEdgeForecast")
    saml_sp_info: Optional[str] = Field(None, alias="samlSpInfo")
    idp_map: Union[Dict, str, None] = Field(None, alias="idpMap")
    config_db_cluster_service_name: Optional[str] = Field(None, alias="configDBClusterServiceName")
    old_idp_map: Union[Dict, str, None] = Field(None, alias="oldIdpMap")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    rid: Optional[int] = Field(None, alias="@rid")
    edge_connector_tunnel_interface_name: Optional[str] = Field(None, alias="edgeConnectorTunnelInterfaceName")
    tenant_id: Optional[str] = Field(None, alias="tenantId")
    sp_metadata: Optional[str] = Field(None, alias="spMetadata")
    state: Optional[str] = None
    wan_edge_present: Optional[int] = Field(None, alias="wanEdgePresent")
    mt_edge: Optional[List[MTEdge]] = Field(None, alias="mtEdge")
    mt_edge_count: Optional[int] = Field(None, alias="mtEdgeCount")
    tenant_vpn_map: Optional[List[TenantVPNMap]] = Field(None, alias="tenantVPNmap")
    tenant_provider_vpn_count: Optional[int] = Field(None, alias="tenantProviderVPNCount")
    model_config = ConfigDict(populate_by_name=True)


class MigrationTenant(Tenant):
    is_destination_overlay_mt: Optional[bool] = Field(None, alias="isDestinationOverlayMT")
