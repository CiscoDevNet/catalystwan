# Copyright 2024 Cisco Systems, Inc. and its affiliates

# This stub provide top-level "public" policy models to be used with PolicyAPI()
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.policy.list.app import AppList, AppListInfo
from catalystwan.models.policy.list.app_probe import AppProbeClassList, AppProbeClassListInfo
from catalystwan.models.policy.list.as_path import ASPathList, ASPathListInfo
from catalystwan.models.policy.list.class_map import ClassMapList, ClassMapListInfo
from catalystwan.models.policy.list.color import ColorList, ColorListInfo
from catalystwan.models.policy.list.communities import (
    CommunityList,
    CommunityListInfo,
    ExpandedCommunityList,
    ExpandedCommunityListInfo,
)
from catalystwan.models.policy.list.data_ipv6_prefix import DataIPv6PrefixList, DataIPv6PrefixListInfo
from catalystwan.models.policy.list.data_prefix import DataPrefixList, DataPrefixListInfo
from catalystwan.models.policy.list.fqdn import FQDNList, FQDNListInfo
from catalystwan.models.policy.list.geo_location import GeoLocationList, GeoLocationListInfo
from catalystwan.models.policy.list.ips_signature import IPSSignatureList, IPSSignatureListInfo
from catalystwan.models.policy.list.ipv6_prefix import IPv6PrefixList, IPv6PrefixListInfo
from catalystwan.models.policy.list.local_app import LocalAppList, LocalAppListInfo
from catalystwan.models.policy.list.local_domain import LocalDomainList, LocalDomainListInfo
from catalystwan.models.policy.list.mirror import MirrorList, MirrorListInfo
from catalystwan.models.policy.list.policer import PolicerList, PolicerListInfo
from catalystwan.models.policy.list.port import PortList, PortListInfo
from catalystwan.models.policy.list.preferred_color_group import PreferredColorGroupList, PreferredColorGroupListInfo
from catalystwan.models.policy.list.prefix import PrefixList, PrefixListInfo
from catalystwan.models.policy.list.protocol_name import ProtocolNameList, ProtocolNameListInfo
from catalystwan.models.policy.list.region import RegionList, RegionListInfo
from catalystwan.models.policy.list.site import SiteList, SiteListInfo
from catalystwan.models.policy.list.sla import SLAClassList, SLAClassListInfo
from catalystwan.models.policy.list.tloc import TLOCList, TLOCListInfo
from catalystwan.models.policy.list.url import URLAllowList, URLAllowListInfo, URLBlockList, URLBlockListInfo
from catalystwan.models.policy.list.vpn import VPNList, VPNListInfo
from catalystwan.models.policy.list.zone import ZoneList, ZoneListInfo

from .centralized import CentralizedPolicy, TrafficDataDirection
from .definition.access_control_list import AclPolicy, AclPolicyGetResponse
from .definition.access_control_list_ipv6 import AclIPv6Policy, AclIPv6PolicyGetResponse
from .definition.control import ControlPolicy, ControlPolicyGetResponse
from .definition.device_access import DeviceAccessPolicy, DeviceAccessPolicyGetResponse
from .definition.device_access_ipv6 import DeviceAccessIPv6Policy, DeviceAccessIPv6PolicyGetResponse
from .definition.hub_and_spoke import HubAndSpokePolicy, HubAndSpokePolicyGetResponse
from .definition.mesh import MeshPolicy, MeshPolicyGetResponse
from .definition.qos_map import QoSDropType, QoSMapPolicy, QoSMapPolicyGetResponse
from .definition.rewrite import RewritePolicy, RewritePolicyGetResponse
from .definition.rule_set import RuleSet, RuleSetGetResponse
from .definition.security_group import SecurityGroup, SecurityGroupGetResponse
from .definition.traffic_data import TrafficDataPolicy, TrafficDataPolicyGetResponse
from .definition.vpn_membership import VPNMembershipPolicy, VPNMembershipPolicyGetResponse
from .definition.zone_based_firewall import ZoneBasedFWPolicy, ZoneBasedFWPolicyGetResponse
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
        AclIPv6Policy,
        AclPolicy,
        ControlPolicy,
        DeviceAccessIPv6Policy,
        DeviceAccessPolicy,
        HubAndSpokePolicy,
        MeshPolicy,
        QoSMapPolicy,
        RewritePolicy,
        RuleSet,
        SecurityGroup,
        TrafficDataPolicy,
        VPNMembershipPolicy,
        ZoneBasedFWPolicy,
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

AnyPolicyListInfo = Annotated[
    Union[
        AppListInfo,
        AppProbeClassListInfo,
        ASPathListInfo,
        ClassMapListInfo,
        ColorListInfo,
        CommunityListInfo,
        DataIPv6PrefixListInfo,
        DataPrefixListInfo,
        ExpandedCommunityListInfo,
        FQDNListInfo,
        GeoLocationListInfo,
        IPSSignatureListInfo,
        IPv6PrefixListInfo,
        LocalAppListInfo,
        LocalDomainListInfo,
        MirrorListInfo,
        PolicerListInfo,
        PortListInfo,
        PreferredColorGroupListInfo,
        PrefixListInfo,
        ProtocolNameListInfo,
        RegionListInfo,
        SiteListInfo,
        SLAClassListInfo,
        TLOCListInfo,
        URLAllowListInfo,
        URLBlockListInfo,
        VPNListInfo,
        ZoneListInfo,
    ],
    Field(discriminator="type"),
]

AnyPolicyDefinitionInfo = Annotated[
    Union[
        AclIPv6PolicyGetResponse,
        AclPolicyGetResponse,
        ControlPolicyGetResponse,
        DeviceAccessIPv6PolicyGetResponse,
        DeviceAccessPolicyGetResponse,
        HubAndSpokePolicyGetResponse,
        MeshPolicyGetResponse,
        QoSMapPolicyGetResponse,
        RewritePolicyGetResponse,
        RuleSetGetResponse,
        SecurityGroupGetResponse,
        TrafficDataPolicyGetResponse,
        VPNMembershipPolicyGetResponse,
        ZoneBasedFWPolicyGetResponse,
    ],
    Field(discriminator="type"),
]


__all__ = (
    "AclIPv6Policy",
    "AclPolicy",
    "AnyPolicyList",
    "AnyPolicyDefinitionInfo",
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
    "PathType",
    "PLPEntryType",
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
