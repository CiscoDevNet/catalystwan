# mypy: disable-error-code="empty-body"
from typing import Any, List, Union

from pydantic import Field
from typing_extensions import Annotated

from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    DefinitionSequence,
    DestinationDataIPv6PrefixListEntry,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationRegionEntry,
    DNSAppListEntry,
    DNSEntry,
    DSCPEntry,
    PacketLengthEntry,
    PLPEntry,
    PolicyDefinitionHeader,
    ProtocolEntry,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    TCPEntry,
    TrafficToEntry,
)

TrafficDataPolicySequenceEntry = Annotated[
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

TrafficDataPolicySequenceActions = Any  # TODO


class TrafficDataPolicyHeader(PolicyDefinitionHeader):
    type: str = Field(default="data", const=True)


class TrafficDataPolicySequence(DefinitionSequence):
    type: str = Field(default="data", const=True)
    entries: List[TrafficDataPolicySequenceEntry]
    actions: List[TrafficDataPolicySequenceActions]


class TrafficDataPolicy(TrafficDataPolicyHeader):
    sequences: List[TrafficDataPolicySequence] = []  # type: ignore [assignment]

    def add_ipv4_sequence(self, name: str) -> TrafficDataPolicySequence:
        pass
