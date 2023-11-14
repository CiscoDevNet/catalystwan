import datetime
from enum import Enum
from typing import Any, List, Optional, Protocol, Sequence, Union

from pydantic.v1 import BaseModel, Field, IPvAnyNetwork
from typing_extensions import Annotated, Literal

from vmngclient.typed_list import DataSequence

# TODO: add validators for custom strings (eg.: port ranges, space separated networks)
# TODO: model actions


class ListReference(BaseModel):
    ref: str


class VariableName(BaseModel):
    vip_variable_name: str = Field(alias="vipVariableName")


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
    PASS = "pass"
    INSPECT = "inspect"


class SequenceType(str, Enum):
    APPLICATION_FIREWALL = "applicationFirewall"
    DATA = "data"
    SERVICE_CHAINING = "serviceChaining"
    TRAFFIC_ENGINEERING = "trafficEngineering"
    QOS = "qos"
    ZONE_BASED_FW = "zoneBasedFW"


class Optimized(str, Enum):
    TRUE = "true"
    FALSE = "false"


class PacketLengthEntry(BaseModel):
    field: Literal["packetLength"] = "packetLength"
    value: str = Field(description="0-65536 range or single number")


class PLPEntry(BaseModel):
    field: Literal["plp"] = "plp"
    value: PLPEntryValues


class ProtocolEntry(BaseModel):
    field: Literal["protocol"] = "protocol"
    value: str = Field(description="0-255 single numbers separate by space")


class DSCPEntry(BaseModel):
    field: Literal["dscp"] = "dscp"
    value: str = Field(description="0-63 single numbers separate by space")


class SourceIPEntry(BaseModel):
    field: Literal["sourceIp"] = "sourceIp"
    value: str = Field(description="IP network specifier separate by space")


class SourcePortEntry(BaseModel):
    field: Literal["sourcePort"] = "sourcePort"
    value: str = Field(description="0-65535 range or separate by space")


class DestinationIPEntry(BaseModel):
    field: Literal["destinationIp"] = "destinationIp"
    value: IPvAnyNetwork


class DestinationPortEntry(BaseModel):
    field: Literal["destinationPort"] = "destinationPort"
    value: str = Field(description="0-65535 range or separate by space")


class TCPEntry(BaseModel):
    field: Literal["tcp"] = "tcp"
    value: Literal["syn"] = "syn"


class DNSEntry(BaseModel):
    field: Literal["dns"] = "dns"
    value: DNSEntryValues


class TrafficToEntry(BaseModel):
    field: Literal["trafficTo"] = "trafficTo"
    value: TrafficToEntryValues


class DestinationRegionEntry(BaseModel):
    field: Literal["destinationRegion"] = "destinationRegion"
    value: DestinationRegionEntryValues


class SourceFQDNEntry(BaseModel):
    field: Literal["sourceFqdn"] = "sourceFqdn"
    value: str = Field(max_length=120)


class DestinationFQDNEntry(BaseModel):
    field: Literal["destinationFqdn"] = "destinationFqdn"
    value: str = Field(max_length=120)


class SourceGeoLocationEntry(BaseModel):
    field: Literal["sourceGeoLocation"] = "sourceGeoLocation"
    value: str = Field(description="Space separated list of ISO3166 country codes")


class DestinationGeoLocationEntry(BaseModel):
    field: Literal["destinationGeoLocation"] = "destinationGeoLocation"
    value: str = Field(description="Space separated list of ISO3166 country codes")


class SourceDataPrefixListEntry(BaseModel):
    field: Literal["sourceDataPrefixList"]
    ref: str


class DestinationDataPrefixListEntry(BaseModel):
    field: Literal["destinationDataPrefixList"] = "destinationDataPrefixList"
    ref: str


class SourceDataIPv6PrefixListEntry(BaseModel):
    field: Literal["sourceDataIpv6PrefixList"] = "sourceDataIpv6PrefixList"
    ref: str


class DestinationDataIPv6PrefixListEntry(BaseModel):
    field: Literal["destinationDataIpv6PrefixList"] = "destinationDataIpv6PrefixList"
    ref: str


class DNSAppListEntry(BaseModel):
    field: Literal["dnsAppList"] = "dnsAppList"
    ref: str


class AppListEntry(BaseModel):
    field: Literal["appList"] = "appList"
    ref: str


class SourceFQDNListEntry(BaseModel):
    field: Literal["sourceFqdnList"] = "sourceFqdnList"
    ref: str


class DestinationFQDNListEntry(BaseModel):
    field: Literal["destinationFqdnList"] = "destinationFqdnList"
    ref: str


class SourceGeoLocationListEntry(BaseModel):
    field: Literal["sourceGeoLocationList"] = "sourceGeoLocationList"
    ref: str


class DestinationGeoLocationListEntry(BaseModel):
    field: Literal["destinationGeoLocationList"] = "destinationGeoLocationList"
    ref: str


class ProtocolNameListEntry(BaseModel):
    field: Literal["protocolNameList"] = "protocolNameList"
    ref: str


class SourcePortListEntry(BaseModel):
    field: Literal["sourcePortList"] = "sourcePortList"
    ref: str


class DestinationPortListEntry(BaseModel):
    field: Literal["destinationPortList"] = "destinationPortList"
    ref: str


class RuleSetListEntry(BaseModel):
    field: Literal["ruleSetList"] = "ruleSetList"
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
        SourceFQDNEntry,
        DestinationFQDNEntry,
        SourceGeoLocationEntry,
        DestinationGeoLocationEntry,
        SourceDataPrefixListEntry,
        DestinationDataPrefixListEntry,
        SourceDataIPv6PrefixListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationRegionEntry,
        DNSAppListEntry,
        AppListEntry,
        SourceFQDNListEntry,
        DestinationFQDNListEntry,
        SourceGeoLocationListEntry,
        DestinationGeoLocationListEntry,
        SourcePortListEntry,
        DestinationPortListEntry,
        ProtocolNameListEntry,
    ],
    Field(discriminator="field"),
]


class Match(BaseModel):
    entries: Sequence[Entry]


class Action(BaseModel):
    pass


class DefinitionSequence(BaseModel):
    sequence_id: int = Field(alias="sequenceId")
    sequence_name: str = Field(alias="sequenceName")
    base_action: BaseAction = Field(default=BaseAction.DROP, alias="baseAction")
    sequence_type: SequenceType = Field(alias="sequenceType")
    sequence_ip_type: SequenceIpType = Field(alias="sequenceIpType")
    ruleset: Optional[bool] = None
    match: Match
    actions: List[Any] = []


class DefaultAction(BaseModel):
    type: DefaultActionType


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", alias="infoTag")


class PolicyDefinitionId(BaseModel):
    definition_id: str = Field(alias="definitionId")


class PolicyReference(BaseModel):
    id: str
    property: str


class PolicyDefinitionHeader(BaseModel):
    name: str = Field(
        regex="^[a-zA-Z0-9_-]{1,128}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 128 characters",
    )
    description: str
    type: str
    mode: Optional[str] = None
    optimized: Optional[Optimized] = Optimized.FALSE


class PolicyDefinitionInfo(PolicyDefinitionHeader):
    last_updated: datetime.datetime = Field(alias="lastUpdated")
    owner: str
    reference_count: int = Field(alias="referenceCount")
    references: List[PolicyReference]


class PolicyDefinitionBody(BaseModel):
    default_action: Optional[DefaultAction] = Field(
        default=DefaultAction(type=DefaultActionType.DROP), alias="defaultAction"
    )
    sequences: Sequence[DefinitionSequence] = []


class PolicyDefinitionCreationPayload(PolicyDefinitionHeader):
    definition: PolicyDefinitionBody


class PolicyDefinitionGetResponse(PolicyDefinitionCreationPayload, PolicyDefinitionId):
    is_activated_by_vsmart: bool = Field(alias="isActivatedByVsmart")


class PolicyDefinitionEditPayload(PolicyDefinitionCreationPayload, PolicyDefinitionId):
    pass


class PolicyDefinitionEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(default=[], alias="masterTemplatesAffected")


class PolicyDefinitionPreview(BaseModel):
    preview: str


class PolicyDefinitionBuilder(Protocol):
    def create_policy_definition(self, payload: BaseModel) -> PolicyDefinitionId:
        ...

    def delete_policy_definition(self, id: str) -> None:
        ...

    def edit_policy_definition(self, id: str, payload: BaseModel) -> PolicyDefinitionEditResponse:
        ...

    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    def get_policy_definition(self, id: str) -> PolicyDefinitionGetResponse:
        ...
