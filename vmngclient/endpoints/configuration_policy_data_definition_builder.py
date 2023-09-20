# mypy: disable-error-code="empty-body"
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, IPvAnyNetwork
from typing_extensions import Annotated, Literal

from vmngclient.endpoints import APIEndpoints, delete, get, post, put
from vmngclient.model.policy_definition import (
    PolicyDefinition,
    PolicyDefinitionCreationPayload,
    PolicyDefinitionEditPayload,
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionPreview,
)
from vmngclient.typed_list import DataSequence

# TODO: add validators for custom strings (eg.: port ranges, space separated networks)
# TODO: model actions


class DefaultActionType(str, Enum):
    DROP = "drop"
    ACCEPT = "accept"


class PLPEntryValues(str, Enum):
    LOW = "low"
    HIGH = "high"


class DNSEntryValues(str, Enum):
    REQUEST = "request"
    RESPONSE = "response"


class TrafficToEntryValues(str, Enum):
    ACCESS = "access"
    CORE = "core"
    SERVICE = "service"


class DestinationRegionEntryValues(str, Enum):
    PRIMARY = "primary-region"
    SECONDARY = "secondary-region"
    OTHER = "other-region"


class SequenceIpType(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    ALL = "all"


class BaseAction(str, Enum):
    DROP = "drop"
    ACCEPT = "accept"


class SequenceType(str, Enum):
    APPLICATION_FIREWALL = "applicationFirewall"
    DATA = "data"
    SERVICE_CHAINING = "serviceChaining"
    TRAFFIC_ENGINEERING = "trafficEngineering"
    QOS = "qos"


class PacketLengthEntry(BaseModel):
    field: Literal["packetLength"]
    value: str = Field(description="0-65536 range or single number")


class PLPEntry(BaseModel):
    field: Literal["plp"]
    value: PLPEntryValues


class ProtocolEntry(BaseModel):
    field: Literal["protocol"]
    value: str = Field(description="0-255 single numbers separate by space")


class DSCPEntry(BaseModel):
    field: Literal["dscp"]
    value: str = Field(description="0-63 single numbers separate by space")


class SourceIPEntry(BaseModel):
    field: Literal["sourceIp"]
    value: str = Field(description="IP network specifier separate by space")


class SourcePortEntry(BaseModel):
    field: Literal["sourcePort"]
    value: str = Field(description="0-65535 range or separate by space")


class DestinationIPEntry(BaseModel):
    field: Literal["destinationIp"]
    value: IPvAnyNetwork


class DestinationPortEntry(BaseModel):
    field: Literal["destinationPort"]
    value: str = Field(description="0-65535 range or separate by space")


class TCPEntry(BaseModel):
    field: Literal["tcp"]
    value: Literal["syn"]


class DNSEntry(BaseModel):
    field: Literal["dns"]
    value: DNSEntryValues


class TrafficToEntry(BaseModel):
    field: Literal["trafficTo"]
    value: TrafficToEntryValues


class DestinationRegionEntry(BaseModel):
    field: Literal["destinationRegion"]
    value: DestinationRegionEntryValues


class SourceDataPrefixListEntry(BaseModel):
    field: Literal["sourceDataPrefixList"]
    ref: str


class DestinationDataPrefixListEntry(BaseModel):
    field: Literal["destinationDataPrefixList"]
    ref: str


class SourceDataIPv6PrefixListEntry(BaseModel):
    field: Literal["sourceDataIpv6PrefixList"]
    ref: str


class DestinationDataIPv6PrefixListEntry(BaseModel):
    field: Literal["destinationDataIpv6PrefixList"]
    ref: str


class DNSAppListEntry(BaseModel):
    field: Literal["dnsAppList"]
    ref: str


class AppListEntry(BaseModel):
    field: Literal["appList"]
    ref: str


Entry = Annotated[
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


class Match(BaseModel):
    entries: List[Entry]


class Action(BaseModel):
    pass


class Sequence(BaseModel):
    sequence_id: int = Field(alias="sequenceId")
    sequence_name: str = Field(alias="sequenceName")
    base_action: BaseAction = Field(alias="baseAction")
    sequence_type: SequenceType = Field(alias="sequenceType")
    sequence_ip_type: SequenceIpType = Field(alias="sequenceIpType")
    match: Match
    actions: List[Any]


class DefaultAction(BaseModel):
    type: DefaultActionType


class Data(BaseModel):
    type: str = Field(default="data", const=True)
    default_action: Optional[DefaultAction] = Field(
        default=DefaultAction(type=DefaultActionType.DROP), alias="defaultAction"
    )
    is_activated_by_vsmart: Optional[bool] = Field(default=False, alias="isActivatedByVsmart")
    sequences: List[Sequence] = []


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
