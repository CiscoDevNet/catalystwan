# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
)


class Hub(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    site_list: UUID = Field(validation_alias="siteList", serialization_alias="siteList")
    preference: Optional[str] = None
    prefix_lists: List[UUID] = Field(default=[], validation_alias="prefixLists", serialization_alias="prefixLists")
    ipv6_prefix_lists: List[UUID] = Field(
        default=[], validation_alias="ipv6PrefixLists", serialization_alias="ipv6PrefixLists"
    )


class Spoke(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    site_list: UUID = Field(validation_alias="siteList", serialization_alias="siteList")
    hubs: List[Hub]


class HubAndSpokePolicySubDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = "My Hub-and-Spoke"
    equal_preference: bool = Field(
        default=True, validation_alias="equalPreference", serialization_alias="equalPreference"
    )
    advertise_tloc: bool = Field(default=False, validation_alias="advertiseTloc", serialization_alias="advertiseTloc")
    tloc_list: Optional[UUID] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    spokes: List[Spoke] = []


class HubAndSpokePolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    vpn_list: UUID = Field(validation_alias="vpnList", serialization_alias="vpnList")
    sub_definitions: List[HubAndSpokePolicySubDefinition] = Field(
        default=[], validation_alias="subDefinitions", serialization_alias="subDefinitions"
    )


class HubAndSpokePolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["hubAndSpoke"] = "hubAndSpoke"
    definition: HubAndSpokePolicyDefinition

    @staticmethod
    def from_vpn_list(name: str, vpn_list: UUID) -> "HubAndSpokePolicy":
        return HubAndSpokePolicy(name=name, definition=HubAndSpokePolicyDefinition(vpn_list=vpn_list))

    def add_hub_and_spoke(
        self,
        name: str,
        hub_site_lists: List[UUID],
        spoke_site_lists: List[UUID],
        advertise_tloc_list: Optional[UUID] = None,
    ) -> HubAndSpokePolicySubDefinition:
        # supports basic configuration with equal preference
        hubs = [Hub(site_list=hub_site_id) for hub_site_id in hub_site_lists]
        spokes = [Spoke(site_list=spoke_site_id, hubs=hubs.copy()) for spoke_site_id in spoke_site_lists]
        sub_definition = HubAndSpokePolicySubDefinition(
            name=name,
            equal_preference=True,
            advertise_tloc=(advertise_tloc_list is not None),
            tloc_list=advertise_tloc_list,
            spokes=spokes,
        )
        self.definition.sub_definitions.append(sub_definition)
        return sub_definition


class HubAndSpokePolicyEditPayload(HubAndSpokePolicy, PolicyDefinitionId):
    pass


class HubAndSpokePolicyGetResponse(HubAndSpokePolicy, PolicyDefinitionGetResponse):
    pass
