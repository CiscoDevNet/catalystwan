import datetime
from enum import Enum
from ipaddress import IPv4Network
from typing import Any, Dict, List, MutableSequence, Optional, Protocol, Sequence, Set, Tuple, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated, Literal

from vmngclient.model.misc.application_protocols import ApplicationProtocol
from vmngclient.typed_list import DataSequence

# TODO: add validators for custom strings (eg.: port ranges, space separated networks)
# TODO: model actions


def port_set_and_ranges_to_str(ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> str:
    if not ports and not port_ranges:
        raise ValueError("Non empty port set or port range list must be provided")
    ports_str = " ".join(f"{port_begin}-{port_end}" for port_begin, port_end in port_ranges)
    ports_str = " " if ports_str else ""
    ports_str += " ".join(str(p) for p in ports)
    return ports_str


def ipv4_networks_to_str(networks: List[IPv4Network]) -> str:
    return " ".join(str(net) for net in networks)


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
    app: Optional[str] = None

    @staticmethod
    def from_protocol_set(protocols: Set[int]) -> "ProtocolEntry":
        return ProtocolEntry(value=" ".join(str(p) for p in protocols))

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "ProtocolEntry":
        return ProtocolEntry(
            value=" ".join(p.protocol_as_string_of_numbers() for p in app_prots),
            app=" ".join(p.name for p in app_prots),
        )


class DSCPEntry(BaseModel):
    field: Literal["dscp"] = "dscp"
    value: str = Field(description="0-63 single numbers separate by space")


class SourceIPEntry(BaseModel):
    field: Literal["sourceIp"] = "sourceIp"
    value: str = Field(description="IP network specifier separate by space")

    @staticmethod
    def from_ipv4_networks(networks: List[IPv4Network]) -> "SourceIPEntry":
        return SourceIPEntry(value=ipv4_networks_to_str(networks))


class SourcePortEntry(BaseModel):
    field: Literal["sourcePort"] = "sourcePort"
    value: str = Field(description="0-65535 range or separate by space")

    @staticmethod
    def from_port_set_and_ranges(ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> "SourcePortEntry":
        return SourcePortEntry(value=port_set_and_ranges_to_str(ports, port_ranges))


class DestinationIPEntry(BaseModel):
    field: Literal["destinationIp"] = "destinationIp"
    value: str

    @staticmethod
    def from_ipv4_networks(networks: List[IPv4Network]) -> "DestinationIPEntry":
        return DestinationIPEntry(value=ipv4_networks_to_str(networks))


class DestinationPortEntry(BaseModel):
    field: Literal["destinationPort"] = "destinationPort"
    value: str = Field(description="0-65535 range or separate by space")
    app: Optional[str] = None

    @staticmethod
    def from_port_set_and_ranges(
        ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []
    ) -> "DestinationPortEntry":
        return DestinationPortEntry(value=port_set_and_ranges_to_str(ports, port_ranges))

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "DestinationPortEntry":
        return DestinationPortEntry(
            value=" ".join(p.port for p in app_prots if p.port),
            app=" ".join(p.name for p in app_prots),
        )


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


class ProtocolNameEntry(BaseModel):
    field: Literal["protocolName"] = "protocolName"
    value: str

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "ProtocolNameEntry":
        return ProtocolNameEntry(value=" ".join(p.name for p in app_prots))


class SourceDataPrefixListEntry(BaseModel):
    field: Literal["sourceDataPrefixList"] = "sourceDataPrefixList"
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

    @staticmethod
    def with_rule_set_ids(rule_set_ids: Set[str]) -> "RuleSetListEntry":
        return RuleSetListEntry(ref=" ".join(rule_set_ids))


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
        ProtocolNameEntry,
        RuleSetListEntry,
    ],
    Field(discriminator="field"),
]

MUTUALLY_EXCLUSIVE_MATCH_FIELDS = [
    {"destinationDataPrefixList", "destinationIp"},
    {"sourceDataPrefixList", "sourceIp"},
    {"protocolName", "protocolNameList", "protocol", "destinationPort", "destinationPortList"},
]


def generate_field_name_check_lookup(spec: Sequence[Set[str]]) -> Dict[str, List[str]]:
    lookup: Dict[str, List[str]] = {}
    for exclusive_set in spec:
        for field in exclusive_set:
            lookup[field] = list(exclusive_set - {field})
    return lookup


MUTUALLY_EXCLUSIVE_MATCH_FIELD_LOOKUP = generate_field_name_check_lookup(MUTUALLY_EXCLUSIVE_MATCH_FIELDS)


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

    def insert_match(self, match: Entry, insert_field_check: bool = True) -> int:
        # inserts new item or replaces item with same field name if found
        if insert_field_check:
            self.check_match_can_be_inserted(match)
        if isinstance(self.match.entries, MutableSequence):
            for index, entry in enumerate(self.match.entries):
                if match.field == entry.field:
                    self.match.entries[index] == match
                    return index
            self.match.entries.append(match)
            return len(self.match.entries) - 1
        else:
            raise TypeError("Match entries must be defined as MutableSequence (eg. List) to use insert_match method")

    def check_match_can_be_inserted(self, match: Entry) -> None:
        existing_fields = set([entry.field for entry in self.match.entries])
        forbidden_fields = set(MUTUALLY_EXCLUSIVE_MATCH_FIELD_LOOKUP.get(match.field, []))
        colliding_fields = set(existing_fields) & set(forbidden_fields)
        if colliding_fields:
            raise ValueError(f"{match.field} is mutually exclusive with {colliding_fields}")


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
    description: str = "default description"
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

    def _enumerate_sequences(self, from_index: int = 0) -> None:
        """Updates sequence entries with appropriate index.

        Args:
            from_index (int, optional): Only rules after that index in table will be updated. Defaults to 0.
        """
        if isinstance(self.sequences, MutableSequence):
            start_index = from_index
            sequence_count = len(self.sequences)
            if from_index < 0:
                start_index = sequence_count - start_index
            for i in range(start_index, sequence_count):
                self.sequences[i].sequence_id = i + 1
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to use _enumerate_sequences method")

    def pop(self, index: int = -1) -> None:
        """Removes a sequence item at given index, consecutive sequence items will be enumarated again.

        Args:
            index (int, optional): Defaults to -1.
        """
        if isinstance(self.sequences, MutableSequence):
            self.sequences.pop(index)
            self._enumerate_sequences(index)
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to use pop method")

    def add(self, item: DefinitionSequence) -> int:
        """Adds new sequence item as last in table, index will be autogenerated.

        Args:
            item (DefinitionSequence): item to be added to sequences

        Returns:
            int: index at which item was added
        """
        if isinstance(self.sequences, MutableSequence):
            insert_index = len(self.sequences)
            self.sequences.append(item)
            self._enumerate_sequences(insert_index)
            return insert_index
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to add method")


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


class PolicyDefinitionEndpoints(Protocol):
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
