# Copyright 2024 Cisco Systems, Inc. and its affiliates

# This stub provide top-level "public" policy models to be used with PolicyAPI()
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.policy.list.app import AppList
from catalystwan.models.policy.list.app_probe import AppProbeClassList
from catalystwan.models.policy.list.as_path import ASPathList
from catalystwan.models.policy.list.class_map import ClassMapList
from catalystwan.models.policy.list.color import ColorList
from catalystwan.models.policy.list.communities import CommunityList, ExpandedCommunityList
from catalystwan.models.policy.list.data_ipv6_prefix import DataIPv6PrefixList
from catalystwan.models.policy.list.data_prefix import DataPrefixList
from catalystwan.models.policy.list.fqdn import FQDNList
from catalystwan.models.policy.list.geo_location import GeoLocationList
from catalystwan.models.policy.list.ips_signature import IPSSignatureList
from catalystwan.models.policy.list.ipv6_prefix import IPv6PrefixList
from catalystwan.models.policy.list.local_app import LocalAppList
from catalystwan.models.policy.list.local_domain import LocalDomainList
from catalystwan.models.policy.list.mirror import MirrorList
from catalystwan.models.policy.list.policer import PolicerList
from catalystwan.models.policy.list.port import PortList
from catalystwan.models.policy.list.preferred_color_group import PreferredColorGroupList
from catalystwan.models.policy.list.prefix import PrefixList
from catalystwan.models.policy.list.protocol_name import ProtocolNameList
from catalystwan.models.policy.list.region import RegionList
from catalystwan.models.policy.list.site import SiteList
from catalystwan.models.policy.list.sla import SLAClassList

from .centralized import CentralizedPolicy, TrafficDataDirection
from .definition.access_control_list import AclPolicy
from .definition.access_control_list_ipv6 import AclIPv6Policy
from .definition.control import ControlPolicy
from .definition.device_access import DeviceAccessPolicy
from .definition.device_access_ipv6 import DeviceAccessIPv6Policy
from .definition.hub_and_spoke import HubAndSpokePolicy
from .definition.mesh import MeshPolicy
from .definition.qos_map import QoSDropType, QoSMapPolicy
from .definition.rewrite import RewritePolicy
from .definition.rule_set import RuleSet
from .definition.security_group import SecurityGroup
from .definition.traffic_data import TrafficDataPolicy
from .definition.vpn_membership import VPNMembershipPolicy
from .definition.zone_based_firewall import ZoneBasedFWPolicy
from .lists import TLOCList, URLAllowList, URLBlockList, VPNList, ZoneList
from .lists_entries import PathPreference, PolicerExceedAction
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
