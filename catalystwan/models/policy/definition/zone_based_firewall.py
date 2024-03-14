# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Network
from typing import Dict, List, Literal, Set, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.misc.application_protocols import ApplicationProtocol
from catalystwan.models.policy.policy_definition import (
    AdvancedInspectionProfileAction,
    AppListEntry,
    AppListFlatEntry,
    ConnectionEventsAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataPrefixListEntry,
    DestinationFQDNEntry,
    DestinationGeoLocationEntry,
    DestinationGeoLocationListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationPortListEntry,
    LogAction,
    Match,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    ProtocolEntry,
    ProtocolNameEntry,
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
)

ZoneBasedFWPolicySequenceEntry = Annotated[
    Union[
        AppListEntry,
        AppListFlatEntry,
        DestinationDataPrefixListEntry,
        DestinationFQDNEntry,
        DestinationGeoLocationEntry,
        DestinationGeoLocationListEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        DestinationPortListEntry,
        ProtocolEntry,
        ProtocolNameEntry,
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

ZoneBasedFWPolicyActions = Annotated[
    Union[
        AdvancedInspectionProfileAction,
        ConnectionEventsAction,
        LogAction,
    ],
    Field(discriminator="type"),
]


class ZoneBasedFWPolicyMatches(Match):
    entries: List[ZoneBasedFWPolicySequenceEntry] = []


class ZoneBasedFWPolicySequenceWithRuleSets(PolicyDefinitionSequenceBase):
    sequence_type: Literal["zoneBasedFW"] = Field(
        default="zoneBasedFW", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    match: ZoneBasedFWPolicyMatches
    ruleset: bool = True
    actions: List[ZoneBasedFWPolicyActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_rule_set_lists(self, rule_set_ids: Set[UUID]) -> None:
        self._insert_match(RuleSetListEntry.from_rule_set_ids(rule_set_ids))

    def match_app_list(self, app_list_id: UUID) -> None:
        if self.base_action != "inspect":
            raise ValueError("Action must be inspect when Application/Application Family List is selected.")
        self._insert_match(AppListEntry(ref=app_list_id))


class ZoneBasedFWPolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["zoneBasedFW"] = Field(
        default="zoneBasedFW", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    match: ZoneBasedFWPolicyMatches
    actions: List[LogAction] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_app_list(self, app_list_id: UUID) -> None:
        if self.base_action != "inspect":
            raise ValueError("Action must be inspect when Application/Application Family List is selected.")
        self._insert_match(AppListEntry(ref=app_list_id))

    def match_destination_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(DestinationDataPrefixListEntry(ref=data_prefix_list_id))

    def match_destination_fqdn(self, fqdn: str) -> None:
        self._insert_match(DestinationFQDNEntry(value=fqdn))

    def match_destination_geo_location(self, geo_location: str) -> None:
        self._insert_match(DestinationGeoLocationEntry(value=geo_location))

    def match_destination_geo_location_list(self, geo_location_list_id: UUID) -> None:
        self._insert_match(DestinationGeoLocationListEntry(ref=geo_location_list_id))

    def match_destination_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(DestinationIPEntry.from_ipv4_networks(networks))

    def match_destination_ports(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_destination_port_list(self, port_list_id: UUID) -> None:
        self._insert_match(DestinationPortListEntry(ref=port_list_id))

    def match_protocols(self, protocols: Set[int]) -> None:
        self._insert_match(ProtocolEntry.from_protocol_set(protocols))

    def match_protocol_names(self, names: Set[str], protocol_map: Dict[str, ApplicationProtocol]) -> None:
        app_protocols = []
        for name in names:
            app_protocol = protocol_map.get(name, None)
            if app_protocol is None:
                raise ValueError(f"{name} not found in protocol map keys: {protocol_map.keys()}")
            app_protocols.append(app_protocol)
        self._insert_match(ProtocolNameEntry.from_application_protocols(app_protocols))
        self._insert_match(DestinationPortEntry.from_application_protocols(app_protocols), False)
        self._insert_match(ProtocolEntry.from_application_protocols(app_protocols), False)

    def match_protocol_name_list(self, protocol_name_list_id: UUID) -> None:
        self._insert_match(ProtocolNameListEntry(ref=protocol_name_list_id))

    def match_source_data_prefix_list(self, data_prefix_lists: List[UUID]) -> None:
        self._insert_match(SourceDataPrefixListEntry(ref=data_prefix_lists))

    def match_source_fqdn(self, fqdn: str) -> None:
        self._insert_match(SourceFQDNEntry(value=fqdn))

    def match_source_fqdn_list(self, fqdn_list_id: UUID) -> None:
        self._insert_match(SourceFQDNListEntry(ref=fqdn_list_id))

    def match_source_geo_location(self, geo_location: str) -> None:
        self._insert_match(SourceGeoLocationEntry(value=geo_location))

    def match_source_geo_location_list(self, geo_location_list_id: UUID) -> None:
        self._insert_match(SourceGeoLocationListEntry(ref=geo_location_list_id))

    def match_source_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(SourceIPEntry.from_ipv4_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_source_port_list(self, port_list_id: UUID) -> None:
        self._insert_match(SourcePortListEntry(ref=port_list_id))


class ZoneBasedFWPolicyEntry(BaseModel):
    source_zone_id: Union[UUID, Literal["self"]] = Field(
        default="self", serialization_alias="sourceZone", validation_alias="sourceZone"
    )
    destination_zone_id: UUID = Field(serialization_alias="destinationZone", validation_alias="destinationZone")
    model_config = ConfigDict(populate_by_name=True)


class ZoneBasedFWPolicyHeader(PolicyDefinitionBase):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"
    mode: str = Field(default="security")
    model_config = ConfigDict(populate_by_name=True)


class ZoneBasedFWPolicyDefinition(DefinitionWithSequencesCommonBase):
    sequences: List[Union[ZoneBasedFWPolicySequence, ZoneBasedFWPolicySequenceWithRuleSets]] = []
    entries: List[ZoneBasedFWPolicyEntry] = []


class ZoneBasedFWPolicy(ZoneBasedFWPolicyHeader):
    type: Literal["zoneBasedFW"] = "zoneBasedFW"
    mode: Literal["security", "unified"] = "security"
    definition: ZoneBasedFWPolicyDefinition = ZoneBasedFWPolicyDefinition()

    def add_ipv4_rule(
        self, name: str, base_action: PolicyActionType = "drop", log: bool = False
    ) -> ZoneBasedFWPolicySequence:
        """Adds new IPv4 Rule to Zone Based Firewall Policy

        Args:
            name (str): Rule name
            base_action (BaseAction, optional): Rule base action (drop, pass, inspect) Defaults to BaseAction.DROP.
            log (bool, optional): If true sets log action

        Returns:
            ZoneBasedFWPolicySequence: Rule object for which matches must be added
        """
        sequence = ZoneBasedFWPolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
            match=ZoneBasedFWPolicyMatches(),
        )
        if log:
            sequence.actions.append(LogAction())
        self.definition.add(sequence)
        return sequence

    def add_ipv4_rule_sets(
        self, name: str, base_action: PolicyActionType = "drop", log: bool = False
    ) -> ZoneBasedFWPolicySequenceWithRuleSets:
        sequence = ZoneBasedFWPolicySequenceWithRuleSets(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
            match=ZoneBasedFWPolicyMatches(),
        )
        if log:
            sequence.actions.append(LogAction())
        self.definition.add(sequence)
        return sequence

    def add_zone_pair(self, source_zone_id: UUID, destination_zone_id: UUID) -> None:
        entry = ZoneBasedFWPolicyEntry(
            source_zone_id=source_zone_id,
            destination_zone_id=destination_zone_id,
        )
        self.definition.entries.append(entry)


class ZoneBasedFWPolicyEditPayload(ZoneBasedFWPolicy, PolicyDefinitionId):
    pass


class ZoneBasedFWPolicyGetResponse(ZoneBasedFWPolicy, PolicyDefinitionGetResponse):
    pass
