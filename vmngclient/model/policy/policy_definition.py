import datetime
from enum import Enum
from functools import wraps
from ipaddress import IPv4Address, IPv4Network
from typing import Dict, List, MutableSequence, Optional, Protocol, Sequence, Set, Tuple, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated, Literal

from vmngclient.model.common import TLOCColorEnum
from vmngclient.model.misc.application_protocols import ApplicationProtocol
from vmngclient.model.policy.lists_entries import EncapEnum
from vmngclient.typed_list import DataSequence


def port_set_and_ranges_to_str(ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> str:
    if not ports and not port_ranges:
        raise ValueError("Non empty port set or port range list must be provided")
    ports_str = " ".join(f"{port_begin}-{port_end}" for port_begin, port_end in port_ranges)
    ports_str += " " if ports_str else ""
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


class LocalTLOCListEntryValue(BaseModel):
    color: TLOCColorEnum
    encap: EncapEnum
    restrict: Optional[str] = None


class TLOCEntryValue(BaseModel):
    ip: IPv4Address
    color: TLOCColorEnum
    encap: EncapEnum


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


class DNSTypeEntryValues(str, Enum):
    HOST = "host"
    UMBRELLA = "umbrella"


class LossProtectionEnum(str, Enum):
    FEC_ADAPTIVE = "fecAdaptive"
    FEC_ALWAYS = "fecAlways"
    PACKET_DUPLICATION = "packetDuplication"


class ServiceChainEntryValue(BaseModel):
    type: str = Field("SC1", pattern=r"SC(1[0-6]|[1-9])")
    vpn: str
    restrict: Optional[str] = None
    local: Optional[str] = None
    tloc: Optional[TLOCEntryValue] = None


class PacketLengthEntry(BaseModel):
    field: Literal["packetLength"] = "packetLength"
    value: str = Field(description="0-65536 range or single number")

    @staticmethod
    def from_range(packet_lengths: Tuple[int, int]) -> "PacketLengthEntry":
        if packet_lengths[0] == packet_lengths[1]:
            return PacketLengthEntry(value=str(packet_lengths[0]))
        return PacketLengthEntry(value=f"{packet_lengths[0]}-{packet_lengths[1]}")


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


class IPAddressEntry(BaseModel):
    field: Literal["ipAddress"] = "ipAddress"
    value: IPv4Address


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


class ForwardingClassEntry(BaseModel):
    field: Literal["forwardingClass"] = "forwardingClass"
    value: str = Field(max_length=32)


class NATPoolEntry(BaseModel):
    field: Literal["pool"] = "pool"
    value: str


class UseVPNEntry(BaseModel):
    field: Literal["useVpn"] = "useVpn"
    value: str = "0"


class FallBackEntry(BaseModel):
    field: Literal["fallback"] = "fallback"
    value: str = ""


class NextHopEntry(BaseModel):
    field: Literal["nextHop"] = "nextHop"
    value: IPv4Address


class NextHopLooseEntry(BaseModel):
    field: Literal["nextHopLoose"] = "nextHopLoose"
    value: str


class LocalTLOCListEntry(BaseModel):
    field: Literal["localTlocList"] = "localTlocList"
    value: LocalTLOCListEntryValue


class DNSTypeEntry(BaseModel):
    field: Literal["dnsType"] = "dnsType"
    value: DNSTypeEntryValues


class ServiceChainEntry(BaseModel):
    field: Literal["serviceChain"] = "serviceChain"
    value: ServiceChainEntryValue


class VPNEntry(BaseModel):
    field: Literal["vpn"] = "vpn"
    value: str


class TLOCEntry(BaseModel):
    field: Literal["tloc"] = "tloc"
    value: TLOCEntryValue


class NATVPNEntry(RootModel):
    root: List[Union[UseVPNEntry, FallBackEntry]]

    @staticmethod
    def from_nat_vpn(fallback: bool, vpn: int = 0) -> "NATVPNEntry":
        if fallback:
            return NATVPNEntry(root=[UseVPNEntry(value=str(vpn)), FallBackEntry()])
        return NATVPNEntry(root=[UseVPNEntry(value=str(vpn))])


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
    def from_rule_set_ids(rule_set_ids: Set[str]) -> "RuleSetListEntry":
        return RuleSetListEntry(ref=" ".join(rule_set_ids))


class PolicerListEntry(BaseModel):
    field: Literal["policer"] = "policer"
    ref: str


class TLOCListEntry(BaseModel):
    field: Literal["tlocList"] = "tlocList"
    ref: str


class PrefferedColorGroupListEntry(BaseModel):
    field: Literal["preferredColorGroup"] = "preferredColorGroup"
    ref: str
    color_restrict: bool = Field(False, alias="colorRestrict")
    model_config = ConfigDict(populate_by_name=True)


RedirectDNSActionEntry = Union[IPAddressEntry, DNSTypeEntry]


ActionSetEntry = Annotated[
    Union[
        DSCPEntry,
        ForwardingClassEntry,
        PrefferedColorGroupListEntry,
        LocalTLOCListEntry,
        NextHopEntry,
        NextHopLooseEntry,
        PolicerListEntry,
        ServiceChainEntry,
        VPNEntry,
        TLOCListEntry,
        TLOCEntry,
    ],
    Field(discriminator="field"),
]


class LogAction(BaseModel):
    type: Literal["log"] = "log"
    parameter: str = ""


class CountAction(BaseModel):
    type: Literal["count"] = "count"
    parameter: str


class ActionSet(BaseModel):
    type: Literal["set"] = "set"
    parameter: List[ActionSetEntry] = []


class NATAction(BaseModel):
    type: Literal["nat"] = "nat"
    parameter: Union[NATPoolEntry, NATVPNEntry]

    @staticmethod
    def from_nat_pool(nat_pool: int) -> "NATAction":
        return NATAction(parameter=NATPoolEntry(value=str(nat_pool)))

    @staticmethod
    def from_nat_vpn(fallback: bool, vpn: int = 0) -> "NATAction":
        return NATAction(parameter=NATVPNEntry.from_nat_vpn(fallback=fallback, vpn=vpn))


class CFlowDAction(BaseModel):
    type: Literal["cflowd"] = "cflowd"


class RedirectDNSAction(BaseModel):
    type: Literal["redirectDns"] = "redirectDns"
    parameter: RedirectDNSActionEntry

    @staticmethod
    def from_ip_address(ip: IPv4Address) -> "RedirectDNSAction":
        return RedirectDNSAction(parameter=IPAddressEntry(value=ip))

    @staticmethod
    def from_dns_type(dns_type: DNSTypeEntryValues = DNSTypeEntryValues.HOST) -> "RedirectDNSAction":
        return RedirectDNSAction(parameter=DNSTypeEntry(value=dns_type))


class TCPOptimizationAction(BaseModel):
    type: Literal["tcpOptimization"] = "tcpOptimization"
    parameter: str = ""


class DREOptimizationAction(BaseModel):
    type: Literal["dreOptimization"] = "dreOptimization"
    parameter: str = ""


class ServiceNodeGroupAction(BaseModel):
    type: Literal["serviceNodeGroup"] = "serviceNodeGroup"
    parameter: str = Field(default="", pattern=r"^(SNG-APPQOE(3[01]|[12][0-9]|[1-9])?)?$")


class LossProtectionAction(BaseModel):
    type: Literal["lossProtect"] = "lossProtect"
    parameter: LossProtectionEnum


class LossProtectionFECAction(BaseModel):
    type: Literal["lossProtectFec"] = "lossProtectFec"
    parameter: LossProtectionEnum = LossProtectionEnum.FEC_ALWAYS
    value: Optional[str] = Field(default=None, description="BETA")


class LossProtectionPacketDuplicationAction(BaseModel):
    type: Literal["lossProtectPktDup"] = "lossProtectPktDup"
    parameter: LossProtectionEnum = LossProtectionEnum.PACKET_DUPLICATION


class SecureInternetGatewayAction(BaseModel):
    type: Literal["sig"] = "sig"
    parameter: str = ""


class FallBackToRoutingAction(BaseModel):
    type: Literal["fallbackToRouting"] = "fallbackToRouting"
    parameter: str = ""


ActionEntry = Annotated[
    Union[
        LogAction,
        CountAction,
        ActionSet,
        NATAction,
        CFlowDAction,
        RedirectDNSAction,
        TCPOptimizationAction,
        DREOptimizationAction,
        ServiceNodeGroupAction,
        LossProtectionAction,
        LossProtectionFECAction,
        LossProtectionPacketDuplicationAction,
        SecureInternetGatewayAction,
        FallBackToRoutingAction,
    ],
    Field(discriminator="type"),
]


MatchEntry = Annotated[
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

MUTUALLY_EXCLUSIVE_FIELDS = [
    {"destinationDataPrefixList", "destinationIp"},
    {"sourceDataPrefixList", "sourceIp"},
    {"protocolName", "protocolNameList", "protocol", "destinationPort", "destinationPortList"},
    {"localTlocList", "preferredColorGroup"},
    {"sig", "fallbackToRouting", "nat", "nextHop", "serviceChain"},
]


def generate_field_name_check_lookup(spec: Sequence[Set[str]]) -> Dict[str, List[str]]:
    lookup: Dict[str, List[str]] = {}
    for exclusive_set in spec:
        for field in exclusive_set:
            lookup[field] = list(exclusive_set - {field})
    return lookup


MUTUALLY_EXCLUSIVE_FIELD_LOOKUP = generate_field_name_check_lookup(MUTUALLY_EXCLUSIVE_FIELDS)


class Match(BaseModel):
    entries: Sequence[MatchEntry]


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
    actions: Sequence[ActionEntry]

    @staticmethod
    def check_field_collision(field: str, fields: Sequence[str]) -> None:
        existing_fields = set(fields)
        forbidden_fields = set(MUTUALLY_EXCLUSIVE_FIELD_LOOKUP.get(field, []))
        colliding_fields = set(existing_fields) & set(forbidden_fields)
        if colliding_fields:
            raise ValueError(f"{field} is mutually exclusive with {colliding_fields}")

    def check_match_can_be_inserted(self, match: MatchEntry) -> None:
        self.check_field_collision(
            match.field,
            [entry.field for entry in self.match.entries],
        )

    def check_action_can_be_inserted_in_set(
        self, action: ActionSetEntry, action_set_param: List[ActionSetEntry]
    ) -> None:
        self.check_field_collision(
            action.field,
            [param.field for param in action_set_param],
        )

    def get_match_entries_by_field(self, field: str) -> Sequence[MatchEntry]:
        return [entry for entry in self.match.entries if entry.field == field]

    def insert_match(self, match: MatchEntry, insert_field_check: bool = True) -> int:
        # inserts new item or replaces item with same field name if found
        if insert_field_check:
            self.check_match_can_be_inserted(match)
        if isinstance(self.match.entries, MutableSequence):
            for index, entry in enumerate(self.match.entries):
                if match.field == entry.field:
                    self.match.entries[index] = match
                    return index
            self.match.entries.append(match)
            return len(self.match.entries) - 1
        else:
            raise TypeError("Match entries must be defined as MutableSequence (eg. List) to use insert_match method")

    def insert_action(self, action: ActionEntry) -> None:
        if isinstance(self.actions, MutableSequence):
            for index, entry in enumerate(self.actions):
                if action.type == entry.type:
                    self.actions[index] = action
                    return
            self.actions.append(action)
        else:
            raise TypeError("Action entries must be defined as MutableSequence (eg. List) to use insert_match method")

    def remove_action(self, action_type_name: str) -> None:
        if isinstance(self.actions, MutableSequence):
            self.actions[:] = [action for action in self.actions if action.type != action_type_name]

    def insert_action_in_set(self, action: ActionSetEntry) -> None:
        if isinstance(self.actions, MutableSequence):
            # Check if ActionSet entry already exist
            action_sets = [act for act in self.actions if isinstance(act, ActionSet)]
            if len(action_sets) < 1:
                # if not found insert new empty ActionSet
                action_set = ActionSet()
                self.actions.append(action_set)
            else:
                action_set = action_sets[0]
            # Now we operate on action_set parameter list
            self.check_action_can_be_inserted_in_set(action, action_set.parameter)
            for index, param in enumerate(action_set.parameter):
                if action.field == param.field:
                    action_set.parameter[index] = action
                    return
            action_set.parameter.append(action)

    def remove_action_from_set(self, field_name: str) -> None:
        if isinstance(self.actions, MutableSequence):
            for action in self.actions:
                if isinstance(action, ActionSet):
                    action.parameter[:] = [param for param in action.parameter if param.field != field_name]


def accept_action(method):
    @wraps(method)
    def wrapper(self: DefinitionSequence, *args, **kwargs):
        if self.base_action != BaseAction.ACCEPT:
            raise ValueError(f"{method.__name__} only allowed when base_action is {BaseAction.ACCEPT}")
        return method(self, *args, **kwargs)

    return wrapper


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
        pattern="^[a-zA-Z0-9_-]{1,128}$",
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
    sequences: Optional[Sequence[DefinitionSequence]] = None

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
