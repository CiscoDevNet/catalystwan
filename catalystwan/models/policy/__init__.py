# This stub provide top-level "public" policy models and enums to be used with PolicyAPI()
# TODO: explore model attribute access customization with https://peps.python.org/pep-0562/
from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from .centralized import CentralizedPolicy as CentralizedPolicy
from .centralized import TrafficDataDirectionEnum as TrafficDataDirectionEnum
from .definitions.access_control_list import AclPolicy as AclPolicy
from .definitions.access_control_list_ipv6 import AclIPv6Policy as AclIPv6Policy
from .definitions.control import ControlPolicy as ControlPolicy
from .definitions.device_access import DeviceAccessPolicy as DeviceAccessPolicy
from .definitions.device_access_ipv6 import DeviceAccessIPv6Policy as DeviceAccessIPv6Policy
from .definitions.hub_and_spoke import HubAndSpokePolicy as HubAndSpokePolicy
from .definitions.mesh import MeshPolicy as MeshPolicy
from .definitions.qos_map import QoSDropEnum as QoSDropEnum
from .definitions.qos_map import QoSMapPolicy as QoSMapPolicy
from .definitions.rewrite import RewritePolicy as RewritePolicy
from .definitions.rule_set import RuleSet as RuleSet
from .definitions.security_group import SecurityGroup as SecurityGroup
from .definitions.traffic_data import TrafficDataPolicy as TrafficDataPolicy
from .definitions.vpn_membership import VPNMembershipPolicy as VPNMembershipPolicy
from .definitions.zone_based_firewall import ZoneBasedFWPolicy as ZoneBasedFWPolicy
from .lists import AppList as AppList
from .lists import AppProbeClassList as AppProbeClassList
from .lists import ASPathList as ASPathList
from .lists import ClassMapList as ClassMapList
from .lists import ColorList as ColorList
from .lists import CommunityList as CommunityList
from .lists import DataIPv6PrefixList as DataIPv6PrefixList
from .lists import DataPrefixList as DataPrefixList
from .lists import ExpandedCommunityList as ExpandedCommunityList
from .lists import FQDNList as FQDNList
from .lists import GeoLocationList as GeoLocationList
from .lists import IPSSignatureList as IPSSignatureList
from .lists import IPv6PrefixList as IPv6PrefixList
from .lists import LocalAppList as LocalAppList
from .lists import LocalDomainList as LocalDomainList
from .lists import MirrorList as MirrorList
from .lists import PolicerList as PolicerList
from .lists import PortList as PortList
from .lists import PreferredColorGroupList as PreferredColorGroupList
from .lists import PrefixList as PrefixList
from .lists import ProtocolNameList as ProtocolNameList
from .lists import RegionList as RegionList
from .lists import SiteList as SiteList
from .lists import SLAClassList as SLAClassList
from .lists import TLOCList as TLOCList
from .lists import URLBlackList as URLBlackList
from .lists import URLWhiteList as URLWhiteList
from .lists import VPNList as VPNList
from .lists import ZoneList as ZoneList
from .lists_entries import EncapEnum as EncapEnum
from .lists_entries import PathPreferenceEnum as PathPreferenceEnum
from .lists_entries import PolicerExceedActionEnum as PolicerExceedActionEnum
from .localized import LocalizedPolicy as LocalizedPolicy
from .policy_definition import CarrierEnum as CarrierEnum
from .policy_definition import DNSTypeEntryEnum as DNSTypeEntryEnum
from .policy_definition import MultiRegionRoleEnum as MultiRegionRoleEnum
from .policy_definition import OriginProtocolEnum as OriginProtocolEnum
from .policy_definition import PathTypeEnum as PathTypeEnum
from .policy_definition import PLPEntryEnum as PLPEntryEnum
from .policy_definition import PolicyActionTypeEnum as PolicyActionTypeEnum
from .policy_definition import ServiceTypeEnum as ServiceTypeEnum
from .policy_definition import TLOCActionEnum as TLOCActionEnum
from .security import SecurityPolicy as SecurityPolicy
from .security import UnifiedSecurityPolicy as UnifiedSecurityPolicy

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
