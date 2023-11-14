# mypy: disable-error-code="empty-body"
from typing import List, Union

from pydantic.v1 import Field
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
    PolicyDefinitionBody,
    PolicyDefinitionHeader,
    ProtocolEntry,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    TCPEntry,
    TrafficToEntry,
)

DataPolicySequenceEntry = Annotated[
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


class DataPolicy(PolicyDefinitionHeader):
    type: str = Field(default="data", const=True)


class DataPolicySequence(DefinitionSequence):
    type: str = Field(default="data", const=True)
    entries: List[DataPolicySequenceEntry]


class DataPolicyDefinition(PolicyDefinitionBody):
    sequences: List[DataPolicySequence] = []
