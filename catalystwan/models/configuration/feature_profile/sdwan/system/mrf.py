from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

EnableMrfMigration = Literal["enabled", "enabled-from-bgp-core"]
Role = Literal["edge-router", "border-router"]


class ManagementRegion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    vrf_id: Optional[Union[Global[int], Default[None], Variable]] = Field(
        None, serialization_alias="vrfId", validation_alias="vrfId", description="VRF name for management region"
    )
    gateway_preference: Optional[Union[Global[List[int]], Default[None], Variable]] = Field(
        None,
        serialization_alias="gatewayPreference",
        validation_alias="gatewayPreference",
        description="List of affinity group preferences for VRF",
    )
    management_gateway: Optional[Union[Global[bool], Default[Literal[False]], Variable]] = Field(
        None,
        serialization_alias="managementGateway",
        validation_alias="managementGateway",
        description="Enable management gateway",
    )


class MRFParcel(_ParcelBase):
    type_: Literal["mrf"] = Field(default="mrf", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
    )
    secondary_region: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        None,
        serialization_alias="secondaryRegion",
        validation_alias="secondaryRegion",
        description="Set secondary region ID",
    )
    role: Optional[Union[Global[Role], Variable, Default[None]]] = Field(None, description="Set the role for router")
    enable_mrf_migration: Optional[Union[Global[EnableMrfMigration], Default[None]]] = Field(
        None,
        serialization_alias="enableMrfMigration",
        validation_alias="enableMrfMigration",
        description="Enable migration mode to Multi-Region Fabric",
    )
    migration_bgp_community: Optional[Union[Global[int], Default[None]]] = Field(
        None,
        serialization_alias="migrationBgpCommunity",
        validation_alias="migrationBgpCommunity",
        description="Set BGP community during migration from BGP-core based network",
    )
    enable_management_region: Optional[Union[Global[bool], Default[Literal[False]], Variable]] = Field(
        None,
        serialization_alias="enableManagementRegion",
        validation_alias="enableManagementRegion",
        description="Enable management region",
    )
    management_region: Optional[ManagementRegion] = Field(
        None,
        serialization_alias="managementRegion",
        validation_alias="managementRegion",
        description="Management Region",
    )
