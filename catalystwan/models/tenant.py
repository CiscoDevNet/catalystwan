# Copyright 2023 Cisco Systems, Inc. and its affiliates

from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic.v1 import BaseModel, Field, IPvAnyAddress


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
    flake_id: Optional[int] = Field(alias="flakeId")
    vbond_address: Optional[str] = Field(alias="vBondAddress")
    edge_connector_system_ip: Optional[str] = Field(alias="edgeConnectorSystemIp")
    edge_connector_enable: Optional[bool] = Field(alias="edgeConnectorEnable")
    vsmarts: Optional[List[str]] = Field(alias="vSmarts")
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
    mt_edge: Optional[List[MTEdge]] = Field(alias="mtEdge")
    mt_edge_count: Optional[int] = Field(alias="mtEdgeCount")
    tenant_vpn_map: Optional[List[TenantVPNMap]] = Field(alias="tenantVPNmap")
    tenant_provider_vpn_count: Optional[int] = Field(alias="tenantProviderVPNCount")

    class Config:
        allow_population_by_field_name = True


class TenantExport(BaseModel):
    name: str
    desc: str
    org_name: str = Field(alias="orgName")
    subdomain: str = Field(alias="subDomain")
    wan_edge_forecast: Optional[int] = Field(alias="wanEdgeForecast")
    is_destination_overlay_mt: Optional[bool] = Field(
        alias="isDestinationOverlayMT", description="required starting from 20.13"
    )
    migration_key: Optional[str] = Field(
        alias="migrationKey", regex=r"^[a-zA-Z0-9]{8,32}$", description="required starting from 20.13"
    )

    class Config:
        allow_population_by_field_name = True
