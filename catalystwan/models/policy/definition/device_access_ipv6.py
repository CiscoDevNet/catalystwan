# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Network
from typing import Any, List, Literal, Optional, Set, Tuple, Union
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.policy.policy_definition import (
    CountAction,
    DefaultAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataIPv6PrefixListEntry,
    DestinationIPv6Entry,
    DestinationPortEntry,
    DeviceAccessProtocol,
    Match,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    SourceDataIPv6PrefixListEntry,
    SourceIPv6Entry,
    SourcePortEntry,
)

DeviceAccessIPv6PolicySequenceMatchEntry = Annotated[
    Union[
        DestinationDataIPv6PrefixListEntry,
        DestinationIPv6Entry,
        DestinationPortEntry,
        SourceDataIPv6PrefixListEntry,
        SourceIPv6Entry,
        SourcePortEntry,
    ],
    Field(discriminator="field"),
]

DeviceAccessIPv6PolicySequenceActions = Any  # TODO


class DeviceAccessIPv6PolicyHeader(PolicyDefinitionBase):
    type: Literal["deviceAccessPolicyv6"] = "deviceAccessPolicyv6"


class DeviceAccessIPv6PolicySequenceMatch(Match):
    entries: List[DeviceAccessIPv6PolicySequenceMatchEntry] = []


class DeviceAccessIPv6PolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["deviceaccesspolicyv6"] = Field(
        default="deviceaccesspolicyv6", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="accept", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: DeviceAccessIPv6PolicySequenceMatch = DeviceAccessIPv6PolicySequenceMatch()
    actions: List[DeviceAccessIPv6PolicySequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_device_access_protocol(self, port: DeviceAccessProtocol) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports={port}))

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

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))


class DeviceAccessIPv6Policy(DeviceAccessIPv6PolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[DeviceAccessIPv6PolicySequence] = []
    default_action: DefaultAction = Field(
        default=DefaultAction(type="drop"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_acl_sequence(
        self,
        name: str = "Device Access Control List",
        base_action: PolicyActionType = "accept",
        device_access_protocol: Optional[DeviceAccessProtocol] = None,
    ) -> DeviceAccessIPv6PolicySequence:
        seq = DeviceAccessIPv6PolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        if device_access_protocol is not None:
            seq.match_device_access_protocol(port=device_access_protocol)
        self.add(seq)
        return seq


class DeviceAccessIPv6PolicyEditPayload(DeviceAccessIPv6Policy, PolicyDefinitionId):
    pass


class DeviceAccessIPv6PolicyGetResponse(DeviceAccessIPv6Policy, PolicyDefinitionGetResponse):
    pass
