# mypy: disable-error-code="empty-body"
from typing import List, Optional, Union

from pydantic import Field
from typing_extensions import Annotated

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    DefinitionSequence,
    DestinationDataIPv6PrefixListEntry,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationRegionEntry,
    DNSAppListEntry,
    DNSEntry,
    DSCPEntry,
    PacketLengthEntry,
    PLPEntry,
    PolicyDefinitionBody,
    PolicyDefinitionEditResponse,
    PolicyDefinitionHeader,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
    ProtocolEntry,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    TCPEntry,
    TrafficToEntry,
)
from vmngclient.typed_list import DataSequence

DataPolicySequenceEntry = Annotated[
    Union[
        PacketLengthEntry,
        PLPEntry,
        ProtocolEntry,
        DSCPEntry,
        SourceIPEntry,
        SourcePortEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        TCPEntry,
        DNSEntry,
        TrafficToEntry,
        SourceDataPrefixListEntry,
        DestinationDataPrefixListEntry,
        SourceDataIPv6PrefixListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationRegionEntry,
        DNSAppListEntry,
        AppListEntry,
    ],
    Field(discriminator="field"),
]


class DataPolicySequence(DefinitionSequence):
    type: str = Field(default="data", const=True)
    entries: List[DataPolicySequenceEntry]


class DataPolicy(PolicyDefinitionHeader):
    type: str = Field(default="data", const=True)


class DataPolicyDefinition(PolicyDefinitionBody):
    sequences: List[DataPolicySequence] = []


class DataPolicyCreationPayload(DataPolicy):
    definition: Optional[DataPolicyDefinition] = None


class DataPolicyGetResponse(DataPolicyCreationPayload, PolicyDefinitionId):
    pass


class DataPolicyEditPayload(DataPolicyCreationPayload, PolicyDefinitionId):
    pass


class DataPolicyInfo(DataPolicy, PolicyDefinitionInfo):
    pass


class ConfigurationPolicyDataDefinitionBuilder(APIEndpoints):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: DataPolicyCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/data/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    @put("/template/policy/definition/data/{id}")
    def edit_policy_definition(self, id: str, payload: DataPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: str) -> DataPolicyGetResponse:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: DataPolicyCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/data/bulk
        ...
