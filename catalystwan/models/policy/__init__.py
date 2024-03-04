# Copyright 2024 Cisco Systems, Inc. and its affiliates

# This stub provide top-level "public" policy models to be used with PolicyAPI()
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .centralized import CentralizedPolicy, TrafficDataDirection
from .definitions.access_control_list import AclPolicy
from .definitions.access_control_list_ipv6 import AclIPv6Policy
from .definitions.control import ControlPolicy
from .definitions.device_access import DeviceAccessPolicy
from .definitions.device_access_ipv6 import DeviceAccessIPv6Policy
from .definitions.hub_and_spoke import HubAndSpokePolicy
from .definitions.mesh import MeshPolicy
from .definitions.qos_map import QoSDropType, QoSMapPolicy
from .definitions.rewrite import RewritePolicy
from .definitions.rule_set import RuleSet
from .definitions.security_group import SecurityGroup
from .definitions.traffic_data import TrafficDataPolicy
from .definitions.vpn_membership import VPNMembershipPolicy
from .definitions.zone_based_firewall import ZoneBasedFWPolicy
from .lists import (
    AppList,
    AppProbeClassList,
    ASPathList,
    ClassMapList,
    ColorList,
    CommunityList,
    DataIPv6PrefixList,
    DataPrefixList,
    ExpandedCommunityList,
    FQDNList,
    GeoLocationList,
    IPSSignatureList,
    IPv6PrefixList,
    LocalAppList,
    LocalDomainList,
    MirrorList,
    PolicerList,
    PortList,
    PreferredColorGroupList,
    PrefixList,
    ProtocolNameList,
    RegionList,
    SiteList,
    SLAClassList,
    TLOCList,
    URLAllowList,
    URLBlockList,
    VPNList,
    ZoneList,
)
from .lists_entries import EncapType, PathPreference, PolicerExceedAction
from .localized import LocalizedPolicy
from .policy_definition import (
    Carrier,
    DNSTypeEntryType,
    MultiRegionRole,
    OriginProtocol,
    PathType,
    PLPEntryType,
    PolicyActionType,
    ServiceType,
    TLOCActionType,
)
from .security import SecurityPolicy, UnifiedSecurityPolicy

AnyPolicyDefinition = Annotated[
    Union[
        RuleSet,
        SecurityGroup,
        ZoneBasedFWPolicy,
        TrafficDataPolicy,
        QoSMapPolicy,
        RewritePolicy,
        ControlPolicy,
        VPNMembershipPolicy,
        HubAndSpokePolicy,
        MeshPolicy,
        AclPolicy,
        AclIPv6Policy,
        DeviceAccessPolicy,
        DeviceAccessIPv6Policy,
    ],
    Field(discriminator="type"),
]

AnyPolicyList = Annotated[
    Union[
        AppList,
        AppProbeClassList,
        ASPathList,
        ClassMapList,
        ColorList,
        CommunityList,
        DataIPv6PrefixList,
        DataPrefixList,
        ExpandedCommunityList,
        FQDNList,
        GeoLocationList,
        IPSSignatureList,
        IPv6PrefixList,
        LocalAppList,
        LocalDomainList,
        MirrorList,
        PolicerList,
        PortList,
        PreferredColorGroupList,
        PrefixList,
        ProtocolNameList,
        RegionList,
        SiteList,
        SLAClassList,
        TLOCList,
        URLBlockList,
        URLAllowList,
        VPNList,
        ZoneList,
    ],
    Field(discriminator="type"),
]


__all__ = (
    "AclIPv6Policy",
    "AclPolicy",
    "AnyPolicyList",
    "AnyPolicyList",
    "AppList",
    "AppProbeClassList",
    "ASPathList",
    "Carrier",
    "CentralizedPolicy",
    "ClassMapList",
    "ColorList",
    "CommunityList",
    "ControlPolicy",
    "DataIPv6PrefixList",
    "DataPrefixList",
    "DeviceAccessIPv6Policy",
    "DeviceAccessPolicy",
    "DNSTypeEntryType",
    "EncapType",
    "ExpandedCommunityList",
    "FQDNList",
    "GeoLocationList",
    "HubAndSpokePolicy",
    "IPSSignatureList",
    "IPv6PrefixList",
    "LocalAppList",
    "LocalDomainList",
    "LocalizedPolicy",
    "MeshPolicy",
    "MirrorList",
    "MultiRegionRole",
    "OriginProtocol",
    "PathPreference",
    "PathType",
    "PLPEntryType",
    "PolicerExceedAction",
    "PolicerList",
    "PolicyActionType",
    "PortList",
    "PreferredColorGroupList",
    "PrefixList",
    "ProtocolNameList",
    "QoSDropType",
    "QoSMapPolicy",
    "RegionList",
    "RewritePolicy",
    "RuleSet",
    "SecurityGroup",
    "SecurityPolicy",
    "ServiceType",
    "SiteList",
    "SLAClassList",
    "TLOCActionType",
    "TLOCList",
    "TrafficDataDirection",
    "TrafficDataPolicy",
    "UnifiedSecurityPolicy",
    "URLBlockList",
    "URLAllowList",
    "VPNList",
    "VPNMembershipPolicy",
    "ZoneBasedFWPolicy",
    "ZoneList",
)


def __dir__() -> "List[str]":
    return list(__all__)
