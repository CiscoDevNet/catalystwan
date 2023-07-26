from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import IPvAnyAddress

from vmngclient.utils.pydantic import BaseModel, Field


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
    desc: str
    org_name: str = Field(alias="orgName")
    subdomain: str = Field(alias="subDomain")
    flake_id: Optional[int] = Field(alias="flakeId", default=None)
    vbond_address: Optional[str] = Field(alias="vBondAddress", default=None)
    edge_connector_system_ip: Optional[str] = Field(alias="edgeConnectorSystemIp", default=None)
    edge_connector_enable: Optional[bool] = Field(alias="edgeConnectorEnable", default=None)
    vsmarts: Optional[List[str]] = Field(alias="vSmarts", default=None)
    wan_edge_forecast: Optional[int] = Field(alias="wanEdgeForecast", default=None)
    saml_sp_info: Optional[str] = Field(alias="samlSpInfo", default=None)
    idp_map: Union[Dict, str, None] = Field(alias="idpMap", default=None)
    config_db_cluster_service_name: Optional[str] = Field(alias="configDBClusterServiceName", default=None)
    old_idp_map: Union[Dict, str, None] = Field(alias="oldIdpMap", default=None)
    created_at: Optional[datetime] = Field(alias="createdAt", default=None)
    rid: Optional[int] = Field(alias="@rid", default=None)
    edge_connector_tunnel_interface_name: Optional[str] = Field(alias="edgeConnectorTunnelInterfaceName", default=None)
    tenant_id: Optional[str] = Field(alias="tenantId", default=None)
    sp_metadata: Optional[str] = Field(alias="spMetadata", default=None)
    state: Optional[str] = None
    wan_edge_present: Optional[int] = Field(alias="wanEdgePresent", default=None)
    mt_edge: Optional[List[MTEdge]] = Field(alias="mtEdge", default=None)
    mt_edge_count: Optional[int] = Field(alias="mtEdgeCount", default=None)
    tenant_vpn_map: Optional[List[TenantVPNMap]] = Field(alias="tenantVPNmap", default=None)
    tenant_provider_vpn_count: Optional[int] = Field(alias="tenantProviderVPNCount", default=None)
