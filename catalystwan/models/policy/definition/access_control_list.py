# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network
from typing import Any, List, Literal, Set, Tuple, Union
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.policy.policy_definition import (
    ClassMapAction,
    ClassMapListEntry,
    CountAction,
    DefaultAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DSCPEntry,
    LogAction,
    Match,
    MirrorAction,
    NextHopEntry,
    PacketLengthEntry,
    PLPEntry,
    PolicerAction,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    ProtocolEntry,
    Reference,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    TCPEntry,
    accept_action,
)

AclPolicySequenceMatchEntry = Annotated[
    Union[
        ClassMapListEntry,
        DestinationDataPrefixListEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        DSCPEntry,
        PacketLengthEntry,
        PLPEntry,
        ProtocolEntry,
        SourceDataPrefixListEntry,
        SourceIPEntry,
        SourcePortEntry,
        TCPEntry,
    ],
    Field(discriminator="field"),
]

AclPolicySequenceActions = Any  # TODO


class AclPolicyHeader(PolicyDefinitionBase):
    type: Literal["acl"] = "acl"


class AclPolicySequenceMatch(Match):
    entries: List[AclPolicySequenceMatchEntry] = []


class AclPolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["acl"] = Field(
        default="acl", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="accept", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: AclPolicySequenceMatch = AclPolicySequenceMatch()
    actions: List[AclPolicySequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_dscp(self, dscp: int) -> None:
        self._insert_match(DSCPEntry(value=str(dscp)))

    def match_packet_length(self, packet_lengths: Tuple[int, int]) -> None:
        self._insert_match(PacketLengthEntry.from_range(packet_lengths))

    def match_low_plp(self) -> None:
        self._insert_match(PLPEntry(value="low"))

    def match_high_plp(self) -> None:
        self._insert_match(PLPEntry(value="high"))

    def match_protocols(self, protocols: Set[int]) -> None:
        self._insert_match(ProtocolEntry.from_protocol_set(protocols))

    def match_source_data_prefix_list(self, data_prefix_lists: List[UUID]) -> None:
        self._insert_match(SourceDataPrefixListEntry(ref=data_prefix_lists))

    def match_source_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(SourceIPEntry.from_ipv4_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_destination_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(DestinationDataPrefixListEntry(ref=data_prefix_list_id))

    def match_destination_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(DestinationIPEntry.from_ipv4_networks(networks))

    def match_destination_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_tcp(self) -> None:
        self._insert_match(TCPEntry())

    def match_class_map_list_entry(self, class_map_list_id: UUID) -> None:
        self._insert_match(ClassMapListEntry(ref=class_map_list_id))

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))

    def associate_log_action(self) -> None:
        self._insert_action(LogAction())

    @accept_action
    def associate_dscp_action(self, dscp: int) -> None:
        self._insert_action_in_set(DSCPEntry(value=str(dscp)))

    @accept_action
    def associate_next_hop_action(self, next_hop: IPv4Address) -> None:
        self._insert_action_in_set(NextHopEntry(value=next_hop))

    @accept_action
    def associate_mirror_action(self, mirror_list_id: UUID) -> None:
        self._insert_action(MirrorAction(parameter=Reference(ref=mirror_list_id)))

    @accept_action
    def associate_class_map_list_action(self, class_map_list_id: UUID) -> None:
        self._insert_action(ClassMapAction(parameter=Reference(ref=class_map_list_id)))

    @accept_action
    def associate_policer_list_action(self, policer_list_id: UUID) -> None:
        self._insert_action(PolicerAction(parameter=Reference(ref=policer_list_id)))


class AclPolicy(AclPolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[AclPolicySequence] = []
    default_action: DefaultAction = Field(
        default=DefaultAction(type="drop"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_acl_sequence(
        self, name: str = "Access Control List", base_action: PolicyActionType = "accept"
    ) -> AclPolicySequence:
        seq = AclPolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        self.add(seq)
        return seq


class AclPolicyEditPayload(AclPolicy, PolicyDefinitionId):
    pass


class AclPolicyGetResponse(AclPolicy, PolicyDefinitionGetResponse):
    pass
