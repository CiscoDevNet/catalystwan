# mypy: disable-error-code="empty-body"
from typing import List, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    DefaultAction,
    DefaultActionType,
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
    PolicyDefinition,
    PolicyDefinitionCreationPayload,
    PolicyDefinitionEditPayload,
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
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


class Data(BaseModel):
    type: str = Field(default="data", const=True)
    default_action: Optional[DefaultAction] = Field(
        default=DefaultAction(type=DefaultActionType.DROP), alias="defaultAction"
    )
    is_activated_by_vsmart: Optional[bool] = Field(default=False, alias="isActivatedByVsmart")
    sequences: List[DataPolicySequenceEntry] = []


class DataDefinitionCreationPayload(Data, PolicyDefinitionCreationPayload):
    pass


class DataDefinitionEditPayload(Data, PolicyDefinitionEditPayload):
    pass


class DataDefinition(Data, PolicyDefinition):
    pass


class ConfigurationPolicyDataDefinitionBuilder(APIEndpoints):
    @post("/template/policy/definition/data")
    def create_policy_definition(self, payload: DataDefinitionCreationPayload) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/data/{id}")
    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/data/multiple/{id}
        ...

    @put("/template/policy/definition/data/{id}")
    def edit_policy_definition(self, id: str, payload: DataDefinitionEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/data", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinition]:
        ...

    @get("/template/policy/definition/data/{id}")
    def get_policy_definition(self, id: str) -> DataDefinition:
        ...

    @post("/template/policy/definition/data/preview")
    def preview_policy_definition(self, payload: DataDefinitionCreationPayload) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/data/preview/{id}")
    def preview_policy_definition_by_id(self, id: str) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/data/bulk
        ...
