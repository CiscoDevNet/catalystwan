# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import Any, List, Literal, Optional, Union, overload
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import EncapType, TLOCColor
from catalystwan.models.policy.policy_definition import (
    AffinityEntry,
    Carrier,
    CarrierEntry,
    ColorListEntry,
    CommunityAdditiveEntry,
    CommunityEntry,
    CommunityListEntry,
    DefaultAction,
    DefinitionWithSequencesCommonBase,
    DomainIDEntry,
    ExpandedCommunityListEntry,
    ExportToAction,
    GroupIDEntry,
    Match,
    MultiRegionRole,
    OMPTagEntry,
    OriginatorEntry,
    OriginEntry,
    OriginProtocol,
    PathType,
    PathTypeEntry,
    PolicyActionType,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    PreferenceEntry,
    PrefixListEntry,
    RegionEntry,
    RegionListEntry,
    RoleEntry,
    ServiceEntry,
    ServiceEntryValue,
    ServiceType,
    SiteEntry,
    SiteListEntry,
    TLOCActionEntry,
    TLOCActionType,
    TLOCEntry,
    TLOCEntryValue,
    TLOCListEntry,
    VPNListEntry,
    accept_action,
)

AnyControlPolicyRouteSequenceMatchEntry = Annotated[
    Union[
        ColorListEntry,
        CommunityListEntry,
        ExpandedCommunityListEntry,
        OMPTagEntry,
        OriginatorEntry,
        OriginEntry,
        PathTypeEntry,
        PreferenceEntry,
        PrefixListEntry,
        RegionEntry,
        RegionListEntry,
        RoleEntry,
        SiteEntry,
        SiteListEntry,
        SiteListEntry,
        TLOCEntry,
        TLOCListEntry,
        VPNListEntry,
    ],
    Field(discriminator="field"),
]

AnyControlPolicyTLOCSequenceMatchEntry = Annotated[
    Union[
        ColorListEntry,
        CommunityListEntry,
        CarrierEntry,
        ColorListEntry,
        DomainIDEntry,
        GroupIDEntry,
        OMPTagEntry,
        OriginatorEntry,
        PreferenceEntry,
        SiteEntry,
        SiteListEntry,
        RegionEntry,
        RegionListEntry,
        RoleEntry,
        TLOCListEntry,
        TLOCEntry,
    ],
    Field(discriminator="field"),
]

ControlPolicyRouteSequenceActions = Any  # TODO
ControlPolicyTLOCSequenceActions = Any  # TODO


class ControlPolicyHeader(PolicyDefinitionBase):
    type: Literal["control"] = "control"


class ControlPolicyRouteSequenceMatch(Match):
    entries: List[AnyControlPolicyRouteSequenceMatchEntry] = []


class ControlPolicyTLOCSequenceMatch(Match):
    entries: List[AnyControlPolicyTLOCSequenceMatchEntry] = []


class ControlPolicyRouteSequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["route"] = Field(
        default="route", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="reject", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: ControlPolicyRouteSequenceMatch = ControlPolicyRouteSequenceMatch()
    actions: List[ControlPolicyRouteSequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_color_list(self, color_list_id: UUID) -> None:
        self._insert_match(ColorListEntry(ref=color_list_id))

    def match_community_list(self, community_list_id: UUID) -> None:
        self._insert_match(CommunityListEntry(ref=community_list_id))

    def match_expanded_community_list(self, expanded_community_list_id: UUID) -> None:
        self._insert_match(ExpandedCommunityListEntry(ref=expanded_community_list_id))

    def match_omp_tag(self, omp_tag: int) -> None:
        self._insert_match(OMPTagEntry(value=str(omp_tag)))

    def match_origin(self, origin: OriginProtocol) -> None:
        self._insert_match(OriginEntry(value=origin))

    def match_originator(self, originator: IPv4Address) -> None:
        self._insert_match(OriginatorEntry(value=originator))

    def match_path_type(self, path_type: PathType) -> None:
        self._insert_match(PathTypeEntry(value=path_type))

    def match_preference(self, preference: int) -> None:
        self._insert_match(PreferenceEntry(value=str(preference)))

    def match_region(self, region_id: int, role: Optional[MultiRegionRole] = None) -> None:
        self._insert_match(RegionEntry(value=str(region_id)))
        if role is not None:
            self._insert_match(RoleEntry(value=role))
        else:
            self._remove_match(RoleEntry)

    def match_region_list(self, region_list_id: UUID, role: Optional[MultiRegionRole] = None) -> None:
        self._insert_match(RegionListEntry(ref=region_list_id))
        if role is not None:
            self._insert_match(RoleEntry(value=role))
        else:
            self._remove_match(RoleEntry)

    def match_site(self, site: int) -> None:
        self._insert_match(SiteEntry(value=str(site)))

    def match_site_list(self, site_list_id: UUID) -> None:
        self._insert_match(SiteListEntry(ref=site_list_id))

    def match_tloc_list(self, tloc_list_id: UUID) -> None:
        self._insert_match(TLOCListEntry(ref=tloc_list_id))

    def match_tloc(self, ip: IPv4Address, color: TLOCColor, encap: EncapType) -> None:
        self._insert_match(TLOCEntry(value=TLOCEntryValue(ip=ip, color=color, encap=encap)))

    def match_vpn_list(self, vpn_list_id: UUID) -> None:
        self._insert_match(VPNListEntry(ref=vpn_list_id))

    def match_prefix_list(self, prefix_list_id: UUID) -> None:
        self._insert_match(PrefixListEntry(ref=prefix_list_id))

    @accept_action
    def associate_community_action(self, community: str, additive: bool = False) -> None:
        self._insert_action_in_set(CommunityEntry(value=community))
        if additive:
            self._insert_action_in_set(CommunityAdditiveEntry())
        else:
            self._remove_action_from_set(CommunityAdditiveEntry().field)

    @accept_action
    def associate_omp_tag_action(self, omp_tag: int) -> None:
        self._insert_action_in_set(OMPTagEntry(value=str(omp_tag)))

    @accept_action
    def associate_preference_action(self, preference: int) -> None:
        self._insert_action_in_set(PreferenceEntry(value=str(preference)))

    @overload
    def associate_service_action(self, service_type: ServiceType, vpn: int, *, tloc_list_id: UUID) -> None:
        ...

    @overload
    def associate_service_action(
        self, service_type: ServiceType, vpn: int, *, ip: IPv4Address, color: TLOCColor, encap: EncapType
    ) -> None:
        ...

    @accept_action
    def associate_service_action(
        self, service_type=ServiceType, vpn=int, *, tloc_list_id=None, ip=None, color=None, encap=None
    ) -> None:
        if tloc_list_id is None:
            tloc_entry = TLOCEntryValue(ip=ip, color=color, encap=encap)
            tloc_list_entry = None
        else:
            tloc_entry = None
            tloc_list_entry = TLOCListEntry(ref=tloc_list_id)
        service_value = ServiceEntryValue(type=service_type, vpn=str(vpn), tloc=tloc_entry, tloc_list=tloc_list_entry)
        self._insert_action_in_set(ServiceEntry(value=service_value))

    @accept_action
    def associate_tloc_action(self, tloc_action: TLOCActionType) -> None:
        self._insert_action_in_set(TLOCActionEntry(value=tloc_action))

    @accept_action
    def associate_affinity_action(self, affinity: int) -> None:
        self._insert_action_in_set(AffinityEntry(value=str(affinity)))

    @accept_action
    def associate_export_to_action(self, vpn_list_id: UUID) -> None:
        self._insert_action(ExportToAction(parameter=VPNListEntry(ref=vpn_list_id)))


class ControlPolicyTLOCSequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["tloc"] = Field(
        default="tloc", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: PolicyActionType = Field(
        default="reject", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: ControlPolicyTLOCSequenceMatch = ControlPolicyTLOCSequenceMatch()
    actions: List[ControlPolicyTLOCSequenceActions] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_carrier(self, carrier: Carrier) -> None:
        self._insert_match(CarrierEntry(value=carrier))

    def match_color_list(self, color_list_id: UUID) -> None:
        self._insert_match(ColorListEntry(ref=color_list_id))

    def match_domain_id(self, domain_id: int) -> None:
        self._insert_match(DomainIDEntry(value=str(domain_id)))

    def match_group_id(self, group_id: int) -> None:
        self._insert_match(GroupIDEntry(value=str(group_id)))

    def match_omp_tag(self, omp_tag: int) -> None:
        self._insert_match(OMPTagEntry(value=str(omp_tag)))

    def match_originator(self, originator: IPv4Address) -> None:
        self._insert_match(OriginatorEntry(value=originator))

    def match_preference(self, preference: int) -> None:
        self._insert_match(PreferenceEntry(value=str(preference)))

    def match_site(self, site: int) -> None:
        self._insert_match(SiteEntry(value=str(site)))

    def match_site_list(self, site_list_id: UUID) -> None:
        self._insert_match(SiteListEntry(ref=site_list_id))

    def match_region(self, region_id: int, role: Optional[MultiRegionRole] = None) -> None:
        self._insert_match(RegionEntry(value=str(region_id)))
        if role is not None:
            self._insert_match(RoleEntry(value=role))
        else:
            self._remove_match(RoleEntry)

    def match_region_list(self, region_list_id: UUID, role: Optional[MultiRegionRole] = None) -> None:
        self._insert_match(RegionListEntry(ref=region_list_id))
        if role is not None:
            self._insert_match(RoleEntry(value=role))
        else:
            self._remove_match(RoleEntry)

    def match_tloc_list(self, tloc_list_id: UUID) -> None:
        self._insert_match(TLOCListEntry(ref=tloc_list_id))

    def match_tloc(self, ip: IPv4Address, color: TLOCColor, encap: EncapType) -> None:
        self._insert_match(TLOCEntry(value=TLOCEntryValue(ip=ip, color=color, encap=encap)))

    @accept_action
    def associate_omp_tag_action(self, omp_tag: int) -> None:
        self._insert_action_in_set(OMPTagEntry(value=str(omp_tag)))

    @accept_action
    def associate_preference_action(self, preference: int) -> None:
        self._insert_action_in_set(PreferenceEntry(value=str(preference)))

    @accept_action
    def associate_affinity_action(self, affinity: int) -> None:
        self._insert_action_in_set(AffinityEntry(value=str(affinity)))


AnyControlPolicySequence = Annotated[
    Union[ControlPolicyRouteSequence, ControlPolicyTLOCSequence],
    Field(discriminator="sequence_type"),
]


class ControlPolicy(ControlPolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[AnyControlPolicySequence] = []
    default_action: DefaultAction = Field(
        default=DefaultAction(type="reject"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_route_sequence(
        self, name: str = "Route", base_action: PolicyActionType = "reject"
    ) -> ControlPolicyRouteSequence:
        seq = ControlPolicyRouteSequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        self.add(seq)
        return seq

    def add_tloc_sequence(
        self, name: str = "TLOC", base_action: PolicyActionType = "reject"
    ) -> ControlPolicyTLOCSequence:
        seq = ControlPolicyTLOCSequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type="ipv4",
        )
        self.add(seq)
        return seq


class ControlPolicyEditPayload(ControlPolicy, PolicyDefinitionId):
    pass


class ControlPolicyGetResponse(ControlPolicy, PolicyDefinitionGetResponse):
    pass
