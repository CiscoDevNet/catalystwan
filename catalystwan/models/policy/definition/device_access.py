# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network
from typing import Any, List, Literal, Optional, Set, Tuple, Union
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.policy.policy_definition import (
    CountAction,
    DefaultAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DeviceAccessProtocol,
    Match,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
)

DeviceAccessPolicySequenceMatchEntry = Annotated[
    Union[
        DestinationDataPrefixListEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        SourceDataPrefixListEntry,
        SourceIPEntry,
        SourcePortEntry,
    ],
    Field(discriminator="field"),
]

DeviceAccessPolicySequenceActions = Any  # TODO


class DeviceAccessPolicyHeader(PolicyDefinitionBase):
    type: Literal["deviceAccessPolicy"] = "deviceAccessPolicy"


class DeviceAccessPolicySequenceMatch(Match):
    entries: List[DeviceAccessPolicySequenceMatchEntry] = []


class DeviceAccessPolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["deviceaccesspolicy"] = Field(
        default="deviceaccesspolicy", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="accept", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: DeviceAccessPolicySequenceMatch = DeviceAccessPolicySequenceMatch()
    actions: List[DeviceAccessPolicySequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_device_access_protocol(self, port: DeviceAccessProtocol) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports={port}))

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

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))


class DeviceAccessPolicy(DeviceAccessPolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[DeviceAccessPolicySequence] = []
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
    ) -> DeviceAccessPolicySequence:
        seq = DeviceAccessPolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        if device_access_protocol is not None:
            seq.match_device_access_protocol(port=device_access_protocol)
        self.add(seq)
        return seq


class DeviceAccessPolicyEditPayload(DeviceAccessPolicy, PolicyDefinitionId):
    pass


class DeviceAccessPolicyGetResponse(DeviceAccessPolicy, PolicyDefinitionGetResponse):
    pass
