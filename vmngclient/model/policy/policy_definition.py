import datetime
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, IPvAnyNetwork
from typing_extensions import Annotated, Literal

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


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyDefinitionId(BaseModel):
    definition_id: str = Field(alias="definitionId")


class PolicyReference(BaseModel):
    id: str
    property: str


class PolicyDefinitionCreationPayload(BaseModel):
    name: str = Field(
        regex="^[a-zA-Z0-9_-]{1,128}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 128 characters",
    )
    description: str
    type: str


class PolicyDefinitionEditPayload(PolicyDefinitionCreationPayload, PolicyDefinitionId):
    pass


class PolicyDefinitionEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class PolicyDefinition(PolicyDefinitionEditPayload, InfoTag):
    last_updated: datetime.datetime = Field(alias="lastUpdated")
    owner: str
    mode: str
    optimized: str
    reference_count: int = Field(alias="referenceCount")
    references: List[PolicyReference]


class PolicyDefinitionPreview(BaseModel):
    preview: str
