# This stub provide top-level "public" policy models and enums to be used with PolicyAPI()
# TODO: explore model attribute access customization with https://peps.python.org/pep-0562/
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .centralized import CentralizedPolicy, TrafficDataDirectionEnum
from .definitions.access_control_list import AclPolicy
from .definitions.access_control_list_ipv6 import AclIPv6Policy
from .definitions.control import ControlPolicy
from .definitions.device_access import DeviceAccessPolicy
from .definitions.device_access_ipv6 import DeviceAccessIPv6Policy
from .definitions.hub_and_spoke import HubAndSpokePolicy
from .definitions.mesh import MeshPolicy
from .definitions.qos_map import QoSDropEnum, QoSMapPolicy
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
    URLBlackList,
    URLWhiteList,
    VPNList,
    ZoneList,
)
from .lists_entries import EncapEnum, PathPreferenceEnum, PolicerExceedActionEnum
from .localized import LocalizedPolicy
from .policy_definition import (
    CarrierEnum,
    DNSTypeEntryEnum,
    MultiRegionRoleEnum,
    OriginProtocolEnum,
    PathTypeEnum,
    PLPEntryEnum,
    PolicyActionTypeEnum,
    ServiceTypeEnum,
    TLOCActionEnum,
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
        URLBlackList,
        URLWhiteList,
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
    "CarrierEnum",
    "CentralizedPolicy",
    "ClassMapList",
    "ColorList",
    "CommunityList",
    "ControlPolicy",
    "DataIPv6PrefixList",
    "DataPrefixList",
    "DeviceAccessIPv6Policy",
    "DeviceAccessPolicy",
    "DNSTypeEntryEnum",
    "EncapEnum",
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
    "MultiRegionRoleEnum",
    "OriginProtocolEnum",
    "PathPreferenceEnum",
    "PathTypeEnum",
    "PLPEntryEnum",
    "PolicerExceedActionEnum",
    "PolicerList",
    "PolicyActionTypeEnum",
    "PortList",
    "PreferredColorGroupList",
    "PrefixList",
    "ProtocolNameList",
    "QoSDropEnum",
    "QoSMapPolicy",
    "RegionList",
    "RewritePolicy",
    "RuleSet",
    "SecurityGroup",
    "SecurityPolicy",
    "ServiceTypeEnum",
    "SiteList",
    "SLAClassList",
    "TLOCActionEnum",
    "TLOCList",
    "TrafficDataDirectionEnum",
    "TrafficDataPolicy",
    "UnifiedSecurityPolicy",
    "URLBlackList",
    "URLWhiteList",
    "VPNList",
    "VPNMembershipPolicy",
    "ZoneBasedFWPolicy",
    "ZoneList",
)


def __dir__() -> "List[str]":
    return list(__all__)
