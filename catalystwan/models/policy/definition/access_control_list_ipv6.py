# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Network
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
    DestinationDataIPv6PrefixListEntry,
    DestinationIPv6Entry,
    DestinationPortEntry,
    LogAction,
    Match,
    MirrorAction,
    NextHeaderEntry,
    NextHopEntry,
    PacketLengthEntry,
    PLPEntry,
    PolicerAction,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    Reference,
    SourceDataIPv6PrefixListEntry,
    SourceIPv6Entry,
    SourcePortEntry,
    TCPEntry,
    TrafficClassEntry,
    accept_action,
)

AclIPv6PolicySequenceMatchEntry = Annotated[
    Union[
        ClassMapListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationIPv6Entry,
        DestinationPortEntry,
        NextHeaderEntry,
        PacketLengthEntry,
        PLPEntry,
        SourceDataIPv6PrefixListEntry,
        SourceIPv6Entry,
        SourcePortEntry,
        TCPEntry,
        TrafficClassEntry,
    ],
    Field(discriminator="field"),
]

AclIPv6PolicySequenceActions = Any  # TODO


class AclIPv6PolicyHeader(PolicyDefinitionBase):
    type: Literal["aclv6"] = "aclv6"


class AclIPv6PolicySequenceMatch(Match):
    entries: List[AclIPv6PolicySequenceMatchEntry] = []


class AclIPv6PolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["aclv6"] = Field(
        default="aclv6", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="accept", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: AclIPv6PolicySequenceMatch = AclIPv6PolicySequenceMatch()
    actions: List[AclIPv6PolicySequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_next_header(self, next_header: int) -> None:
        self._insert_match(NextHeaderEntry(value=str(next_header)))

    def match_packet_length(self, packet_lengths: Tuple[int, int]) -> None:
        self._insert_match(PacketLengthEntry.from_range(packet_lengths))

    def match_low_plp(self) -> None:
        self._insert_match(PLPEntry(value="low"))

    def match_high_plp(self) -> None:
        self._insert_match(PLPEntry(value="high"))

    def match_source_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(SourceDataIPv6PrefixListEntry(ref=data_prefix_list_id))

    def match_source_ip(self, networks: List[IPv6Network]) -> None:
        self._insert_match(SourceIPv6Entry.from_ipv6_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_destination_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(DestinationDataIPv6PrefixListEntry(ref=data_prefix_list_id))

    def match_destination_ip(self, networks: List[IPv6Network]) -> None:
        self._insert_match(DestinationIPv6Entry.from_ipv6_networks(networks))

    def match_destination_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_tcp(self) -> None:
        self._insert_match(TCPEntry())

    def match_class_map_list_entry(self, class_map_list_id: UUID) -> None:
        self._insert_match(ClassMapListEntry(ref=class_map_list_id))

    def match_traffic_class(self, traffic_class: int) -> None:
        self._insert_match(TrafficClassEntry(value=str(traffic_class)))

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))

    def associate_log_action(self) -> None:
        self._insert_action(LogAction())

    @accept_action
    def associate_next_hop_action(self, next_hop: IPv4Address) -> None:
        self._insert_action_in_set(NextHopEntry(value=next_hop))

    @accept_action
    def associate_traffic_class_action(self, traffic_class: int) -> None:
        self._insert_action_in_set(TrafficClassEntry(value=str(traffic_class)))

    @accept_action
    def associate_mirror_action(self, mirror_list_id: UUID) -> None:
        self._insert_action(MirrorAction(parameter=Reference(ref=mirror_list_id)))

    @accept_action
    def associate_class_map_list_action(self, class_map_list_id: UUID) -> None:
        self._insert_action(ClassMapAction(parameter=Reference(ref=class_map_list_id)))

    @accept_action
    def associate_policer_list_action(self, policer_list_id: UUID) -> None:
        self._insert_action(PolicerAction(parameter=Reference(ref=policer_list_id)))


class AclIPv6Policy(AclIPv6PolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[AclIPv6PolicySequence] = []
    default_action: DefaultAction = Field(
        default=DefaultAction(type="drop"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_acl_sequence(
        self, name: str = "Access Control List", base_action: PolicyActionType = "accept"
    ) -> AclIPv6PolicySequence:
        seq = AclIPv6PolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv6",
        )
        self.add(seq)
        return seq


class AclIPv6PolicyEditPayload(AclIPv6Policy, PolicyDefinitionId):
    pass


class AclIPv6PolicyGetResponse(AclIPv6Policy, PolicyDefinitionGetResponse):
    pass
