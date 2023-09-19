# mypy: disable-error-code="empty-body"
from typing import List, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    DefinitionSequence,
    DestinationDataPrefixListEntry,
    DestinationFQDNEntry,
    DestinationGeoLocationEntry,
    DestinationGeoLocationListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationPortListEntry,
    Match,
    PolicyDefinitionBody,
    PolicyDefinitionEditResponse,
    PolicyDefinitionHeader,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
    ProtocolEntry,
    ProtocolNameListEntry,
    SequenceType,
    SourceDataPrefixListEntry,
    SourceFQDNEntry,
    SourceFQDNListEntry,
    SourceGeoLocationEntry,
    SourceGeoLocationListEntry,
    SourceIPEntry,
    SourcePortEntry,
    SourcePortListEntry,
)
from vmngclient.typed_list import DataSequence

ZoneBasedFWPolicySequenceEntry = Annotated[
    Union[
        SourceFQDNListEntry,
        ProtocolEntry,
        SourceIPEntry,
        SourcePortEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        SourceFQDNEntry,
        DestinationFQDNEntry,
        SourceGeoLocationEntry,
        DestinationGeoLocationEntry,
        SourceDataPrefixListEntry,
        DestinationDataPrefixListEntry,
        SourceGeoLocationListEntry,
        DestinationGeoLocationListEntry,
        SourcePortListEntry,
        DestinationPortListEntry,
        ProtocolNameListEntry,
        AppListEntry,
    ],
    Field(discriminator="field"),
]


class ZoneBasedFWPolicyMatch(Match):
    entries: List[ZoneBasedFWPolicySequenceEntry]


class ZoneBasedFWPolicySequence(DefinitionSequence):
    sequence_type: SequenceType = Field(default=SequenceType.ZONE_BASED_FW, const=True, alias="sequenceType")
    match: ZoneBasedFWPolicyMatch


class ZoneBasedFWPolicyEntry(BaseModel):
    source_zone: str = Field(default="self", alias="sourceZone")
    destination_zone: str = Field(alias="destinationZone")


class ZoneBasedFWPolicy(PolicyDefinitionHeader):
    type: str = Field(default="zoneBasedFW", const=True)
    mode: str = Field(default="security", const=True)


class ZoneBasedFWPolicyDefinition(PolicyDefinitionBody):
    sequences: List[ZoneBasedFWPolicySequence] = []
    entries: List[ZoneBasedFWPolicyEntry]


class ZoneBasedFWPolicyCreationPayload(ZoneBasedFWPolicy):
    definition: ZoneBasedFWPolicyDefinition


class ZoneBasedFWPolicyGetResponse(ZoneBasedFWPolicyCreationPayload, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyEditPayload(ZoneBasedFWPolicyCreationPayload, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyInfo(ZoneBasedFWPolicy, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyZoneBasedFirewallDefinitionBuilder(APIEndpoints):
    @post("/template/policy/definition/zonebasedfw")
    def create_policy_definition(self, payload: ZoneBasedFWPolicyCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/zonebasedfw/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/zonebasedfw/multiple/{id}
        ...

    @put("/template/policy/definition/zonebasedfw/{id}")
    def edit_policy_definition(self, id: str) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/zonebasedfw", "data")
    def get_definitions(self) -> DataSequence[ZoneBasedFWPolicyInfo]:
        ...

    @get("/template/policy/definition/zonebasedfw/{id}")
    def get_policy_definition(self, id: str) -> ZoneBasedFWPolicyGetResponse:
        ...

    @post("/template/policy/definition/zonebasedfw/preview")
    def preview_policy_definition(self, payload: ZoneBasedFWPolicyCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/zonebasedfw/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/zonebasedfw/bulk
        ...
