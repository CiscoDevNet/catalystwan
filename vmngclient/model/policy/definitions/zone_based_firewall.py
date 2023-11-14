# mypy: disable-error-code="empty-body"
from ipaddress import IPv4Network
from typing import List, Literal, Set, Tuple, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from vmngclient.model.policy.policy_definition import (
    AppListEntry,
    BaseAction,
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
    RuleSetListEntry,
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
        AppListEntry,
        DestinationDataPrefixListEntry,
        DestinationFQDNEntry,
        DestinationGeoLocationEntry,
        DestinationGeoLocationListEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        DestinationPortListEntry,
        ProtocolEntry,
        ProtocolNameListEntry,
        RuleSetListEntry,
        SourceDataPrefixListEntry,
        SourceFQDNEntry,
        SourceFQDNListEntry,
        SourceGeoLocationEntry,
        SourceGeoLocationListEntry,
        SourceIPEntry,
        SourcePortEntry,
        SourcePortListEntry,
    ],
    Field(discriminator="field"),
]

ZoneBasedFWPolicySequenceEntryWithRuleSets = Annotated[
    Union[
        AppListEntry,
        RuleSetListEntry,
    ],
    Field(discriminator="field"),
]


class LogAction(BaseModel):
    type: Literal["log"] = "log"
    parameter: str = ""


class ZoneBasedFWPolicyMatches(Match):
    entries: List[ZoneBasedFWPolicySequenceEntry] = []


class ZoneBasedFWPolicySequenceWithRuleSets(DefinitionSequence):
    sequence_type: SequenceType = Field(default=SequenceType.ZONE_BASED_FW, const=True, alias="sequenceType")
    match: ZoneBasedFWPolicyMatches
    ruleset: bool = True

    class Config:
        allow_population_by_field_name = True

    def add_match(self, match: ZoneBasedFWPolicySequenceEntryWithRuleSets):
        added_fields = [entry.field for entry in self.match.entries]
        if match.field in added_fields:
            raise ValueError("{match.field} already added")
        self.match.entries.append(match)

    def match_rule_set_lists(self, rule_set_ids: Set[str]) -> None:
        self.add_match(RuleSetListEntry.with_rule_set_ids(rule_set_ids))

    def match_app_list(self, app_list_id: str) -> None:
        if self.base_action != BaseAction.INSPECT:
            raise ValueError("Action must be Inspect when Application/Application Family List is selected.")
        self.add_match(AppListEntry(ref=app_list_id))


class ZoneBasedFWPolicySequence(DefinitionSequence):
    sequence_type: SequenceType = Field(default=SequenceType.ZONE_BASED_FW, const=True, alias="sequenceType")
    match: ZoneBasedFWPolicyMatches

    class Config:
        allow_population_by_field_name = True

    def insert_match(self, match: ZoneBasedFWPolicySequenceEntry) -> int:
        # overwrite if exists
        for index, entry in enumerate(self.match.entries):
            if match.field == entry.field:
                self.match.entries[index] == match
                return index
        self.match.entries.append(match)
        return len(self.match.entries) - 1

    def match_app_list(self, app_list_id: str) -> None:
        if self.base_action != BaseAction.INSPECT:
            raise ValueError("Action must be Inspect when Application/Application Family List is selected.")
        self.insert_match(AppListEntry(ref=app_list_id))

    def match_destination_data_prefix_list(self, data_prefix_list_id: str) -> None:
        self.insert_match(DestinationDataPrefixListEntry(ref=data_prefix_list_id))

    def match_destination_fqdn(self, fqdn: str) -> None:
        self.insert_match(DestinationFQDNEntry(value=fqdn))

    def match_destination_geo_location(self, geo_location: str) -> None:
        self.insert_match(DestinationGeoLocationEntry(value=geo_location))

    def match_destination_geo_location_list(self, geo_location_list_id: str) -> None:
        self.insert_match(DestinationGeoLocationListEntry(ref=geo_location_list_id))

    def match_destination_ip(self, networks: List[IPv4Network]) -> None:
        self.insert_match(DestinationIPEntry.from_ipv4_networks(networks))

    def match_destination_ports(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self.insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_destination_port_list(self, port_list_id: str) -> None:
        self.insert_match(DestinationPortListEntry(ref=port_list_id))

    def match_protocols(self, protocols: Set[int]) -> None:
        self.insert_match(ProtocolEntry.from_protocol_set(protocols))

    def match_protocol_name_list(self, protocol_name_list_id: str) -> None:
        self.insert_match(ProtocolNameListEntry(ref=protocol_name_list_id))

    def match_source_data_prefix_list(self, data_prefix_list_id: str) -> None:
        self.insert_match(SourceDataPrefixListEntry(ref=data_prefix_list_id))

    def match_source_fqdn(self, fqdn: str) -> None:
        self.insert_match(SourceFQDNEntry(value=fqdn))

    def match_source_fqdn_list(self, fqdn_list_id: str) -> None:
        self.insert_match(SourceFQDNListEntry(ref=fqdn_list_id))

    def match_source_geo_location(self, geo_location: str) -> None:
        self.insert_match(SourceGeoLocationEntry(value=geo_location))

    def match_source_geo_location_list(self, geo_location_list: str) -> None:
        self.insert_match(SourceGeoLocationListEntry(ref=geo_location_list))

    def match_source_ip(self, networks: List[IPv4Network]) -> None:
        self.insert_match(SourceIPEntry.from_ipv4_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self.insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_source_port_list(self, port_list_id: str) -> None:
        self.insert_match(SourcePortListEntry(ref=port_list_id))


class ZoneBasedFWPolicyEntry(BaseModel):
    source_zone: str = Field(default="self", alias="sourceZone")
    destination_zone: str = Field(alias="destinationZone")

    class Config:
        allow_population_by_field_name = True


class ZoneBasedFWPolicyHeader(PolicyDefinitionHeader):
    type: str = Field(default="zoneBasedFW", const=True)
    mode: str = Field(default="security")

    class Config:
        allow_population_by_field_name = True


class ZoneBasedFWPolicyDefinition(PolicyDefinitionBody):
    sequences: List[Union[ZoneBasedFWPolicySequence, ZoneBasedFWPolicySequenceWithRuleSets]] = []
    entries: List[ZoneBasedFWPolicyEntry] = []


class ZoneBasedFWPolicy(ZoneBasedFWPolicyHeader):
    type: str = Field(default="zoneBasedFW", const=True)
    mode: str = Field(default="security", const=True)
    definition: ZoneBasedFWPolicyDefinition = ZoneBasedFWPolicyDefinition()

    def _enumerate_sequences(self, from_index: int = 0) -> None:
        """Updates sequences entries with appropriate order and rule values.

        Args:
            from_index (int, optional): Only sequences after that index in table will be updated. Defaults to 0.
        """
        start_index = from_index
        sequence_count = len(self.definition.sequences)
        if from_index < 0:
            start_index = sequence_count - start_index
        for i in range(start_index, sequence_count):
            self.definition.sequences[i].sequence_id = i + 1

    def add(self, sequence: Union[ZoneBasedFWPolicySequence, ZoneBasedFWPolicySequenceWithRuleSets]) -> None:
        """Adds new sequence as last in table, sequence_id will be autogenerated.

        Args:
            sequence (ZoneBasedFWPolicySequence): sequence representing rule matches, action pair
        """
        insert_index = len(self.definition.sequences)
        self.definition.sequences.append(sequence)
        self._enumerate_sequences(insert_index)

    def pop(self, index: int = -1) -> None:
        """Removes a sequence at given index, consecutive sequences will be enumarated again.

        Args:
            index (int, optional): Defaults to -1.
        """
        self.definition.sequences.pop(index)
        self._enumerate_sequences(index)

    def add_ipv4_rule(
        self, name: str, base_action: BaseAction = BaseAction.DROP, log: bool = False
    ) -> ZoneBasedFWPolicySequence:
        """Adds new IPv4 Rule to Zone Based Firewall Policy

        Args:
            name (str): Rule name
            base_action (BaseAction, optional): Rule base action (drop, pass, inspect) Defaults to BaseAction.DROP.
            log (bool, optional): If true sets log action

        Returns:
            ZoneBasedFWPolicySequence: Rule object for which matches must be added
        """
        sequence = ZoneBasedFWPolicySequence(  # type: ignore[call-arg]
            sequence_id=0,  # sequence id will be autogenerated in add method
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
            match=ZoneBasedFWPolicyMatches(),
        )
        if log:
            sequence.actions.append(LogAction())
        self.add(sequence)
        return sequence

    def add_ipv4_rule_sets(
        self, name: str, base_action: BaseAction = BaseAction.DROP, log: bool = False
    ) -> ZoneBasedFWPolicySequenceWithRuleSets:
        sequence = ZoneBasedFWPolicySequenceWithRuleSets(  # type: ignore[call-arg]
            sequence_id=0,  # sequence id will be autogenerated in add method
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
            match=ZoneBasedFWPolicyMatches(),
        )
        if log:
            sequence.actions.append(LogAction())
        self.add(sequence)
        return sequence

    def add_zone_pair(self, source_zone_id: str, destination_zone_id: str) -> None:
        entry = ZoneBasedFWPolicyEntry(  # type: ignore[call-arg]
            source_zone=source_zone_id,
            destination_zone=destination_zone_id,
        )
        self.definition.entries.append(entry)
