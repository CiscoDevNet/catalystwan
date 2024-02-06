from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId


class Action(str, Enum):
    DROP = "drop"
    ACCEPT = "accept"


class IcmpMessage(str, Enum):
    ADMINISTRATIVELY_PROHIBITED = "administratively-prohibited"
    DOD_HOST_PROHIBITED = "dod-host-prohibited"
    DOD_NET_PROHIBITED = "dod-net-prohibited"
    ECHO = "echo"
    ECHO_REPLY = "echo-reply"
    ECHO_REPLY_NO_ERROR = "echo-reply-no-error"
    EXTENDED_ECHO = "extended-echo"
    EXTENDED_ECHO_REPLY = "extended-echo-reply"
    GENERAL_PARAMETER_PROBLEM = "general-parameter-problem"
    HOST_ISOLATED = "host-isolated"
    HOST_PRECEDENCE_UNREACHABLE = "host-precedence-unreachable"
    HOST_REDIRECT = "host-redirect"
    HOST_TOS_REDIRECT = "host-tos-redirect"
    HOST_TOS_UNREACHABLE = "host-tos-unreachable"
    HOST_UNKNOWN = "host-unknown"
    HOST_UNREACHABLE = "host-unreachable"
    INTERFACE_ERROR = "interface-error"
    MALFORMED_QUERY = "malformed-query"
    MULTIPLE_INTERFACE_MATCH = "multiple-interface-match"
    NET_REDIRECT = "net-redirect"
    NET_TOS_REDIRECT = "net-tos-redirect"
    NET_TOS_UNREACHABLE = "net-tos-unreachable"
    NET_UNREACHABLE = "net-unreachable"
    NETWORK_UNKNOWN = "network-unknown"
    NO_ROOM_FOR_OPTION = "no-room-for-option"
    OPTION_MISSING = "option-missing"
    PACKET_TOO_BIG = "packet-too-big"
    PARAMETER_PROBLEM = "parameter-problem"
    PHOTURIS = "photuris"
    PORT_UNREACHABLE = "port-unreachable"
    PRECEDENCE_UNREACHABLE = "precedence-unreachable"
    PROTOCOL_UNREACHABLE = "protocol-unreachable"
    REASSEMBLY_TIMEOUT = "reassembly-timeout"
    REDIRECT = "redirect"
    ROUTER_ADVERTISEMENT = "router-advertisement"
    ROUTER_SOLICITATION = "router-solicitation"
    SOURCE_ROUTE_FAILED = "source-route-failed"
    TABLE_ENTRY_ERROR = "table-entry-error"
    TIME_EXCEEDED = "time-exceeded"
    TIMESTAMP_REPLY = "timestamp-reply"
    TIMESTAMP_REQUEST = "timestamp-request"
    TTL_EXCEEDED = "ttl-exceeded"
    UNREACHABLE = "unreachable"


class Icmp6Message(str, Enum):
    BEYOND_SCOPE = "beyond-scope"
    CP_ADVERTISEMENT = "cp-advertisement"
    CP_SOLICITATION = "cp-solicitation"
    DESTINATION_UNREACHABLE = "destination-unreachable"
    DHAAD_REPLY = "dhaad-reply"
    DHAAD_REQUEST = "dhaad-request"
    ECHO_REPLY = "echo-reply"
    ECHO_REQUEST = "echo-request"
    HEADER = "header"
    HOP_LIMIT = "hop-limit"
    IND_ADVERTISEMENT = "ind-advertisement"
    IND_SOLICITATION = "ind-solicitation"
    MLD_QUERY = "mld-query"
    MLD_REDUCTION = "mld-reduction"
    MLD_REPORT = "mld-report"
    MLDV2_REPORT = "mldv2-report"
    MPD_ADVERTISEMENT = "mpd-advertisement"
    MPD_SOLICITATION = "mpd-solicitation"
    MR_ADVERTISEMENT = "mr-advertisement"
    MR_SOLICITATION = "mr-solicitation"
    MR_TERMINATION = "mr-termination"
    ND_NA = "nd-na"
    ND_NS = "nd-ns"
    NEXT_HEADER_TYPE = "next-header-type"
    NI_QUERY = "ni-query"
    NI_QUERY_NAME = "ni-query-name"
    NI_QUERY_V4_ADDRESS = "ni-query-v4-address"
    NI_QUERY_V6_ADDRESS = "ni-query-v6-address"
    NI_RESPONSE = "ni-response"
    NI_RESPONSE_QTYPE_UNKNOWN = "ni-response-qtype-unknown"
    NI_RESPONSE_REFUSE = "ni-response-refuse"
    NI_RESPONSE_SUCCESS = "ni-response-success"
    NO_ADMIN = "no-admin"
    NO_ROUTE = "no-route"
    PACKET_TOO_BIG = "packet-too-big"
    PARAMETER_OPTION = "parameter-option"
    PARAMETER_PROBLEM = "parameter-problem"
    PORT_UNREACHABLE = "port-unreachable"
    REASSEMBLY_TIMEOUT = "reassembly-timeout"
    REDIRECT = "redirect"
    REJECT_ROUTE = "reject-route"
    RENUM_COMMAND = "renum-command"
    RENUM_RESULT = "renum-result"
    RENUM_SEQ_NUMBER = "renum-seq-number"
    ROUTER_ADVERTISEMENT = "router-advertisement"
    ROUTER_RENUMBERING = "router-renumbering"
    ROUTER_SOLICITATION = "router-solicitation"
    RPL_CONTROL = "rpl-control"
    SOURCE_POLICY = "source-policy"
    SOURCE_ROUTE_HEADER = "source-route-header"
    TIME_EXCEEDED = "time-exceeded"
    UNREACHABLE = "unreachable"


class SourceDataIPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip_prefix: Union[Global[str], Variable] = Field(alias="sourceIpPrefix")


class SourceDataIPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip_prefix: Union[Global[str], Variable] = Field(alias="sourceIpPrefix")


class SourceDataIPv4PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_data_prefix_list: RefId = Field(alias="sourceDataPrefixList")


class SourceDataIPv6PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_data_prefix_list: RefId = Field(alias="sourceDataPrefixList")


class SourcePort(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_port: Global[int] = Field(alias="sourcePort")


class DestinationDataIPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    destination_ip_prefix: Union[Global[str], Variable] = Field(alias="destinationIpPrefix")


class DestinationDataIPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    destination_ip_prefix: Union[Global[str], Variable] = Field(alias="destinationIpPrefix")


class DestinationDataIPv4PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    destination_data_prefix_list: RefId = Field(alias="destinationDataPrefixList")


class DestinationDataIPv6PrefixParcel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    destination_data_prefix_list: RefId = Field(alias="destinationDataPrefixList")


class DestinationPort(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    destination_port: Global[int] = Field(alias="destinationPort")


class TcpState(str, Enum):
    SYN = "syn"


class IPv4Match(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dscp: Optional[Global[List[int]]] = None
    packet_length: Optional[Global[int]] = Field(alias="packetLength", default=None)
    protocol: Optional[Global[List[int]]] = None
    icmp_message: Optional[Global[List[IcmpMessage]]] = Field(alias="icmpMsg", default=None)
    source_data_prefix: Optional[Union[SourceDataIPv4Prefix, SourceDataIPv4PrefixParcel]] = Field(
        alias="sourceDataPrefix", default=None
    )
    source_ports: Optional[List[SourcePort]] = Field(alias="sourcePorts", default=None)
    destination_data_prefix: Optional[Union[DestinationDataIPv4Prefix, DestinationDataIPv4PrefixParcel]] = Field(
        alias="destinationDataPrefix", default=None
    )
    destination_ports: Optional[List[DestinationPort]] = Field(alias="destinationPorts", default=None)
    tcp: Optional[Global[TcpState]] = None


class IPv6Match(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_header: Optional[Global[int]] = Field(alias="nextHeader", default=None)
    packet_length: Optional[Global[int]] = Field(alias="packetLength", default=None)
    source_data_prefix: Optional[Union[SourceDataIPv6Prefix, SourceDataIPv6PrefixParcel]] = Field(
        alias="sourceDataPrefix", default=None
    )
    source_ports: Optional[List[SourcePort]] = Field(alias="sourcePorts", default=None)
    destination_data_prefix: Optional[Union[DestinationDataIPv6Prefix, DestinationDataIPv6PrefixParcel]] = Field(
        alias="destinationDataPrefix", default=None
    )
    destination_ports: Optional[List[DestinationPort]] = Field(alias="destinationPorts", default=None)
    tcp: Optional[Global[TcpState]] = None
    traffic_class: Optional[Global[int]] = None
    icmp6_message: Optional[Global[List[Icmp6Message]]] = Field(alias="icmpMsg", default=None)


class ServiceChainNumber(str, Enum):
    SC1 = "SC1"
    SC2 = "SC2"
    SC3 = "SC3"
    SC4 = "SC4"
    SC5 = "SC5"
    SC6 = "SC6"
    SC7 = "SC7"
    SC8 = "SC8"
    SC9 = "SC9"
    SC10 = "SC10"
    SC11 = "SC11"
    SC12 = "SC12"
    SC13 = "SC13"
    SC14 = "SC14"
    SC15 = "SC15"
    SC16 = "SC16"


class ServiceChain(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_chain_number: Union[Global[ServiceChainNumber], Variable] = Field(alias="serviceChainNumber")
    vpn: Optional[Union[Global[int], Variable]] = None
    fallback: Optional[Union[Global[bool], Variable, Default[bool]]] = None


class AcceptActionIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    set_dscp: Optional[Global[int]] = Field(alias="setDscp", default=None)
    counter_name: Optional[Global[str]] = Field(alias="counterName", default=None)
    log: Optional[Union[Global[bool], Default[bool]]] = None
    set_next_hop: Optional[Global[str]] = Field(alias="setNextHop", default=None)
    set_service_chain: Optional[ServiceChain] = Field(alias="setServiceChain", default=None)
    mirror: Optional[RefId] = None
    policer: Optional[RefId] = None


class AcceptActionIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    counter_name: Optional[Global[str]] = Field(alias="counterName", default=None)
    log: Optional[Union[Global[bool], Default[bool]]] = None
    set_next_hop: Optional[Global[str]] = Field(alias="setNextHop", default=None)
    set_service_chain: Optional[ServiceChain] = Field(alias="setServiceChain", default=None)
    set_traffic_class: Optional[Global[int]] = Field(alias="setTrafficClass", default=None)
    mirror: Optional[RefId] = None
    policer: Optional[RefId] = None


class DropAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    counter_name: Optional[Global[str]] = Field(alias="counterName", default=None)
    log: Optional[Union[Global[bool], Default[bool]]] = None


class AcceptActionsIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    accept: AcceptActionIPv4


class AcceptActionsIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    accept: AcceptActionIPv6


class DropActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    drop: DropAction


class IPv4SequenceBaseAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    sequence_id: Global[int] = Field(alias="sequenceId")
    sequence_name: Global[str] = Field(alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        alias="baseAction", default=Default[Action](value=Action.ACCEPT)
    )
    match_entries: Optional[List[IPv4Match]] = Field(alias="matchEntries", default=None)


class IPv6SequenceBaseAction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    sequence_id: Global[int] = Field(alias="sequenceId")
    sequence_name: Global[str] = Field(alias="sequenceName")
    base_action: Union[Global[Action], Default[Action]] = Field(
        alias="baseAction", default=Default[Action](value=Action.ACCEPT)
    )
    match_entries: Optional[List[IPv6Match]] = Field(alias="matchEntries", default=None)


class IPv4SequenceActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    sequence_id: Global[int] = Field(alias="sequenceId")
    sequence_name: Global[str] = Field(alias="sequenceName")
    actions: List[Union[AcceptActionsIPv4, DropActions]] = Field(alias="actions")
    match_entries: Optional[List[IPv4Match]] = Field(alias="matchEntries", default=None)


class IPv6SequenceActions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    sequence_id: Global[int] = Field(alias="sequenceId")
    sequence_name: Global[str] = Field(alias="sequenceName")
    actions: List[Union[AcceptActionsIPv6, DropActions]] = Field(alias="actions")
    match_entries: Optional[List[IPv6Match]] = Field(alias="matchEntries", default=None)


class IPv4AclData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        alias="defaultAction", default=Default[Action](value=Action.DROP)
    )
    sequences: List[Union[IPv4SequenceBaseAction, IPv4SequenceActions]]


class IPv4AclCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: IPv4AclData


class IPv6AclData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    defautl_action: Union[Global[Action], Default[Action]] = Field(
        alias="defaultAction", default=Default[Action](value=Action.DROP)
    )
    sequences: List[Union[IPv6SequenceBaseAction, IPv6SequenceActions]]


class IPv6AclCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: IPv6AclData
