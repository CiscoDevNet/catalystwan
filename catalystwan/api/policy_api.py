# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Type, overload
from uuid import UUID

from catalystwan.api.task_status_api import Task
from catalystwan.endpoints.configuration.policy.definition.access_control_list import (
    AclPolicyGetResponse,
    ConfigurationPolicyAclDefinition,
)
from catalystwan.endpoints.configuration.policy.definition.access_control_list_ipv6 import (
    AclIPv6PolicyGetResponse,
    ConfigurationPolicyAclIPv6Definition,
)
from catalystwan.endpoints.configuration.policy.definition.control import (
    ConfigurationPolicyControlDefinition,
    ControlPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.device_access import (
    ConfigurationPolicyDeviceAccessDefinition,
    DeviceAccessPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.device_access_ipv6 import (
    ConfigurationPolicyDeviceAccessIPv6Definition,
    DeviceAccessIPv6PolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.hub_and_spoke import (
    ConfigurationPolicyHubAndSpokeDefinition,
    HubAndSpokePolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.mesh import (
    ConfigurationPolicyMeshDefinition,
    MeshPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.qos_map import (
    ConfigurationPolicyQoSMapDefinition,
    QoSMapPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.rewrite import (
    ConfigurationPolicyRewriteRuleDefinition,
    RewritePolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.rule_set import (
    ConfigurationPolicyRuleSetDefinition,
    RuleSetGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.security_group import (
    ConfigurationPolicySecurityGroupDefinition,
    SecurityGroupGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.traffic_data import (
    ConfigurationPolicyDataDefinition,
    TrafficDataPolicy,
    TrafficDataPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.vpn_membership import (
    ConfigurationPolicyVPNMembershipGroupDefinition,
    VPNMembershipPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.definition.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinition,
    ZoneBasedFWPolicyGetResponse,
)
from catalystwan.endpoints.configuration.policy.list.app import AppListInfo, ConfigurationPolicyApplicationList
from catalystwan.endpoints.configuration.policy.list.app_probe import (
    AppProbeClassListInfo,
    ConfigurationPolicyAppProbeClassList,
)
from catalystwan.endpoints.configuration.policy.list.as_path import ASPathListInfo, ConfigurationPolicyASPathList
from catalystwan.endpoints.configuration.policy.list.class_map import (
    ClassMapListInfo,
    ConfigurationPolicyForwardingClassList,
)
from catalystwan.endpoints.configuration.policy.list.color import ColorListInfo, ConfigurationPolicyColorList
from catalystwan.endpoints.configuration.policy.list.community import (
    CommunityListInfo,
    ConfigurationPolicyCommunityList,
)
from catalystwan.endpoints.configuration.policy.list.data_ipv6_prefix import (
    ConfigurationPolicyDataIPv6PrefixList,
    DataIPv6PrefixListInfo,
)
from catalystwan.endpoints.configuration.policy.list.data_prefix import (
    ConfigurationPolicyDataPrefixList,
    DataPrefixListInfo,
)
from catalystwan.endpoints.configuration.policy.list.expanded_community import (
    ConfigurationPolicyExpandedCommunityList,
    ExpandedCommunityListInfo,
)
from catalystwan.endpoints.configuration.policy.list.fqdn import ConfigurationPolicyFQDNList, FQDNListInfo
from catalystwan.endpoints.configuration.policy.list.geo_location import (
    ConfigurationPolicyGeoLocationList,
    GeoLocationListInfo,
)
from catalystwan.endpoints.configuration.policy.list.ips_signature import (
    ConfigurationPolicyIPSSignatureList,
    IPSSignatureListInfo,
)
from catalystwan.endpoints.configuration.policy.list.ipv6_prefix import (
    ConfigurationPolicyIPv6PrefixList,
    IPv6PrefixListInfo,
)
from catalystwan.endpoints.configuration.policy.list.local_app import ConfigurationPolicyLocalAppList, LocalAppListInfo
from catalystwan.endpoints.configuration.policy.list.local_domain import (
    ConfigurationPolicyLocalDomainList,
    LocalDomainListInfo,
)
from catalystwan.endpoints.configuration.policy.list.mirror import ConfigurationPolicyMirrorList, MirrorListInfo
from catalystwan.endpoints.configuration.policy.list.policer import ConfigurationPolicyPolicerClassList, PolicerListInfo
from catalystwan.endpoints.configuration.policy.list.port import ConfigurationPolicyPortList, PortListInfo
from catalystwan.endpoints.configuration.policy.list.preferred_color_group import (
    ConfigurationPreferredColorGroupList,
    PreferredColorGroupListInfo,
)
from catalystwan.endpoints.configuration.policy.list.prefix import ConfigurationPolicyPrefixList, PrefixListInfo
from catalystwan.endpoints.configuration.policy.list.protocol_name import (
    ConfigurationPolicyProtocolNameList,
    ProtocolNameListInfo,
)
from catalystwan.endpoints.configuration.policy.list.region import ConfigurationPolicyRegionList, RegionListInfo
from catalystwan.endpoints.configuration.policy.list.site import ConfigurationPolicySiteList, SiteListInfo
from catalystwan.endpoints.configuration.policy.list.sla import ConfigurationPolicySLAClassList, SLAClassListInfo
from catalystwan.endpoints.configuration.policy.list.tloc import ConfigurationPolicyTLOCList, TLOCListInfo
from catalystwan.endpoints.configuration.policy.list.url_allow_list import (
    ConfigurationPolicyURLAllowList,
    URLAllowListInfo,
)
from catalystwan.endpoints.configuration.policy.list.url_block_list import (
    ConfigurationPolicyURLBlockList,
    URLBlockListInfo,
)
from catalystwan.endpoints.configuration.policy.list.vpn import ConfigurationPolicyVPNList, VPNListInfo
from catalystwan.endpoints.configuration.policy.list.zone import ConfigurationPolicyZoneList, ZoneListInfo
from catalystwan.endpoints.configuration.policy.security_template import ConfigurationSecurityTemplatePolicy
from catalystwan.endpoints.configuration.policy.vedge_template import ConfigurationVEdgeTemplatePolicy
from catalystwan.endpoints.configuration.policy.vsmart_template import (
    ConfigurationVSmartTemplatePolicy,
    VSmartConnectivityStatus,
)
from catalystwan.models.misc.application_protocols import ApplicationProtocol
from catalystwan.models.policy import AnyPolicyDefinition, AnyPolicyList
from catalystwan.models.policy.centralized import CentralizedPolicy, CentralizedPolicyEditPayload, CentralizedPolicyInfo
from catalystwan.models.policy.definitions.access_control_list import AclPolicy
from catalystwan.models.policy.definitions.access_control_list_ipv6 import AclIPv6Policy
from catalystwan.models.policy.definitions.control import ControlPolicy
from catalystwan.models.policy.definitions.device_access import DeviceAccessPolicy
from catalystwan.models.policy.definitions.device_access_ipv6 import DeviceAccessIPv6Policy
from catalystwan.models.policy.definitions.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definitions.mesh import MeshPolicy
from catalystwan.models.policy.definitions.qos_map import QoSMapPolicy
from catalystwan.models.policy.definitions.rewrite import RewritePolicy
from catalystwan.models.policy.definitions.rule_set import RuleSet
from catalystwan.models.policy.definitions.security_group import SecurityGroup
from catalystwan.models.policy.definitions.vpn_membership import VPNMembershipPolicy
from catalystwan.models.policy.definitions.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.models.policy.lists import (
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
    PolicyListBase,
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
from catalystwan.models.policy.localized import (
    LocalizedPolicy,
    LocalizedPolicyDeviceInfo,
    LocalizedPolicyEditResponse,
    LocalizedPolicyInfo,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionEditResponse,
    PolicyDefinitionEndpoints,
    PolicyDefinitionInfo,
)
from catalystwan.models.policy.policy_list import PolicyListEndpoints
from catalystwan.models.policy.security import (
    AnySecurityPolicy,
    AnySecurityPolicyInfo,
    SecurityPolicy,
    SecurityPolicyEditResponse,
    UnifiedSecurityPolicy,
)
from catalystwan.typed_list import DataSequence

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


POLICY_LIST_ENDPOINTS_MAP: Mapping[type, type] = {
    AppList: ConfigurationPolicyApplicationList,
    AppProbeClassList: ConfigurationPolicyAppProbeClassList,
    ASPathList: ConfigurationPolicyASPathList,
    ClassMapList: ConfigurationPolicyForwardingClassList,
    ColorList: ConfigurationPolicyColorList,
    CommunityList: ConfigurationPolicyCommunityList,
    DataIPv6PrefixList: ConfigurationPolicyDataIPv6PrefixList,
    DataPrefixList: ConfigurationPolicyDataPrefixList,
    ExpandedCommunityList: ConfigurationPolicyExpandedCommunityList,
    FQDNList: ConfigurationPolicyFQDNList,
    GeoLocationList: ConfigurationPolicyGeoLocationList,
    IPSSignatureList: ConfigurationPolicyIPSSignatureList,
    IPv6PrefixList: ConfigurationPolicyIPv6PrefixList,
    LocalAppList: ConfigurationPolicyLocalAppList,
    LocalDomainList: ConfigurationPolicyLocalDomainList,
    MirrorList: ConfigurationPolicyMirrorList,
    PolicerList: ConfigurationPolicyPolicerClassList,
    PortList: ConfigurationPolicyPortList,
    PreferredColorGroupList: ConfigurationPreferredColorGroupList,
    PrefixList: ConfigurationPolicyPrefixList,
    ProtocolNameList: ConfigurationPolicyProtocolNameList,
    RegionList: ConfigurationPolicyRegionList,
    SiteList: ConfigurationPolicySiteList,
    SLAClassList: ConfigurationPolicySLAClassList,
    TLOCList: ConfigurationPolicyTLOCList,
    URLBlockList: ConfigurationPolicyURLBlockList,
    URLAllowList: ConfigurationPolicyURLAllowList,
    VPNList: ConfigurationPolicyVPNList,
    ZoneList: ConfigurationPolicyZoneList,
}

POLICY_DEFINITION_ENDPOINTS_MAP: Mapping[type, type] = {
    RuleSet: ConfigurationPolicyRuleSetDefinition,
    SecurityGroup: ConfigurationPolicySecurityGroupDefinition,
    ZoneBasedFWPolicy: ConfigurationPolicyZoneBasedFirewallDefinition,
    TrafficDataPolicy: ConfigurationPolicyDataDefinition,
    QoSMapPolicy: ConfigurationPolicyQoSMapDefinition,
    RewritePolicy: ConfigurationPolicyRewriteRuleDefinition,
    ControlPolicy: ConfigurationPolicyControlDefinition,
    VPNMembershipPolicy: ConfigurationPolicyVPNMembershipGroupDefinition,
    HubAndSpokePolicy: ConfigurationPolicyHubAndSpokeDefinition,
    MeshPolicy: ConfigurationPolicyMeshDefinition,
    AclPolicy: ConfigurationPolicyAclDefinition,
    AclIPv6Policy: ConfigurationPolicyAclIPv6Definition,
    DeviceAccessPolicy: ConfigurationPolicyDeviceAccessDefinition,
    DeviceAccessIPv6Policy: ConfigurationPolicyDeviceAccessIPv6Definition,
}


class CentralizedPolicyAPI:
    def __init__(self, session: ManagerSession):
        self._session = session
        self._endpoints = ConfigurationVSmartTemplatePolicy(session)

    def activate(self, id: UUID) -> Task:
        task_id = self._endpoints.activate_policy(id).id
        return Task(self._session, task_id)

    def deactivate(self, id: UUID) -> Task:
        task_id = self._endpoints.deactivate_policy(id).id
        return Task(self._session, task_id)

    def create(self, policy: CentralizedPolicy) -> UUID:
        return self._endpoints.create_vsmart_template(policy).policy_id

    def edit(self, policy: CentralizedPolicyEditPayload, lock_checks: bool = True) -> None:
        if lock_checks:
            self._endpoints.edit_vsmart_template(policy.policy_id, policy)
        self._endpoints.edit_template_without_lock_checks(policy.policy_id, policy)

    def delete(self, id: UUID) -> None:
        self._endpoints.delete_vsmart_template(id)

    @overload
    def get(self) -> DataSequence[CentralizedPolicyInfo]:
        ...

    @overload
    def get(self, id: UUID) -> CentralizedPolicy:
        ...

    def get(self, id: Optional[UUID] = None) -> Any:
        if id is not None:
            return self._endpoints.get_template_by_policy_id(id)
        return self._endpoints.generate_vsmart_policy_template_list()

    def check_vsmart_connectivity(self) -> DataSequence[VSmartConnectivityStatus]:
        return self._endpoints.check_vsmart_connectivity_status()


class LocalizedPolicyAPI:
    def __init__(self, session: ManagerSession):
        self._session = session
        self._endpoints = ConfigurationVEdgeTemplatePolicy(session)

    def create(self, policy: LocalizedPolicy) -> UUID:
        return self._endpoints.create_vedge_template(policy).policy_id

    def edit(self, id: UUID, policy: LocalizedPolicy) -> LocalizedPolicyEditResponse:
        return self._endpoints.edit_vedge_template(id, policy)

    def delete(self, id: UUID) -> None:
        self._endpoints.delete_vedge_template(id)

    @overload
    def get(self) -> DataSequence[LocalizedPolicyInfo]:
        ...

    @overload
    def get(self, id: UUID) -> LocalizedPolicy:
        ...

    def get(self, id: Optional[UUID] = None) -> Any:
        if id is not None:
            return self._endpoints.get_vedge_template(id)
        return self._endpoints.generate_policy_template_list()

    def list_devices(self, id: Optional[UUID] = None) -> DataSequence[LocalizedPolicyDeviceInfo]:
        if id is not None:
            return self._endpoints.get_device_list_by_policy(id)
        return self._endpoints.get_vedge_policy_device_list()

    def preview(self, id: UUID) -> str:
        return self._endpoints.preview_by_id(id).preview


class SecurityPolicyAPI:
    def __init__(self, session: ManagerSession):
        self._session = session
        self._endpoints = ConfigurationSecurityTemplatePolicy(session)

    def create(self, policy: AnySecurityPolicy) -> UUID:
        # POST does not return anything! we need to list all after creation and find by name to get id
        self._endpoints.create_security_template(policy)
        policy_infos = [
            info.root
            for info in self._endpoints.generate_security_template_list()
            if info.root.policy_name == policy.policy_name
        ]
        assert len(policy_infos) == 1
        return policy_infos[0].policy_id

    def edit(self, id: UUID, policy: AnySecurityPolicy) -> SecurityPolicyEditResponse:
        return self._endpoints.edit_security_template(id, policy)

    def delete(self, id: UUID) -> None:
        self._endpoints.delete_security_template(id)

    @overload
    def get(self) -> List[AnySecurityPolicyInfo]:
        ...

    @overload
    def get(self, id: UUID) -> AnySecurityPolicy:
        ...

    def get(self, id: Optional[UUID] = None) -> Any:
        if id is not None:
            return self._endpoints.get_security_template(id).root
        return [info.root for info in self._endpoints.generate_security_template_list()]


class PolicyListsAPI:
    def __init__(self, session: ManagerSession):
        self._session = session

    def __get_list_endpoints_instance(self, payload_type: type) -> PolicyListEndpoints:
        endpoints_class = POLICY_LIST_ENDPOINTS_MAP.get(payload_type)
        if endpoints_class is None:
            raise TypeError(f"Unsupported policy list type: {payload_type}")
        return endpoints_class(self._session)

    def create(self, policy_list: AnyPolicyList) -> UUID:
        endpoints = self.__get_list_endpoints_instance(type(policy_list))
        return endpoints.create_policy_list(payload=policy_list).list_id

    def edit(self, id: UUID, policy_list: AnyPolicyList) -> None:
        endpoints = self.__get_list_endpoints_instance(type(policy_list))
        endpoints.edit_policy_list(id=id, payload=policy_list)

    def delete(self, type: Type[AnyPolicyList], id: UUID) -> None:
        endpoints = self.__get_list_endpoints_instance(type)
        endpoints.delete_policy_list(id=id)

    @overload
    def get(self, type: Type[AppList]) -> DataSequence[AppListInfo]:
        ...

    @overload
    def get(self, type: Type[AppProbeClassList]) -> DataSequence[AppProbeClassListInfo]:
        ...

    @overload
    def get(self, type: Type[ASPathList]) -> DataSequence[ASPathListInfo]:
        ...

    @overload
    def get(self, type: Type[ClassMapList]) -> DataSequence[ClassMapListInfo]:
        ...

    @overload
    def get(self, type: Type[ColorList]) -> DataSequence[ColorListInfo]:
        ...

    @overload
    def get(self, type: Type[CommunityList]) -> DataSequence[CommunityListInfo]:
        ...

    @overload
    def get(self, type: Type[DataIPv6PrefixList]) -> DataSequence[DataIPv6PrefixListInfo]:
        ...

    @overload
    def get(self, type: Type[DataPrefixList]) -> DataSequence[DataPrefixListInfo]:
        ...

    @overload
    def get(self, type: Type[ExpandedCommunityList]) -> DataSequence[ExpandedCommunityListInfo]:
        ...

    @overload
    def get(self, type: Type[FQDNList]) -> DataSequence[FQDNListInfo]:
        ...

    @overload
    def get(self, type: Type[GeoLocationList]) -> DataSequence[GeoLocationListInfo]:
        ...

    @overload
    def get(self, type: Type[IPSSignatureList]) -> DataSequence[IPSSignatureListInfo]:
        ...

    @overload
    def get(self, type: Type[IPv6PrefixList]) -> DataSequence[IPv6PrefixListInfo]:
        ...

    @overload
    def get(self, type: Type[LocalAppList]) -> DataSequence[LocalAppListInfo]:
        ...

    @overload
    def get(self, type: Type[LocalDomainList]) -> DataSequence[LocalDomainListInfo]:
        ...

    @overload
    def get(self, type: Type[MirrorList]) -> DataSequence[MirrorListInfo]:
        ...

    @overload
    def get(self, type: Type[PolicerList]) -> DataSequence[PolicerListInfo]:
        ...

    @overload
    def get(self, type: Type[PortList]) -> DataSequence[PortListInfo]:
        ...

    @overload
    def get(self, type: Type[PreferredColorGroupList]) -> DataSequence[PreferredColorGroupListInfo]:
        ...

    @overload
    def get(self, type: Type[PrefixList]) -> DataSequence[PrefixListInfo]:
        ...

    @overload
    def get(self, type: Type[ProtocolNameList]) -> DataSequence[ProtocolNameListInfo]:
        ...

    @overload
    def get(self, type: Type[RegionList]) -> DataSequence[RegionListInfo]:
        ...

    @overload
    def get(self, type: Type[SiteList]) -> DataSequence[SiteListInfo]:
        ...

    @overload
    def get(self, type: Type[SLAClassList]) -> DataSequence[SLAClassListInfo]:
        ...

    @overload
    def get(self, type: Type[TLOCList]) -> DataSequence[TLOCListInfo]:
        ...

    @overload
    def get(self, type: Type[URLBlockList]) -> DataSequence[URLBlockListInfo]:
        ...

    @overload
    def get(self, type: Type[URLAllowList]) -> DataSequence[URLAllowListInfo]:
        ...

    @overload
    def get(self, type: Type[VPNList]) -> DataSequence[VPNListInfo]:
        ...

    @overload
    def get(self, type: Type[ZoneList]) -> DataSequence[ZoneListInfo]:
        ...

    # get by id

    @overload
    def get(self, type: Type[AppList], id: UUID) -> AppListInfo:
        ...

    @overload
    def get(self, type: Type[AppProbeClassList], id: UUID) -> AppProbeClassListInfo:
        ...

    @overload
    def get(self, type: Type[ASPathList], id: UUID) -> ASPathListInfo:
        ...

    @overload
    def get(self, type: Type[ClassMapList], id: UUID) -> ClassMapListInfo:
        ...

    @overload
    def get(self, type: Type[ColorList], id: UUID) -> ColorListInfo:
        ...

    @overload
    def get(self, type: Type[CommunityList], id: UUID) -> CommunityListInfo:
        ...

    @overload
    def get(self, type: Type[DataIPv6PrefixList], id: UUID) -> DataIPv6PrefixListInfo:
        ...

    @overload
    def get(self, type: Type[DataPrefixList], id: UUID) -> DataPrefixListInfo:
        ...

    @overload
    def get(self, type: Type[ExpandedCommunityList], id: UUID) -> ExpandedCommunityListInfo:
        ...

    @overload
    def get(self, type: Type[FQDNList], id: UUID) -> FQDNListInfo:
        ...

    @overload
    def get(self, type: Type[GeoLocationList], id: UUID) -> GeoLocationListInfo:
        ...

    @overload
    def get(self, type: Type[IPSSignatureList], id: UUID) -> IPSSignatureListInfo:
        ...

    @overload
    def get(self, type: Type[IPv6PrefixList], id: UUID) -> IPv6PrefixListInfo:
        ...

    @overload
    def get(self, type: Type[LocalAppList], id: UUID) -> LocalAppListInfo:
        ...

    @overload
    def get(self, type: Type[LocalDomainList], id: UUID) -> LocalDomainListInfo:
        ...

    @overload
    def get(self, type: Type[MirrorList], id: UUID) -> MirrorListInfo:
        ...

    @overload
    def get(self, type: Type[PolicerList], id: UUID) -> PolicerListInfo:
        ...

    @overload
    def get(self, type: Type[PortList], id: UUID) -> PortListInfo:
        ...

    @overload
    def get(self, type: Type[PreferredColorGroupList], id: UUID) -> PreferredColorGroupListInfo:
        ...

    @overload
    def get(self, type: Type[PrefixList], id: UUID) -> PrefixListInfo:
        ...

    @overload
    def get(self, type: Type[ProtocolNameList], id: UUID) -> ProtocolNameListInfo:
        ...

    @overload
    def get(self, type: Type[RegionList], id: UUID) -> RegionListInfo:
        ...

    @overload
    def get(self, type: Type[SiteList], id: UUID) -> SiteListInfo:
        ...

    @overload
    def get(self, type: Type[SLAClassList], id: UUID) -> SLAClassListInfo:
        ...

    @overload
    def get(self, type: Type[TLOCList], id: UUID) -> TLOCListInfo:
        ...

    @overload
    def get(self, type: Type[URLBlockList], id: UUID) -> URLBlockListInfo:
        ...

    @overload
    def get(self, type: Type[URLAllowList], id: UUID) -> URLAllowListInfo:
        ...

    @overload
    def get(self, type: Type[VPNList], id: UUID) -> VPNListInfo:
        ...

    @overload
    def get(self, type: Type[ZoneList], id: UUID) -> ZoneListInfo:
        ...

    def get(self, type: Type[AnyPolicyList], id: Optional[UUID] = None) -> Any:
        endpoints = self.__get_list_endpoints_instance(type)
        if id is not None:
            return endpoints.get_lists_by_id(id=id)
        return endpoints.get_policy_lists()


class PolicyDefinitionsAPI:
    def __init__(self, session: ManagerSession):
        self._session = session

    def __get_definition_endpoints_instance(self, payload_type: type) -> PolicyDefinitionEndpoints:
        endpoints_class = POLICY_DEFINITION_ENDPOINTS_MAP.get(payload_type)
        if endpoints_class is None:
            raise TypeError(f"Unsupported policy definition type: {payload_type}")
        return endpoints_class(self._session)

    def create(self, policy_definition: AnyPolicyDefinition) -> UUID:
        endpoints = self.__get_definition_endpoints_instance(type(policy_definition))
        return endpoints.create_policy_definition(payload=policy_definition).definition_id

    def edit(self, id: UUID, policy_definition: AnyPolicyDefinition) -> PolicyDefinitionEditResponse:
        endpoints = self.__get_definition_endpoints_instance(type(policy_definition))
        return endpoints.edit_policy_definition(id=id, payload=policy_definition)

    def delete(self, type: Type[AnyPolicyDefinition], id: UUID) -> None:
        endpoints = self.__get_definition_endpoints_instance(type)
        endpoints.delete_policy_definition(id=id)

    @overload
    def get(self, type: Type[TrafficDataPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[RuleSet]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[SecurityGroup]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[ZoneBasedFWPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[QoSMapPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[RewritePolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[ControlPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[VPNMembershipPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[HubAndSpokePolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[MeshPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[AclPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[AclIPv6Policy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[DeviceAccessPolicy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @overload
    def get(self, type: Type[DeviceAccessIPv6Policy]) -> DataSequence[PolicyDefinitionInfo]:
        ...

    # get by id

    @overload
    def get(self, type: Type[TrafficDataPolicy], id: UUID) -> TrafficDataPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[RuleSet], id: UUID) -> RuleSetGetResponse:
        ...

    @overload
    def get(self, type: Type[SecurityGroup], id: UUID) -> SecurityGroupGetResponse:
        ...

    @overload
    def get(self, type: Type[ZoneBasedFWPolicy], id: UUID) -> ZoneBasedFWPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[QoSMapPolicy], id: UUID) -> QoSMapPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[RewritePolicy], id: UUID) -> RewritePolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[ControlPolicy], id: UUID) -> ControlPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[VPNMembershipPolicy], id: UUID) -> VPNMembershipPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[HubAndSpokePolicy], id: UUID) -> HubAndSpokePolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[MeshPolicy], id: UUID) -> MeshPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[AclPolicy], id: UUID) -> AclPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[AclIPv6Policy], id: UUID) -> AclIPv6PolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[DeviceAccessPolicy], id: UUID) -> DeviceAccessPolicyGetResponse:
        ...

    @overload
    def get(self, type: Type[DeviceAccessIPv6Policy], id: UUID) -> DeviceAccessIPv6PolicyGetResponse:
        ...

    def get(self, type: Type[AnyPolicyDefinition], id: Optional[UUID] = None) -> Any:
        endpoints = self.__get_definition_endpoints_instance(type)
        if id is not None:
            return endpoints.get_policy_definition(id=id)
        return endpoints.get_definitions()


class PolicyAPI:
    """This is exposing so called 'UX 1.0' API"""

    def __init__(self, session: ManagerSession):
        self._session = session
        self.centralized = CentralizedPolicyAPI(session)
        self.localized = LocalizedPolicyAPI(session)
        self.security = SecurityPolicyAPI(session)
        self.definitions = PolicyDefinitionsAPI(session)
        self.lists = PolicyListsAPI(session)

    def delete_any(self, _type: Any, id: UUID) -> None:
        if issubclass(_type, PolicyListBase):
            self.lists.delete(_type, id)
        elif issubclass(_type, PolicyDefinitionBase):
            self.definitions.delete(_type, id)
        elif _type == CentralizedPolicy:
            self.centralized.delete(id)
        elif _type == LocalizedPolicy:
            self.localized.delete(id)
        elif _type in [SecurityPolicy, UnifiedSecurityPolicy]:
            self.security.delete(id)
        else:
            raise TypeError(f"Cannot find API method to delete item type: {_type}, {id}")

    def get_protocol_map(self) -> Dict[str, ApplicationProtocol]:
        result = {}
        protocol_map_list = self._session.endpoints.misc.get_application_protocols()
        for protocol_map in protocol_map_list:
            result.update(protocol_map.root)
        return result
