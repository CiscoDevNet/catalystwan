# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network
from typing import Any, List, Literal, Optional, Set, Tuple, Union, overload
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import EncapType, ICMPMessageType, ServiceChainNumber, TLOCColor
from catalystwan.models.policy.policy_definition import (
    AppListEntry,
    CFlowDAction,
    CountAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataIPv6PrefixListEntry,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationRegionEntry,
    DNSAppListEntry,
    DNSEntry,
    DNSTypeEntryType,
    DREOptimizationAction,
    DSCPEntry,
    FallBackToRoutingAction,
    ForwardingClassEntry,
    ICMPMessageEntry,
    LocalTLOCListEntry,
    LocalTLOCListEntryValue,
    LogAction,
    LossProtectionAction,
    LossProtectionFECAction,
    LossProtectionPacketDuplicationAction,
    LossProtectionType,
    Match,
    NATAction,
    NextHopEntry,
    NextHopLooseEntry,
    PacketLengthEntry,
    PLPEntry,
    PolicerListEntry,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    PrefferedColorGroupListEntry,
    ProtocolEntry,
    RedirectDNSAction,
    SecureInternetGatewayAction,
    ServiceChainEntry,
    ServiceChainEntryValue,
    ServiceNodeGroupAction,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    TCPEntry,
    TCPOptimizationAction,
    TLOCEntry,
    TLOCEntryValue,
    TLOCListEntry,
    TrafficToEntry,
    VPNEntry,
    accept_action,
)

TrafficDataPolicySequenceEntry = Annotated[
    Union[
        AppListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationDataPrefixListEntry,
        DestinationIPEntry,
        DestinationPortEntry,
        DestinationRegionEntry,
        DNSAppListEntry,
        DNSEntry,
        DSCPEntry,
        ICMPMessageEntry,
        PacketLengthEntry,
        PLPEntry,
        ProtocolEntry,
        SourceDataIPv6PrefixListEntry,
        SourceDataPrefixListEntry,
        SourceIPEntry,
        SourcePortEntry,
        TCPEntry,
        TrafficToEntry,
    ],
    Field(discriminator="field"),
]

TrafficDataPolicySequenceActions = Any  # TODO


class TrafficDataPolicyHeader(PolicyDefinitionBase):
    type: Literal["data"] = "data"


class TrafficDataPolicySequenceMatch(Match):
    entries: List[TrafficDataPolicySequenceEntry] = []


class TrafficDataPolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["applicationFirewall", "qos", "serviceChaining", "trafficEngineering", "data"] = Field(
        default="data", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    match: TrafficDataPolicySequenceMatch = TrafficDataPolicySequenceMatch()
    actions: List[TrafficDataPolicySequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_app_list(self, app_list_id: UUID) -> None:
        self._insert_match(AppListEntry(ref=app_list_id))

    def match_dns_app_list(self, dns_app_list_id: UUID) -> None:
        self._insert_match(DNSAppListEntry(ref=dns_app_list_id))

    def match_dns_request(self) -> None:
        self._insert_match(DNSEntry(value="request"))

    def match_dns_response(self) -> None:
        self._insert_match(DNSEntry(value="response"))

    def match_dscp(self, dscp: int) -> None:
        self._insert_match(DSCPEntry(value=str(dscp)))

    def match_icmp(self, icmp_message_types: List[ICMPMessageType]) -> None:
        self._insert_match(ICMPMessageEntry(value=icmp_message_types))

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

    def match_primary_destination_region(self) -> None:
        self._insert_match(DestinationRegionEntry(value="primary-region"))

    def match_secondary_destination_region(self) -> None:
        self._insert_match(DestinationRegionEntry(value="secondary-region"))

    def match_other_destination_region(self) -> None:
        self._insert_match(DestinationRegionEntry(value="other-region"))

    def match_destination_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_tcp(self) -> None:
        self._insert_match(TCPEntry())

    def match_traffic_to_access(self) -> None:
        self._insert_match(TrafficToEntry(value="access"))

    def match_traffic_to_core(self) -> None:
        self._insert_match(TrafficToEntry(value="core"))

    def match_traffic_to_service(self) -> None:
        self._insert_match(TrafficToEntry(value="service"))

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))

    def associate_log_action(self) -> None:
        self._insert_action(LogAction())

    @accept_action
    def associate_dscp_action(self, dscp: int) -> None:
        self._insert_action_in_set(DSCPEntry(value=str(dscp)))

    @accept_action
    def associate_forwarding_class_action(self, fwclass: str) -> None:
        self._insert_action_in_set(ForwardingClassEntry(value=fwclass))

    @accept_action
    def associate_local_tloc_action(self, color: TLOCColor, encap: EncapType, restrict: bool = False) -> None:
        tloc_entry = LocalTLOCListEntry(
            value=LocalTLOCListEntryValue(
                color=color,
                encap=encap,
                restrict="" if restrict else None,
            )
        )
        self._insert_action_in_set(tloc_entry)

    @accept_action
    def associate_preffered_color_group(self, color_group_list_id: UUID, restrict: bool = False) -> None:
        self._insert_action_in_set(PrefferedColorGroupListEntry(ref=color_group_list_id, color_restrict=restrict))

    @accept_action
    def associate_cflowd_action(self) -> None:
        self._insert_action(CFlowDAction())

    @overload
    def associate_nat_action(self, *, nat_pool: int) -> None:
        ...

    @overload
    def associate_nat_action(self, *, vpn_fallback: bool = False, vpn: int = 0) -> None:
        ...

    @accept_action
    def associate_nat_action(self, *, nat_pool: Optional[int] = None, vpn_fallback: bool = False, vpn: int = 0) -> None:
        if nat_pool:
            nat_action = NATAction.from_nat_pool(nat_pool=nat_pool)
        else:
            nat_action = NATAction.from_nat_vpn(fallback=vpn_fallback, vpn=vpn)
        self._insert_action(nat_action)

    @accept_action
    def associate_next_hop_action(self, next_hop: IPv4Address, loose: bool = False) -> None:
        self._insert_action_in_set(NextHopEntry(value=next_hop))
        self._insert_action_in_set(NextHopLooseEntry(value="true" if loose else "false"))

    @accept_action
    def associate_policer_list_action(self, policer_list_id: UUID) -> None:
        self._insert_action_in_set(PolicerListEntry(ref=policer_list_id))

    @overload
    def associate_redirect_dns_action(self, *, ip: IPv4Address) -> None:
        ...

    @overload
    def associate_redirect_dns_action(self, *, dns_type: DNSTypeEntryType = "host") -> None:
        ...

    @accept_action
    def associate_redirect_dns_action(self, *, ip=None, dns_type=None) -> None:
        if ip:
            redirect_dns_action = RedirectDNSAction.from_ip_address(ip)
        else:
            redirect_dns_action = RedirectDNSAction.from_dns_type(dns_type)
        self._insert_action(redirect_dns_action)

    @accept_action
    def associate_local_service_chain_action(
        self, sc_type: ServiceChainNumber, vpn: int, restrict: bool = False
    ) -> None:
        self._insert_action_in_set(
            ServiceChainEntry(
                value=ServiceChainEntryValue(
                    type=sc_type,
                    vpn=str(vpn),
                    restrict="" if restrict else None,
                    local="",
                )
            )
        )

    @accept_action
    def associate_remote_service_chain_action(
        self,
        sc_type: ServiceChainNumber,
        vpn: int,
        ip: IPv4Address,
        color: TLOCColor,
        encap: EncapType,
        restrict: bool = False,
    ) -> None:
        self._insert_action_in_set(
            ServiceChainEntry(
                value=ServiceChainEntryValue(
                    type=sc_type,
                    vpn=str(vpn),
                    restrict="" if restrict else None,
                    tloc=TLOCEntryValue(
                        ip=ip,
                        color=color,
                        encap=encap,
                    ),
                )
            )
        )

    @accept_action
    def associate_app_qoe_optimization_action(
        self, tcp: bool = False, dre: bool = False, service_node_group: Optional[str] = None
    ) -> None:
        if tcp:
            self._insert_action(TCPOptimizationAction())
        else:
            self._remove_action(TCPOptimizationAction().type)
        if dre:
            self._insert_action(DREOptimizationAction())
        else:
            self._remove_action(DREOptimizationAction().type)
        if service_node_group is not None:
            self._insert_action(ServiceNodeGroupAction(parameter=service_node_group))
        else:
            self._remove_action(ServiceNodeGroupAction().type)

    @accept_action
    def associate_loss_correction_fec_action(self, adaptive: bool = False, threshold: Optional[int] = None) -> None:
        self._remove_action(LossProtectionPacketDuplicationAction().type)
        fec_type: LossProtectionType = "fecAdaptive" if adaptive else "fecAlways"
        fec_value = str(threshold) if adaptive and threshold is not None else None
        self._insert_action(LossProtectionAction(parameter=fec_type))
        self._insert_action(LossProtectionFECAction(parameter=fec_type, value=fec_value))

    @accept_action
    def associate_loss_correction_packet_duplication_action(self) -> None:
        self._remove_action(LossProtectionFECAction().type)
        self._insert_action(LossProtectionAction(parameter="packetDuplication"))
        self._insert_action(LossProtectionPacketDuplicationAction())

    @accept_action
    def associate_vpn_action(self, vpn: int) -> None:
        # TLOC or Next Hop is mandatory when configuring VPN. Please populate Action > TLOC or Action > Next Hop
        self._insert_action_in_set(VPNEntry(value=str(vpn)))

    @overload
    def associate_tloc_action(self, *, tloc_list_id: UUID) -> None:
        ...

    @overload
    def associate_tloc_action(self, *, ip: IPv4Address, color: TLOCColor, encap: EncapType) -> None:
        ...

    @accept_action
    def associate_tloc_action(self, *, tloc_list_id=None, ip=None, color=None, encap=None) -> None:
        # VPN is mandatory when configuring TLOC. Please populate Action > VPN.
        if tloc_list_id is not None:
            self._insert_action_in_set(TLOCListEntry(ref=tloc_list_id))
        else:
            self._insert_action_in_set(
                TLOCEntry(
                    value=TLOCEntryValue(
                        ip=ip,
                        color=color,
                        encap=encap,
                    )
                )
            )

    @accept_action
    def associate_secure_internet_gateway_action(self, fallback_to_routing: bool = False) -> None:
        # Secure Internet Gateway cannot be enabled with NAT Pool or NAT VPN or Next Hop.
        self._insert_action(SecureInternetGatewayAction())
        if fallback_to_routing:
            self._insert_action(FallBackToRoutingAction())
        else:
            self._remove_action(FallBackToRoutingAction().type)


class TrafficDataPolicy(TrafficDataPolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[TrafficDataPolicySequence] = []
    model_config = ConfigDict(populate_by_name=True)

    def add_ipv4_sequence(
        self, name: str = "Custom", base_action: PolicyActionType = "drop", log: bool = False
    ) -> TrafficDataPolicySequence:
        seq = TrafficDataPolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        self.add(seq)
        return seq


class TrafficDataPolicyEditPayload(TrafficDataPolicy, PolicyDefinitionId):
    pass


class TrafficDataPolicyGetResponse(TrafficDataPolicy, PolicyDefinitionGetResponse):
    pass
