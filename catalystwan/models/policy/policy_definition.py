# Copyright 2023 Cisco Systems, Inc. and its affiliates

import datetime
from functools import wraps
from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import Any, Dict, List, MutableSequence, Optional, Sequence, Set, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator, model_validator
from typing_extensions import Annotated, Literal

from catalystwan.models.common import (
    EncapType,
    ICMPMessageType,
    ServiceChainNumber,
    TLOCColor,
    check_fields_exclusive,
    str_as_str_list,
    str_as_uuid_list,
)
from catalystwan.models.misc.application_protocols import ApplicationProtocol


def port_set_and_ranges_to_str(ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> str:
    assert ports or port_ranges
    ports_str = " ".join(f"{port_begin}-{port_end}" for port_begin, port_end in port_ranges)
    ports_str += " " if ports_str else ""
    ports_str += " ".join(str(p) for p in ports)
    return ports_str


def networks_to_str(networks: Sequence[Union[IPv4Network, IPv6Network]]) -> str:
    return " ".join(str(net) for net in networks)


PLPEntryType = Literal[
    "low",
    "high",
]

DNSEntryType = Literal[
    "request",
    "response",
]

TrafficTargetType = Literal[
    "access",
    "core",
    "service",
]

DestinationRegion = Literal[
    "primary-region",
    "secondary-region",
    "other-region",
]

OriginProtocol = Literal[
    "aggregate",
    "bgp",
    "bgp-external",
    "bgp-internal",
    "connected",
    "eigrp",
    "ospf",
    "ospf-inter-area",
    "ospf-intra-area",
    "ospf-external1",
    "ospf-external2",
    "rip",
    "static",
    "eigrp-summary",
    "eigrp-internal",
    "eigrp-external",
    "lisp",
    "nat-dia",
    "natpool",
    "isis",
    "isis-level1",
    "isis-level2",
]

PathType = Literal[
    "hierarchical-path",
    "direct-path",
    "transport-gateway-path",
]

SequenceIpType = Literal[
    "ipv4",
    "ipv6",
    "all",
]

PolicyActionType = Literal[
    "drop",
    "accept",
    "pass",
    "inspect",
    "reject",
]

SequenceType = Literal[
    "applicationFirewall",
    "data",
    "serviceChaining",
    "trafficEngineering",
    "qos",
    "zoneBasedFW",
    "tloc",
    "route",
    "acl",
    "aclv6",
    "deviceaccesspolicy",
    "deviceaccesspolicyv6",
]


Optimized = Literal[
    "true",
    "false",
]

DNSTypeEntryType = Literal[
    "host",
    "umbrella",
]

LossProtectionType = Literal[
    "fecAdaptive",
    "fecAlways",
    "packetDuplication",
]

MultiRegionRole = Literal[
    "border-router",
    "edge-router",
]

ServiceType = Literal[
    "FW",
    "IDP",
    "IDS",
    "netsvc1",
    "netsvc2",
    "netsvc3",
    "netsvc4",
]

TLOCActionType = Literal[
    "strict",
    "primary",
    "backup",
    "ecmp",
]

Carrier = Literal[
    "default",
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
]

DeviceAccessProtocol = Literal[22, 161]


class Reference(BaseModel):
    ref: UUID


class VariableName(BaseModel):
    vip_variable_name: str = Field(serialization_alias="vipVariableName", validation_alias="vipVariableName")


class LocalTLOCListEntryValue(BaseModel):
    color: TLOCColor
    encap: EncapType
    restrict: Optional[str] = None


class TLOCEntryValue(BaseModel):
    ip: IPv4Address
    color: TLOCColor
    encap: EncapType


class ServiceChainEntryValue(BaseModel):
    type: ServiceChainNumber = Field(default="SC1")
    vpn: str
    restrict: Optional[str] = None
    local: Optional[str] = None
    tloc: Optional[TLOCEntryValue] = None


class PacketLengthEntry(BaseModel):
    field: Literal["packetLength"] = "packetLength"
    value: str = Field(description="0-65536 range or single number")

    @staticmethod
    def from_range(packet_lengths: Tuple[int, int]) -> "PacketLengthEntry":
        if packet_lengths[0] == packet_lengths[1]:
            return PacketLengthEntry(value=str(packet_lengths[0]))
        return PacketLengthEntry(value=f"{packet_lengths[0]}-{packet_lengths[1]}")


class PLPEntry(BaseModel):
    field: Literal["plp"] = "plp"
    value: PLPEntryType


class ProtocolEntry(BaseModel):
    field: Literal["protocol"] = "protocol"
    value: str = Field(description="0-255 single numbers separate by space")
    app: Optional[str] = None

    @staticmethod
    def from_protocol_set(protocols: Set[int]) -> "ProtocolEntry":
        return ProtocolEntry(value=" ".join(str(p) for p in protocols))

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "ProtocolEntry":
        return ProtocolEntry(
            value=" ".join(p.protocol_as_string_of_numbers() for p in app_prots),
            app=" ".join(p.name for p in app_prots),
        )


class DSCPEntry(BaseModel):
    field: Literal["dscp"] = "dscp"
    value: str = Field(description="0-63 single numbers separate by space")


class SourceIPEntry(BaseModel):
    field: Literal["sourceIp"] = "sourceIp"
    value: str = Field(description="IP network specifiers separate by space")

    @staticmethod
    def from_ipv4_networks(networks: List[IPv4Network]) -> "SourceIPEntry":
        return SourceIPEntry(value=networks_to_str(networks))


class SourceIPv6Entry(BaseModel):
    field: Literal["sourceIpv6"] = "sourceIpv6"
    value: str = Field(description="IPv6 network specifiers separate by space")

    @staticmethod
    def from_ipv6_networks(networks: List[IPv6Network]) -> "SourceIPv6Entry":
        return SourceIPv6Entry(value=networks_to_str(networks))


class IPAddressEntry(BaseModel):
    field: Literal["ipAddress"] = "ipAddress"
    value: IPv4Address


class SourcePortEntry(BaseModel):
    field: Literal["sourcePort"] = "sourcePort"
    value: str = Field(description="0-65535 range or separate by space")

    @staticmethod
    def from_port_set_and_ranges(ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> "SourcePortEntry":
        return SourcePortEntry(value=port_set_and_ranges_to_str(ports, port_ranges))


class DestinationIPEntry(BaseModel):
    field: Literal["destinationIp"] = "destinationIp"
    value: str

    @staticmethod
    def from_ipv4_networks(networks: List[IPv4Network]) -> "DestinationIPEntry":
        return DestinationIPEntry(value=networks_to_str(networks))


class DestinationIPv6Entry(BaseModel):
    field: Literal["destinationIpv6"] = "destinationIpv6"
    value: str

    @staticmethod
    def from_ipv6_networks(networks: List[IPv6Network]) -> "DestinationIPv6Entry":
        return DestinationIPv6Entry(value=networks_to_str(networks))


class DestinationPortEntry(BaseModel):
    field: Literal["destinationPort"] = "destinationPort"
    value: str = Field(description="0-65535 range or separate by space")
    app: Optional[str] = None

    @staticmethod
    def from_port_set_and_ranges(
        ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []
    ) -> "DestinationPortEntry":
        return DestinationPortEntry(value=port_set_and_ranges_to_str(ports, port_ranges))

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "DestinationPortEntry":
        return DestinationPortEntry(
            value=" ".join(p.port for p in app_prots if p.port),
            app=" ".join(p.name for p in app_prots),
        )


class TCPEntry(BaseModel):
    field: Literal["tcp"] = "tcp"
    value: Literal["syn"] = "syn"


class DNSEntry(BaseModel):
    field: Literal["dns"] = "dns"
    value: DNSEntryType


class TrafficToEntry(BaseModel):
    field: Literal["trafficTo"] = "trafficTo"
    value: TrafficTargetType


class DestinationRegionEntry(BaseModel):
    field: Literal["destinationRegion"] = "destinationRegion"
    value: DestinationRegion


class SourceFQDNEntry(BaseModel):
    field: Literal["sourceFqdn"] = "sourceFqdn"
    value: str = Field(max_length=120)


class DestinationFQDNEntry(BaseModel):
    field: Literal["destinationFqdn"] = "destinationFqdn"
    value: str = Field(max_length=120)


class SourceGeoLocationEntry(BaseModel):
    field: Literal["sourceGeoLocation"] = "sourceGeoLocation"
    value: str = Field(description="Space separated list of ISO3166 country codes")


class DestinationGeoLocationEntry(BaseModel):
    field: Literal["destinationGeoLocation"] = "destinationGeoLocation"
    value: str = Field(description="Space separated list of ISO3166 country codes")


class ProtocolNameEntry(BaseModel):
    field: Literal["protocolName"] = "protocolName"
    value: str

    @staticmethod
    def from_application_protocols(app_prots: List[ApplicationProtocol]) -> "ProtocolNameEntry":
        return ProtocolNameEntry(value=" ".join(p.name for p in app_prots))


class ForwardingClassEntry(BaseModel):
    field: Literal["forwardingClass"] = "forwardingClass"
    value: str = Field(max_length=32)


class NATPoolEntry(BaseModel):
    field: Literal["pool"] = "pool"
    value: str


class UseVPNEntry(BaseModel):
    field: Literal["useVpn"] = "useVpn"
    value: str = "0"


class FallBackEntry(BaseModel):
    field: Literal["fallback"] = "fallback"
    value: str = ""


class NextHopEntry(BaseModel):
    field: Literal["nextHop"] = "nextHop"
    value: IPv4Address


class NextHopLooseEntry(BaseModel):
    field: Literal["nextHopLoose"] = "nextHopLoose"
    value: str


class OMPTagEntry(BaseModel):
    field: Literal["ompTag"] = "ompTag"
    value: str = Field(description="Number in range 0-4294967295")


class OriginEntry(BaseModel):
    field: Literal["origin"] = "origin"
    value: OriginProtocol


class OriginatorEntry(BaseModel):
    field: Literal["originator"] = "originator"
    value: IPv4Address


class PreferenceEntry(BaseModel):
    field: Literal["preference"] = "preference"
    value: str = Field(description="Number in range 0-4294967295")


class PathTypeEntry(BaseModel):
    field: Literal["pathType"] = "pathType"
    value: PathType


class RegionEntry(BaseModel):
    field: Literal["regionId"] = "regionId"
    value: str


class RoleEntry(BaseModel):
    field: Literal["role"] = "role"
    value: MultiRegionRole


class SiteEntry(BaseModel):
    field: Literal["siteId"] = "siteId"
    value: str = Field(description="Site ID numeric value")


class LocalTLOCListEntry(BaseModel):
    field: Literal["localTlocList"] = "localTlocList"
    value: LocalTLOCListEntryValue


class DNSTypeEntry(BaseModel):
    field: Literal["dnsType"] = "dnsType"
    value: DNSTypeEntryType


class ServiceChainEntry(BaseModel):
    field: Literal["serviceChain"] = "serviceChain"
    value: ServiceChainEntryValue


class VPNEntry(BaseModel):
    field: Literal["vpn"] = "vpn"
    value: str


class TLOCEntry(BaseModel):
    field: Literal["tloc"] = "tloc"
    value: TLOCEntryValue


class CommunityEntry(BaseModel):
    field: Literal["community"] = "community"
    value: str = Field(description="Example: 1000:10000 or internet or local-AS or no advertise or no-export")


class CommunityAdditiveEntry(BaseModel):
    field: Literal["communityAdditive"] = "communityAdditive"
    value: Literal["true"] = "true"


class CarrierEntry(BaseModel):
    field: Literal["carrier"] = "carrier"
    value: Carrier


class DomainIDEntry(BaseModel):
    field: Literal["domainId"] = "domainId"
    value: str = Field(description="Number in range 1-4294967295")


class GroupIDEntry(BaseModel):
    field: Literal["groupId"] = "groupId"
    value: str = Field(description="Number in range 0-4294967295")


class NextHeaderEntry(BaseModel):
    field: Literal["nextHeader"] = "nextHeader"
    value: str = Field(description="0-63 single numbers separate by space")


class TrafficClassEntry(BaseModel):
    field: Literal["trafficClass"] = "trafficClass"
    value: str = Field(description="Number in range 0-63")


class NATVPNEntry(RootModel):
    root: List[Union[UseVPNEntry, FallBackEntry]]

    @staticmethod
    def from_nat_vpn(fallback: bool, vpn: int = 0) -> "NATVPNEntry":
        if fallback:
            return NATVPNEntry(root=[UseVPNEntry(value=str(vpn)), FallBackEntry()])
        return NATVPNEntry(root=[UseVPNEntry(value=str(vpn))])


class ICMPMessageEntry(BaseModel):
    field: Literal["icmpMessage"] = "icmpMessage"
    value: List[ICMPMessageType]

    _value = field_validator("value", mode="before")(str_as_str_list)


class SourceDataPrefixListEntry(BaseModel):
    field: Literal["sourceDataPrefixList"] = "sourceDataPrefixList"
    ref: List[UUID]

    _ref = field_validator("ref", mode="before")(str_as_uuid_list)


class SourceDataIPv6PrefixListEntry(BaseModel):
    field: Literal["sourceDataIpv6PrefixList"] = "sourceDataIpv6PrefixList"
    ref: UUID


class DestinationDataPrefixListEntry(BaseModel):
    field: Literal["destinationDataPrefixList"] = "destinationDataPrefixList"
    ref: UUID


class DestinationDataIPv6PrefixListEntry(BaseModel):
    field: Literal["destinationDataIpv6PrefixList"] = "destinationDataIpv6PrefixList"
    ref: UUID


class DNSAppListEntry(BaseModel):
    field: Literal["dnsAppList"] = "dnsAppList"
    ref: UUID


class AppListEntry(BaseModel):
    field: Literal["appList"] = "appList"
    ref: UUID


class AppListFlatEntry(BaseModel):
    field: Literal["appListFlat"] = "appListFlat"
    ref: UUID


class SourceFQDNListEntry(BaseModel):
    field: Literal["sourceFqdnList"] = "sourceFqdnList"
    ref: UUID


class DestinationFQDNListEntry(BaseModel):
    field: Literal["destinationFqdnList"] = "destinationFqdnList"
    ref: UUID


class SourceGeoLocationListEntry(BaseModel):
    field: Literal["sourceGeoLocationList"] = "sourceGeoLocationList"
    ref: UUID


class DestinationGeoLocationListEntry(BaseModel):
    field: Literal["destinationGeoLocationList"] = "destinationGeoLocationList"
    ref: UUID


class ProtocolNameListEntry(BaseModel):
    field: Literal["protocolNameList"] = "protocolNameList"
    ref: UUID


class SourcePortListEntry(BaseModel):
    field: Literal["sourcePortList"] = "sourcePortList"
    ref: UUID


class DestinationPortListEntry(BaseModel):
    field: Literal["destinationPortList"] = "destinationPortList"
    ref: UUID


class RuleSetListEntry(BaseModel):
    field: Literal["ruleSetList"] = "ruleSetList"
    ref: str

    @staticmethod
    def from_rule_set_ids(rule_set_ids: Set[UUID]) -> "RuleSetListEntry":
        return RuleSetListEntry(ref=" ".join(str(rule_set_ids)))


class PolicerListEntry(BaseModel):
    field: Literal["policer"] = "policer"
    ref: UUID


class TLOCListEntry(BaseModel):
    field: Literal["tlocList"] = "tlocList"
    ref: UUID


class PrefferedColorGroupListEntry(BaseModel):
    field: Literal["preferredColorGroup"] = "preferredColorGroup"
    ref: UUID
    color_restrict: bool = Field(False, serialization_alias="colorRestrict", validation_alias="colorRestrict")
    model_config = ConfigDict(populate_by_name=True)


class ColorListEntry(BaseModel):
    field: Literal["colorList"] = "colorList"
    ref: UUID


class CommunityListEntry(BaseModel):
    field: Literal["community"] = "community"
    ref: UUID


class ExpandedCommunityListEntry(BaseModel):
    field: Literal["expandedCommunity"] = "expandedCommunity"
    ref: UUID


class SiteListEntry(BaseModel):
    field: Literal["siteList"] = "siteList"
    ref: UUID


class VPNListEntry(BaseModel):
    field: Literal["vpnList"] = "vpnList"
    ref: UUID


class PrefixListEntry(BaseModel):
    field: Literal["prefixList"] = "prefixList"
    ref: UUID


class RegionListEntry(BaseModel):
    field: Literal["regionList"] = "regionList"
    ref: UUID


class ClassMapListEntry(BaseModel):
    field: Literal["class"] = "class"
    ref: UUID


class ServiceEntryValue(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: ServiceType
    vpn: str
    tloc: Optional[TLOCEntryValue] = None
    tloc_list: Optional[TLOCListEntry] = Field(
        default=None, validation_alias="tlocList", serialization_alias="tlocList"
    )

    @model_validator(mode="after")
    def tloc_xor_tloc_list(self):
        check_fields_exclusive(self.__dict__, {"tloc", "tloc_list"}, True)
        return self


class ServiceEntry(BaseModel):
    field: Literal["service"] = "service"
    value: ServiceEntryValue


class TLOCActionEntry(BaseModel):
    field: Literal["tlocAction"] = "tlocAction"
    value: TLOCActionType


class AffinityEntry(BaseModel):
    field: Literal["affinity"] = "affinity"
    value: str = Field(description="Number in range 0-63")


RedirectDNSActionEntry = Union[IPAddressEntry, DNSTypeEntry]


class LogAction(BaseModel):
    type: Literal["log"] = "log"
    parameter: str = ""


class CountAction(BaseModel):
    type: Literal["count"] = "count"
    parameter: str


class NATAction(BaseModel):
    type: Literal["nat"] = "nat"
    parameter: Union[NATPoolEntry, NATVPNEntry]

    @staticmethod
    def from_nat_pool(nat_pool: int) -> "NATAction":
        return NATAction(parameter=NATPoolEntry(value=str(nat_pool)))

    @staticmethod
    def from_nat_vpn(fallback: bool, vpn: int = 0) -> "NATAction":
        return NATAction(parameter=NATVPNEntry.from_nat_vpn(fallback=fallback, vpn=vpn))


class CFlowDAction(BaseModel):
    type: Literal["cflowd"] = "cflowd"


class RedirectDNSAction(BaseModel):
    type: Literal["redirectDns"] = "redirectDns"
    parameter: RedirectDNSActionEntry

    @staticmethod
    def from_ip_address(ip: IPv4Address) -> "RedirectDNSAction":
        return RedirectDNSAction(parameter=IPAddressEntry(value=ip))

    @staticmethod
    def from_dns_type(dns_type: DNSTypeEntryType = "host") -> "RedirectDNSAction":
        return RedirectDNSAction(parameter=DNSTypeEntry(value=dns_type))


class TCPOptimizationAction(BaseModel):
    type: Literal["tcpOptimization"] = "tcpOptimization"
    parameter: str = ""


class DREOptimizationAction(BaseModel):
    type: Literal["dreOptimization"] = "dreOptimization"
    parameter: str = ""


class ServiceNodeGroupAction(BaseModel):
    type: Literal["serviceNodeGroup"] = "serviceNodeGroup"
    parameter: str = Field(default="", pattern=r"^(SNG-APPQOE(3[01]|[12][0-9]|[1-9])?)?$")


class LossProtectionAction(BaseModel):
    type: Literal["lossProtect"] = "lossProtect"
    parameter: LossProtectionType


class LossProtectionFECAction(BaseModel):
    type: Literal["lossProtectFec"] = "lossProtectFec"
    parameter: LossProtectionType = "fecAlways"
    value: Optional[str] = Field(default=None, description="BETA number in range 1-5")


class LossProtectionPacketDuplicationAction(BaseModel):
    type: Literal["lossProtectPktDup"] = "lossProtectPktDup"
    parameter: LossProtectionType = "packetDuplication"


class SecureInternetGatewayAction(BaseModel):
    type: Literal["sig"] = "sig"
    parameter: str = ""


class FallBackToRoutingAction(BaseModel):
    type: Literal["fallbackToRouting"] = "fallbackToRouting"
    parameter: str = ""


class ExportToAction(BaseModel):
    type: Literal["exportTo"] = "exportTo"
    parameter: VPNListEntry


class MirrorAction(BaseModel):
    type: Literal["mirror"] = "mirror"
    parameter: Reference


class ClassMapAction(BaseModel):
    type: Literal["class"] = "class"
    parameter: Reference


class PolicerAction(BaseModel):
    type: Literal["policer"] = "policer"
    parameter: Reference


class ConnectionEventsAction(BaseModel):
    type: Literal["connectionEvents"] = "connectionEvents"
    parameter: str = ""


class AdvancedInspectionProfileAction(BaseModel):
    type: Literal["advancedInspectionProfile"] = "advancedInspectionProfile"
    parameter: Reference


ActionSetEntry = Annotated[
    Union[
        AffinityEntry,
        CommunityAdditiveEntry,
        CommunityEntry,
        DSCPEntry,
        ForwardingClassEntry,
        LocalTLOCListEntry,
        NextHopEntry,
        NextHopLooseEntry,
        OMPTagEntry,
        PolicerListEntry,
        PreferenceEntry,
        PrefferedColorGroupListEntry,
        ServiceChainEntry,
        ServiceEntry,
        TLOCActionEntry,
        TLOCEntry,
        TLOCListEntry,
        TrafficClassEntry,
        VPNEntry,
    ],
    Field(discriminator="field"),
]


class ActionSet(BaseModel):
    type: Literal["set"] = "set"
    parameter: List[ActionSetEntry] = []


ActionEntry = Annotated[
    Union[
        ActionSet,
        AdvancedInspectionProfileAction,
        CFlowDAction,
        ClassMapAction,
        ConnectionEventsAction,
        CountAction,
        DREOptimizationAction,
        FallBackToRoutingAction,
        LogAction,
        LossProtectionAction,
        LossProtectionFECAction,
        LossProtectionPacketDuplicationAction,
        MirrorAction,
        NATAction,
        PolicerAction,
        RedirectDNSAction,
        SecureInternetGatewayAction,
        ServiceNodeGroupAction,
        TCPOptimizationAction,
        ExportToAction,
    ],
    Field(discriminator="type"),
]

MatchEntry = Annotated[
    Union[
        AppListEntry,
        AppListFlatEntry,
        CarrierEntry,
        ClassMapListEntry,
        ColorListEntry,
        CommunityListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationDataPrefixListEntry,
        DestinationFQDNEntry,
        DestinationFQDNListEntry,
        DestinationGeoLocationEntry,
        DestinationGeoLocationListEntry,
        DestinationIPEntry,
        DestinationIPv6Entry,
        DestinationPortEntry,
        DestinationPortListEntry,
        DestinationRegionEntry,
        DNSAppListEntry,
        DNSEntry,
        DomainIDEntry,
        DSCPEntry,
        ExpandedCommunityListEntry,
        GroupIDEntry,
        ICMPMessageEntry,
        NextHeaderEntry,
        OMPTagEntry,
        OriginatorEntry,
        OriginEntry,
        PacketLengthEntry,
        PathTypeEntry,
        PLPEntry,
        PreferenceEntry,
        PrefixListEntry,
        ProtocolEntry,
        ProtocolNameEntry,
        ProtocolNameListEntry,
        RegionEntry,
        RegionListEntry,
        RoleEntry,
        RuleSetListEntry,
        SiteEntry,
        SiteListEntry,
        SiteListEntry,
        SourceDataIPv6PrefixListEntry,
        SourceDataPrefixListEntry,
        SourceFQDNEntry,
        SourceFQDNListEntry,
        SourceGeoLocationEntry,
        SourceGeoLocationListEntry,
        SourceIPEntry,
        SourceIPv6Entry,
        SourcePortEntry,
        SourcePortListEntry,
        TCPEntry,
        TLOCEntry,
        TLOCListEntry,
        TrafficClassEntry,
        TrafficToEntry,
        VPNListEntry,
    ],
    Field(discriminator="field"),
]

MUTUALLY_EXCLUSIVE_FIELDS = [
    {"destinationDataPrefixList", "destinationIp"},
    {"destinationDataIpv6PrefixList", "destinationIpv6"},
    {"sourceDataPrefixList", "sourceIp"},
    {"sourceDataIpv6PrefixList", "sourceIpv6"},
    {"protocolName", "protocolNameList", "protocol", "destinationPort", "destinationPortList"},
    {"localTlocList", "preferredColorGroup"},
    {"sig", "fallbackToRouting", "nat", "nextHop", "serviceChain"},
    {"regionId", "regionList"},
    {"siteId", "siteList"},
    {"tloc", "tlocList"},
    {"service", "tlocAction"},
]


def _generate_field_name_check_lookup(spec: Sequence[Set[str]]) -> Dict[str, List[str]]:
    lookup: Dict[str, List[str]] = {}
    for exclusive_set in spec:
        for field in exclusive_set:
            lookup[field] = list(exclusive_set - {field})
    return lookup


MUTUALLY_EXCLUSIVE_FIELD_LOOKUP = _generate_field_name_check_lookup(MUTUALLY_EXCLUSIVE_FIELDS)


class Match(BaseModel):
    entries: Sequence[MatchEntry]


class Action(BaseModel):
    pass


class PolicyDefinitionSequenceBase(BaseModel):
    sequence_id: int = Field(default=0, serialization_alias="sequenceId", validation_alias="sequenceId")
    sequence_name: str = Field(serialization_alias="sequenceName", validation_alias="sequenceName")
    base_action: PolicyActionType = Field(
        default="drop", serialization_alias="baseAction", validation_alias="baseAction"
    )
    sequence_type: SequenceType = Field(serialization_alias="sequenceType", validation_alias="sequenceType")
    sequence_ip_type: Optional[SequenceIpType] = Field(
        default="ipv4", serialization_alias="sequenceIpType", validation_alias="sequenceIpType"
    )
    ruleset: Optional[bool] = None
    match: Match
    actions: Sequence[ActionEntry]

    @staticmethod
    def _check_field_collision(field: str, fields: Sequence[str]) -> None:
        existing_fields = set(fields)
        forbidden_fields = set(MUTUALLY_EXCLUSIVE_FIELD_LOOKUP.get(field, []))
        colliding_fields = set(existing_fields) & set(forbidden_fields)
        assert not colliding_fields, f"{field} is mutually exclusive with {colliding_fields}"

    def _check_match_can_be_inserted(self, match: MatchEntry) -> None:
        self._check_field_collision(
            match.field,
            [entry.field for entry in self.match.entries],
        )

    def _check_action_can_be_inserted_in_set(
        self, action: ActionSetEntry, action_set_param: List[ActionSetEntry]
    ) -> None:
        self._check_field_collision(
            action.field,
            [param.field for param in action_set_param],
        )

    def _get_match_entries_by_field(self, field: str) -> Sequence[MatchEntry]:
        return [entry for entry in self.match.entries if entry.field == field]

    def _remove_match(self, match_type: Any) -> None:
        if isinstance(self.match.entries, MutableSequence):
            self.match.entries[:] = [entry for entry in self.match.entries if type(entry) != match_type]

    def _insert_match(self, match: MatchEntry, insert_field_check: bool = True) -> int:
        # inserts new item or replaces item with same field name if found
        if insert_field_check:
            self._check_match_can_be_inserted(match)
        if isinstance(self.match.entries, MutableSequence):
            for index, entry in enumerate(self.match.entries):
                if match.field == entry.field:
                    self.match.entries[index] = match
                    return index
            self.match.entries.append(match)
            return len(self.match.entries) - 1
        else:
            raise TypeError("Match entries must be defined as MutableSequence (eg. List) to use _insert_match method")

    def _insert_action(self, action: ActionEntry) -> None:
        if isinstance(self.actions, MutableSequence):
            for index, entry in enumerate(self.actions):
                if action.type == entry.type:
                    self.actions[index] = action
                    return
            self.actions.append(action)
        else:
            raise TypeError("Action entries must be defined as MutableSequence (eg. List) to use _insert_match method")

    def _remove_action(self, action_type_name: str) -> None:
        if isinstance(self.actions, MutableSequence):
            self.actions[:] = [action for action in self.actions if action.type != action_type_name]

    def _insert_action_in_set(self, action: ActionSetEntry) -> None:
        if isinstance(self.actions, MutableSequence):
            # Check if ActionSet entry already exist
            action_sets = [act for act in self.actions if isinstance(act, ActionSet)]
            if len(action_sets) < 1:
                # if not found insert new empty ActionSet
                action_set = ActionSet()
                self.actions.append(action_set)
            else:
                action_set = action_sets[0]
            # Now we operate on action_set parameter list
            self._check_action_can_be_inserted_in_set(action, action_set.parameter)
            for index, param in enumerate(action_set.parameter):
                if action.field == param.field:
                    action_set.parameter[index] = action
                    return
            action_set.parameter.append(action)

    def _remove_action_from_set(self, field_name: str) -> None:
        if isinstance(self.actions, MutableSequence):
            for action in self.actions:
                if isinstance(action, ActionSet):
                    action.parameter[:] = [param for param in action.parameter if param.field != field_name]


def accept_action(method):
    @wraps(method)
    def wrapper(self: PolicyDefinitionSequenceBase, *args, **kwargs):
        assert self.base_action == "accept", f"{method.__name__} only allowed when base_action is accept"
        return method(self, *args, **kwargs)

    return wrapper


class DefaultAction(BaseModel):
    type: PolicyActionType


class InfoTag(BaseModel):
    info_tag: Optional[str] = Field("", serialization_alias="infoTag", validation_alias="infoTag")


class PolicyDefinitionId(BaseModel):
    definition_id: UUID = Field(serialization_alias="definitionId", validation_alias="definitionId")


class PolicyReference(BaseModel):
    id: UUID
    property: str


class DefinitionWithSequencesCommonBase(BaseModel):
    default_action: Optional[DefaultAction] = Field(
        default=DefaultAction(type="drop"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    sequences: Optional[Sequence[PolicyDefinitionSequenceBase]] = None

    def _enumerate_sequences(self, from_index: int = 0) -> None:
        """Updates sequence entries with appropriate index.

        Args:
            from_index (int, optional): Only rules after that index in table will be updated. Defaults to 0.
        """
        if isinstance(self.sequences, MutableSequence):
            start_index = from_index
            sequence_count = len(self.sequences)
            if from_index < 0:
                start_index = sequence_count - start_index
            for i in range(start_index, sequence_count):
                self.sequences[i].sequence_id = i + 1
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to use _enumerate_sequences method")

    def pop(self, index: int = -1) -> None:
        """Removes a sequence item at given index, consecutive sequence items will be enumarated again.

        Args:
            index (int, optional): Defaults to -1.
        """
        if isinstance(self.sequences, MutableSequence):
            self.sequences.pop(index)
            self._enumerate_sequences(index)
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to use pop method")

    def add(self, item: PolicyDefinitionSequenceBase) -> int:
        """Adds new sequence item as last in table, index will be autogenerated.

        Args:
            item (DefinitionSequence): item to be added to sequences

        Returns:
            int: index at which item was added
        """
        if isinstance(self.sequences, MutableSequence):
            insert_index = len(self.sequences)
            self.sequences.append(item)
            self._enumerate_sequences(insert_index)
            return insert_index
        else:
            raise TypeError("sequences be defined as MutableSequence (eg. List) to add method")


class PolicyDefinitionBase(BaseModel):
    name: str = Field(
        pattern="^[a-zA-Z0-9_-]{1,128}$",
        description="Can include only alpha-numeric characters, hyphen '-' or underscore '_'; maximum 128 characters",
    )
    description: str = "default description"
    type: str
    mode: Optional[str] = None
    optimized: Optional[Optimized] = "false"


class PolicyDefinitionInfo(PolicyDefinitionBase, PolicyDefinitionId):
    last_updated: datetime.datetime = Field(serialization_alias="lastUpdated", validation_alias="lastUpdated")
    owner: str
    reference_count: int = Field(serialization_alias="referenceCount", validation_alias="referenceCount")
    references: List[PolicyReference]


class PolicyDefinitionGetResponse(PolicyDefinitionInfo):
    is_activated_by_vsmart: bool = Field(
        serialization_alias="isActivatedByVsmart", validation_alias="isActivatedByVsmart"
    )


class PolicyDefinitionEditResponse(BaseModel):
    master_templates_affected: List[str] = Field(
        default=[], serialization_alias="masterTemplatesAffected", validation_alias="masterTemplatesAffected"
    )


class PolicyDefinitionPreview(BaseModel):
    preview: str
