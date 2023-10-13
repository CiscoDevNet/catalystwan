from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Sequence, Type, Union, overload

from vmngclient.endpoints.configuration.policy.definition_builder.data import (
    ConfigurationPolicyDataDefinitionBuilder,
    DataPolicy,
    DataPolicyGetResponse,
)
from vmngclient.endpoints.configuration.policy.definition_builder.rule_set import (
    ConfigurationPolicyRuleSetDefinitionBuilder,
    RuleSetInfo,
)
from vmngclient.endpoints.configuration.policy.definition_builder.security_group import (
    ConfigurationPolicySecurityGroupDefinitionBuilder,
    SecurityGroupInfo,
)
from vmngclient.endpoints.configuration.policy.definition_builder.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinitionBuilder,
    ZoneBasedFWPolicyGetResponse,
    ZoneBasedFWPolicyInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.app import (
    AppListInfo,
    ConfigurationPolicyApplicationListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.app_probe import (
    AppProbeClassListInfo,
    ConfigurationPolicyAppProbeClassListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.as_path import (
    ASPathListInfo,
    ConfigurationPolicyASPathListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.class_map import (
    ClassMapListInfo,
    ConfigurationPolicyForwardingClassListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.color import (
    ColorListInfo,
    ConfigurationPolicyColorListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.community import (
    CommunityListInfo,
    ConfigurationPolicyCommunityListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.data_ipv6_prefix import (
    ConfigurationPolicyDataIPv6PrefixListBuilder,
    DataIPv6PrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.data_prefix import (
    ConfigurationPolicyDataPrefixListBuilder,
    DataPrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.expanded_community import (
    ConfigurationPolicyExpandedCommunityListBuilder,
    ExpandedCommunityListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.fqdn import ConfigurationPolicyFQDNListBuilder, FQDNListInfo
from vmngclient.endpoints.configuration.policy.list_builder.geo_location import (
    ConfigurationPolicyGeoLocationListBuilder,
    GeoLocationListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.ips_signature import (
    ConfigurationPolicyIPSSignatureListBuilder,
    IPSSignatureListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.ipv6_prefix import (
    ConfigurationPolicyIPv6PrefixListBuilder,
    IPv6PrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.local_app import (
    ConfigurationPolicyLocalAppListBuilder,
    LocalAppListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.local_domain import (
    ConfigurationPolicyLocalDomainListBuilder,
    LocalDomainListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.mirror import (
    ConfigurationPolicyMirrorListBuilder,
    MirrorListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.policer import (
    ConfigurationPolicyPolicerClassListBuilder,
    PolicerListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.port import ConfigurationPolicyPortListBuilder, PortListInfo
from vmngclient.endpoints.configuration.policy.list_builder.preferred_color_group import (
    ConfigurationPreferredColorGroupListBuilder,
    PreferredColorGroupListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.prefix import (
    ConfigurationPolicyPrefixListBuilder,
    PrefixListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.protocol_name import (
    ConfigurationPolicyProtocolNameListBuilder,
    ProtocolNameListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.site import ConfigurationPolicySiteListBuilder, SiteListInfo
from vmngclient.endpoints.configuration.policy.list_builder.sla import (
    ConfigurationPolicySLAClassListBuilder,
    SLAClassListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.tloc import ConfigurationPolicyTLOCListBuilder, TLOCListInfo
from vmngclient.endpoints.configuration.policy.list_builder.url_black_list import (
    ConfigurationPolicyURLBlackListBuilder,
    URLBlackListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.url_white_list import (
    ConfigurationPolicyURLWhiteListBuilder,
    URLWhiteListInfo,
)
from vmngclient.endpoints.configuration.policy.list_builder.vpn import ConfigurationPolicyVPNListBuilder, VPNListInfo
from vmngclient.endpoints.configuration.policy.list_builder.zone import ConfigurationPolicyZoneListBuilder, ZoneListInfo
from vmngclient.model.policy.definitions.rule_set import RuleSet
from vmngclient.model.policy.definitions.security_group import SecurityGroup
from vmngclient.model.policy.definitions.zone_based_firewall import ZoneBasedFWPolicy
from vmngclient.model.policy.lists import (
    AllPolicyLists,
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
    SiteList,
    SLAClassList,
    TLOCList,
    URLBlackList,
    URLWhiteList,
    VPNList,
    ZoneList,
)
from vmngclient.model.policy.policy_definition import (
    PolicyDefinitionBuilder,
    PolicyDefinitionEditResponse,
    PolicyDefinitionInfo,
)
from vmngclient.model.policy.policy_list import PolicyListBuilder, PolicyListInfo
from vmngclient.typed_list import DataSequence

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


POLICY_LIST_BUILDER_MAP: Mapping[type, type] = {
    AppList: ConfigurationPolicyApplicationListBuilder,
    AppProbeClassList: ConfigurationPolicyAppProbeClassListBuilder,
    ASPathList: ConfigurationPolicyASPathListBuilder,
    ClassMapList: ConfigurationPolicyForwardingClassListBuilder,
    ColorList: ConfigurationPolicyColorListBuilder,
    CommunityList: ConfigurationPolicyCommunityListBuilder,
    DataIPv6PrefixList: ConfigurationPolicyDataIPv6PrefixListBuilder,
    DataPrefixList: ConfigurationPolicyDataPrefixListBuilder,
    ExpandedCommunityList: ConfigurationPolicyExpandedCommunityListBuilder,
    FQDNList: ConfigurationPolicyFQDNListBuilder,
    GeoLocationList: ConfigurationPolicyGeoLocationListBuilder,
    IPSSignatureList: ConfigurationPolicyIPSSignatureListBuilder,
    IPv6PrefixList: ConfigurationPolicyIPv6PrefixListBuilder,
    LocalAppList: ConfigurationPolicyLocalAppListBuilder,
    LocalDomainList: ConfigurationPolicyLocalDomainListBuilder,
    MirrorList: ConfigurationPolicyMirrorListBuilder,
    PolicerList: ConfigurationPolicyPolicerClassListBuilder,
    PortList: ConfigurationPolicyPortListBuilder,
    PreferredColorGroupList: ConfigurationPreferredColorGroupListBuilder,
    PrefixList: ConfigurationPolicyPrefixListBuilder,
    ProtocolNameList: ConfigurationPolicyProtocolNameListBuilder,
    SiteList: ConfigurationPolicySiteListBuilder,
    SLAClassList: ConfigurationPolicySLAClassListBuilder,
    TLOCList: ConfigurationPolicyTLOCListBuilder,
    URLBlackList: ConfigurationPolicyURLBlackListBuilder,
    URLWhiteList: ConfigurationPolicyURLWhiteListBuilder,
    VPNList: ConfigurationPolicyVPNListBuilder,
    ZoneList: ConfigurationPolicyZoneListBuilder,
}

POLICY_DEFINITION_BUILDER_MAP: Mapping[type, type] = {
    RuleSet: ConfigurationPolicyRuleSetDefinitionBuilder,
    SecurityGroup: ConfigurationPolicySecurityGroupDefinitionBuilder,
    ZoneBasedFWPolicy: ConfigurationPolicyZoneBasedFirewallDefinitionBuilder,
    DataPolicy: ConfigurationPolicyDataDefinitionBuilder,
}

SupportedPolicyDefinitions = Union[RuleSet, SecurityGroup, ZoneBasedFWPolicy, DataPolicy]


class PolicyBuilder:
    def __init__(self, session: vManageSession):
        self.session = session

    def __get_list_builder_instance(self, payload_type: type) -> PolicyListBuilder:
        builder_class = POLICY_LIST_BUILDER_MAP.get(payload_type)
        if builder_class is None:
            raise TypeError(f"Unsupported policy list type: {payload_type}")
        return builder_class(self.session)

    def __get_definition_builder_instance(self, payload_type: type) -> PolicyDefinitionBuilder:
        builder_class = POLICY_DEFINITION_BUILDER_MAP.get(payload_type)
        if builder_class is None:
            raise TypeError(f"Unsupported policy definition type: {payload_type}")
        return builder_class(self.session)

    def create_policy_list(self, policy_list: AllPolicyLists) -> str:
        builder = self.__get_list_builder_instance(type(policy_list))
        return builder.create_policy_list(payload=policy_list).list_id

    def edit_policy_list(self, id: str, policy_list: AllPolicyLists) -> None:
        builder = self.__get_list_builder_instance(type(policy_list))
        builder.edit_policy_list(id=id, payload=policy_list)

    def delete_policy_list(self, type: Type[AllPolicyLists], id: str) -> None:
        builder = self.__get_list_builder_instance(type)
        builder.delete_policy_list(id=id)

    def create_policy_definition(self, policy_definition: SupportedPolicyDefinitions) -> str:
        builder = self.__get_definition_builder_instance(type(policy_definition))
        return builder.create_policy_definition(payload=policy_definition).definition_id

    def edit_policy_definition(
        self, id: str, policy_definition: SupportedPolicyDefinitions
    ) -> PolicyDefinitionEditResponse:
        builder = self.__get_definition_builder_instance(type(policy_definition))
        return builder.edit_policy_definition(id=id, payload=policy_definition)

    def delete_policy_definition(self, type: Type[SupportedPolicyDefinitions], id: str) -> None:
        builder = self.__get_definition_builder_instance(type)
        builder.delete_policy_definition(id=id)

    @overload
    def get_policy_lists(self, type: Type[AppList]) -> DataSequence[AppListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[AppProbeClassList]) -> DataSequence[AppProbeClassListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ASPathList]) -> DataSequence[ASPathListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ClassMapList]) -> DataSequence[ClassMapListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ColorList]) -> DataSequence[ColorListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[CommunityList]) -> DataSequence[CommunityListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[DataIPv6PrefixList]) -> DataSequence[DataIPv6PrefixListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[DataPrefixList]) -> DataSequence[DataPrefixListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ExpandedCommunityList]) -> DataSequence[ExpandedCommunityListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[FQDNList]) -> DataSequence[FQDNListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[GeoLocationList]) -> DataSequence[GeoLocationListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[IPSSignatureList]) -> DataSequence[IPSSignatureListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[IPv6PrefixList]) -> DataSequence[IPv6PrefixListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[LocalAppList]) -> DataSequence[LocalAppListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[LocalDomainList]) -> DataSequence[LocalDomainListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[MirrorList]) -> DataSequence[MirrorListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[PolicerList]) -> DataSequence[PolicerListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[PortList]) -> DataSequence[PortListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[PreferredColorGroupList]) -> DataSequence[PreferredColorGroupListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[PrefixList]) -> DataSequence[PrefixListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ProtocolNameList]) -> DataSequence[ProtocolNameListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[SiteList]) -> DataSequence[SiteListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[SLAClassList]) -> DataSequence[SLAClassListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[TLOCList]) -> DataSequence[TLOCListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[URLBlackList]) -> DataSequence[URLBlackListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[URLWhiteList]) -> DataSequence[URLWhiteListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[VPNList]) -> DataSequence[VPNListInfo]:
        ...

    @overload
    def get_policy_lists(self, type: Type[ZoneList]) -> DataSequence[ZoneListInfo]:
        ...

    def get_policy_lists(self, type: Type[AllPolicyLists]) -> Sequence[PolicyListInfo]:
        builder = self.__get_list_builder_instance(type)
        return builder.get_policy_lists()

    @overload
    def get_lists_by_id(self, type: Type[AppList], id: str) -> AppListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[AppProbeClassList], id: str) -> AppProbeClassListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ASPathList], id: str) -> ASPathListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ClassMapList], id: str) -> ClassMapListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ColorList], id: str) -> ColorListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[CommunityList], id: str) -> CommunityListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[DataIPv6PrefixList], id: str) -> DataIPv6PrefixListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[DataPrefixList], id: str) -> DataPrefixListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ExpandedCommunityList], id: str) -> ExpandedCommunityListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[FQDNList], id: str) -> FQDNListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[GeoLocationList], id: str) -> GeoLocationListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[IPSSignatureList], id: str) -> IPSSignatureListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[IPv6PrefixList], id: str) -> IPv6PrefixListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[LocalAppList], id: str) -> LocalAppListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[LocalDomainList], id: str) -> LocalDomainListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[MirrorList], id: str) -> MirrorListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[PolicerList], id: str) -> PolicerListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[PortList], id: str) -> PortListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[PreferredColorGroupList], id: str) -> PreferredColorGroupListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[PrefixList], id: str) -> PrefixListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ProtocolNameList], id: str) -> ProtocolNameListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[SiteList], id: str) -> SiteListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[SLAClassList], id: str) -> SLAClassListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[TLOCList], id: str) -> TLOCListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[URLBlackList], id: str) -> URLBlackListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[URLWhiteList], id: str) -> URLWhiteListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[VPNList], id: str) -> VPNListInfo:
        ...

    @overload
    def get_lists_by_id(self, type: Type[ZoneList], id: str) -> ZoneListInfo:
        ...

    def get_lists_by_id(self, type: Type[AllPolicyLists], id: str) -> PolicyListInfo:
        builder = self.__get_list_builder_instance(type)
        return builder.get_lists_by_id(id=id)

    @overload
    def get_definitions(self, type: Type[DataPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[RuleSet]) -> DataSequence[RuleSetInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[SecurityGroup]) -> DataSequence[SecurityGroupInfo]:
        ...

    @overload
    def get_definitions(self, type: Type[ZoneBasedFWPolicy]) -> DataSequence[ZoneBasedFWPolicyInfo]:
        ...

    def get_definitions(self, type: Type[SupportedPolicyDefinitions]) -> Sequence[PolicyDefinitionInfo]:
        builder = self.__get_definition_builder_instance(type)
        return builder.get_definitions()

    @overload
    def get_policy_definition(self, type: Type[DataPolicy], id: str) -> DataPolicyGetResponse:
        ...

    @overload
    def get_policy_definition(self, type: Type[RuleSet], id: str) -> RuleSetInfo:
        ...

    @overload
    def get_policy_definition(self, type: Type[SecurityGroup], id: str) -> SecurityGroupInfo:
        ...

    @overload
    def get_policy_definition(self, type: Type[ZoneBasedFWPolicy], id: str) -> ZoneBasedFWPolicyGetResponse:
        ...

    def get_policy_definition(self, type: Type[SupportedPolicyDefinitions], id: str) -> Any:
        builder = self.__get_definition_builder_instance(type)
        return builder.get_policy_definition(id=id)
