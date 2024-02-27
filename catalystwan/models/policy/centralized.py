# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union, overload
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Annotated

from catalystwan.models.policy.policy import (
    AssemblyItemBase,
    PolicyCreationPayload,
    PolicyDefinition,
    PolicyEditPayload,
    PolicyInfo,
)

TrafficDataDirection = Literal[
    "service",
    "tunnel",
    "all",
]

ControlDirection = Literal[
    "in",
    "out",
]


class DataApplicationEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    direction: TrafficDataDirection = "service"
    site_lists: Optional[List[UUID]] = Field(
        default=None, serialization_alias="siteLists", validation_alias="siteLists"
    )
    vpn_lists: List[UUID] = Field(default=[], serialization_alias="vpnLists", validation_alias="vpnLists")
    region_ids: Optional[List[str]] = Field(default=None, serialization_alias="regionIds", validation_alias="regionIds")
    region_lists: Optional[List[UUID]] = Field(
        default=None, serialization_alias="regionLists", validation_alias="regionLists"
    )

    # def apply_site_list(self, site_list_id: UUID):
    #     self.site_lists.append(site_list_id)

    # def apply_vpn_list(self, vpn_list_id: UUID):
    #     self.vpn_lists.append(vpn_list_id)


class ControlApplicationEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    direction: ControlDirection
    site_lists: Optional[List[UUID]] = Field(
        default=None, serialization_alias="siteLists", validation_alias="siteLists"
    )
    region_lists: Optional[List[UUID]] = Field(
        default=None, serialization_alias="regionLists", validation_alias="regionLists"
    )
    region_ids: Optional[List[str]] = Field(default=None, serialization_alias="regionIds", validation_alias="regionIds")


class ControlPolicyItem(AssemblyItemBase):
    type: Literal["control"] = "control"
    entries: List[ControlApplicationEntry] = []

    def assign_to_inbound_sites(self, site_lists: List[UUID]) -> None:
        entry = ControlApplicationEntry(direction="in", site_lists=site_lists)
        self.entries.append(entry)

    def assign_to_outbound_sites(self, site_lists: List[UUID]) -> None:
        entry = ControlApplicationEntry(direction="in", site_lists=site_lists)
        self.entries.append(entry)

    @overload
    def assign_to_inbound_regions(self, *, region_ids: List[int]) -> None:
        ...

    @overload
    def assign_to_inbound_regions(self, *, region_lists: List[UUID]) -> None:
        ...

    def assign_to_inbound_regions(
        self, *, region_ids: Optional[List[int]] = None, region_lists: Optional[List[UUID]] = None
    ) -> None:
        _region_ids = [str(rid) for rid in region_ids] if region_ids else None
        entry = entry = ControlApplicationEntry(direction="in", region_ids=_region_ids, region_lists=region_lists)
        self.entries.append(entry)

    @overload
    def assign_to_outbound_regions(self, *, region_ids: List[int]) -> None:
        ...

    @overload
    def assign_to_outbound_regions(self, *, region_lists: List[UUID]) -> None:
        ...

    def assign_to_outbound_regions(
        self, *, region_ids: Optional[List[int]] = None, region_lists: Optional[List[UUID]] = None
    ) -> None:
        _region_ids = [str(rid) for rid in region_ids] if region_ids else None
        entry = entry = ControlApplicationEntry(direction="out", region_ids=_region_ids, region_lists=region_lists)
        self.entries.append(entry)


class TrafficDataPolicyItem(AssemblyItemBase):
    type: Literal["data"] = "data"
    entries: List[DataApplicationEntry] = []

    @overload
    def assign_to(
        self,
        vpn_lists: List[UUID],
        direction: TrafficDataDirection = "service",
        *,
        site_lists: List[UUID],
    ) -> None:
        ...

    @overload
    def assign_to(
        self,
        vpn_lists: List[UUID],
        direction: TrafficDataDirection = "service",
        *,
        region_lists: List[UUID],
    ) -> None:
        ...

    @overload
    def assign_to(
        self,
        vpn_lists: List[UUID],
        direction: TrafficDataDirection = "service",
        *,
        region_ids: List[int],
    ) -> None:
        ...

    def assign_to(
        self,
        vpn_lists: List[UUID],
        direction: TrafficDataDirection = "service",
        *,
        site_lists: Optional[List[UUID]] = None,
        region_lists: Optional[List[UUID]] = None,
        region_ids: Optional[List[int]] = None,
    ) -> None:
        entry = DataApplicationEntry(
            direction=direction,
            site_lists=site_lists,
            vpn_lists=vpn_lists,
            region_lists=region_lists,
            region_ids=[str(rid) for rid in region_ids] if region_ids else None,
        )
        self.entries.append(entry)


class HubAndSpokePolicyItem(AssemblyItemBase):
    type: Literal["hubAndSpoke"] = "hubAndSpoke"


class MeshPolicyItem(AssemblyItemBase):
    type: Literal["mesh"] = "mesh"


AnyAssemblyItem = Annotated[
    Union[
        TrafficDataPolicyItem,
        ControlPolicyItem,
        MeshPolicyItem,
        HubAndSpokePolicyItem,
    ],
    Field(discriminator="type"),
]


class CentralizedPolicyDefinition(PolicyDefinition):
    region_role_assembly: List = Field(
        default=[], serialization_alias="regionRoleAssembly", validation_alias="regionRoleAssembly"
    )
    assembly: List[AnyAssemblyItem] = []
    model_config = ConfigDict(populate_by_name=True)


class CentralizedPolicy(PolicyCreationPayload):
    policy_definition: CentralizedPolicyDefinition = Field(
        default=CentralizedPolicyDefinition(),
        serialization_alias="policyDefinition",
        validation_alias="policyDefinition",
    )
    policy_type: Literal["feature"] = Field(
        default="feature", serialization_alias="policyType", validation_alias="policyType"
    )

    def add_traffic_data_policy(self, traffic_data_policy_id: UUID) -> TrafficDataPolicyItem:
        item = TrafficDataPolicyItem(definition_id=traffic_data_policy_id)
        self.policy_definition.assembly.append(item)
        return item

    def add_control_policy(self, control_policy_id: UUID) -> ControlPolicyItem:
        item = ControlPolicyItem(definition_id=control_policy_id)
        self.policy_definition.assembly.append(item)
        return item

    def add_mesh_policy(self, mesh_policy_id: UUID) -> None:
        self.policy_definition.assembly.append(MeshPolicyItem(definition_id=mesh_policy_id))

    def add_hub_and_spoke_policy(self, hub_and_spoke_policy_id: UUID) -> None:
        self.policy_definition.assembly.append(HubAndSpokePolicyItem(definition_id=hub_and_spoke_policy_id))

    @field_validator("policy_definition", mode="before")
    @classmethod
    def try_parse(cls, policy_definition):
        # this is needed because GET /template/policy/vsmart contains string in policyDefinition field
        # while POST /template/policy/vsmart requires a regular object
        # it makes sense to reuse that model for both requests and present parsed data to the user
        if isinstance(policy_definition, str):
            return CentralizedPolicyDefinition.parse_raw(policy_definition)
        return policy_definition


class CentralizedPolicyEditPayload(PolicyEditPayload, CentralizedPolicy):
    rid: Optional[str] = Field(default=None, serialization_alias="@rid", validation_alias="@rid")


class CentralizedPolicyInfo(PolicyInfo, CentralizedPolicyEditPayload):
    pass
