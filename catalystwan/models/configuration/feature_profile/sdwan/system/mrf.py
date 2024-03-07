from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

EnableMrfMigration = Literal["enabled", "enabled-from-bgp-core"]
Role = Literal["edge-router", "border-router"]


class ManagementRegion(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    vrf_id: Union[Global[int], Default[None], Variable] = Field(
        default=Default[None](value=None),
        serialization_alias="vrfId",
        validation_alias="vrfId",
        description="VRF name for management region",
    )
    gateway_preference: Optional[Union[Global[List[int]], Default[None], Variable]] = Field(
        default=Default[None](value=None),
        serialization_alias="gatewayPreference",
        validation_alias="gatewayPreference",
        description="List of affinity group preferences for VRF",
    )
    management_gateway: Union[Global[bool], Default[bool], Variable] = Field(
        default=as_default(False),
        serialization_alias="managementGateway",
        validation_alias="managementGateway",
        description="Enable management gateway",
    )


class MRFParcel(_ParcelBase):
    type_: Literal["mrf"] = Field(default="mrf", exclude=True)

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    secondary_region: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "secondaryRegion"),
        description="Set secondary region ID",
    )
    role: Union[Global[Role], Variable, Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "role"),
        description="Set the role for router",
    )
    enable_mrf_migration: Union[Global[EnableMrfMigration], Default[None]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "enableMrfMigration"),
        description="Enable migration mode to Multi-Region Fabric",
    )
    migration_bgp_community: Optional[Union[Global[int], Default[None]]] = Field(
        default=Default[None](value=None),
        validation_alias=AliasPath("data", "migrationBgpCommunity"),
        description="Set BGP community during migration from BGP-core based network",
    )
    enable_management_region: Union[Global[bool], Default[bool], Variable] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "enableManagementRegion"),
        description="Enable management region",
    )
    management_region: ManagementRegion = Field(
        default_factory=ManagementRegion,
        validation_alias=AliasPath("data", "managementRegion"),
        description="Management Region",
    )
