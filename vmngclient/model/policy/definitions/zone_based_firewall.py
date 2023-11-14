# mypy: disable-error-code="empty-body"
from typing import List, Union

from pydantic.v1 import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    DefinitionSequence,
    DestinationDataPrefixListEntry,
    DestinationFQDNEntry,
    DestinationGeoLocationEntry,
    DestinationGeoLocationListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationPortListEntry,
    Match,
    PolicyDefinitionBody,
    PolicyDefinitionHeader,
    ProtocolEntry,
    ProtocolNameListEntry,
    SequenceType,
    SourceDataPrefixListEntry,
    SourceFQDNEntry,
    SourceFQDNListEntry,
    SourceGeoLocationEntry,
    SourceGeoLocationListEntry,
    SourceIPEntry,
    SourcePortEntry,
    SourcePortListEntry,
)

ZoneBasedFWPolicySequenceEntry = Annotated[
    Union[
        SourceFQDNListEntry,
        ProtocolEntry,
        SourceIPEntry,
        SourcePortEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        SourceFQDNEntry,
        DestinationFQDNEntry,
        SourceGeoLocationEntry,
        DestinationGeoLocationEntry,
        SourceDataPrefixListEntry,
        DestinationDataPrefixListEntry,
        SourceGeoLocationListEntry,
        DestinationGeoLocationListEntry,
        SourcePortListEntry,
        DestinationPortListEntry,
        ProtocolNameListEntry,
        AppListEntry,
    ],
    Field(discriminator="field"),
]


class ZoneBasedFWPolicyMatch(Match):
    entries: List[ZoneBasedFWPolicySequenceEntry]


class ZoneBasedFWPolicySequence(DefinitionSequence):
    sequence_type: SequenceType = Field(default=SequenceType.ZONE_BASED_FW, const=True, alias="sequenceType")
    match: ZoneBasedFWPolicyMatch


class ZoneBasedFWPolicyEntry(BaseModel):
    source_zone: str = Field(default="self", alias="sourceZone")
    destination_zone: str = Field(alias="destinationZone")


class ZoneBasedFWPolicy(PolicyDefinitionHeader):
    type: str = Field(default="zoneBasedFW", const=True)
    mode: str = Field(default="security", const=True)


class ZoneBasedFWPolicyDefinition(PolicyDefinitionBody):
    sequences: List[ZoneBasedFWPolicySequence] = []
    entries: List[ZoneBasedFWPolicyEntry]
