from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.endpoints.administration_user_and_group import AdministrationUserAndGroup
from vmngclient.endpoints.certificate_management_device import CertificateManagementDevice
from vmngclient.endpoints.certificate_management_vmanage import CertificateManagementVManage
from vmngclient.endpoints.client import Client
from vmngclient.endpoints.cluster_management import ClusterManagement
from vmngclient.endpoints.configuration.policy.definition.qos_map import ConfigurationPolicyQoSMapDefinition
from vmngclient.endpoints.configuration.policy.definition.rewrite import ConfigurationPolicyRewriteRuleDefinition
from vmngclient.endpoints.configuration.policy.definition.rule_set import ConfigurationPolicyRuleSetDefinition
from vmngclient.endpoints.configuration.policy.definition.security_group import (
    ConfigurationPolicySecurityGroupDefinition,
)
from vmngclient.endpoints.configuration.policy.definition.traffic_data import ConfigurationPolicyDataDefinition
from vmngclient.endpoints.configuration.policy.definition.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinition,
)
from vmngclient.endpoints.configuration.policy.list.app import ConfigurationPolicyApplicationList
from vmngclient.endpoints.configuration.policy.list.app_probe import ConfigurationPolicyAppProbeClassList
from vmngclient.endpoints.configuration.policy.list.as_path import ConfigurationPolicyASPathList
from vmngclient.endpoints.configuration.policy.list.class_map import ConfigurationPolicyForwardingClassList
from vmngclient.endpoints.configuration.policy.list.color import ConfigurationPolicyColorList
from vmngclient.endpoints.configuration.policy.list.community import ConfigurationPolicyCommunityList
from vmngclient.endpoints.configuration.policy.list.data_ipv6_prefix import ConfigurationPolicyDataIPv6PrefixList
from vmngclient.endpoints.configuration.policy.list.data_prefix import ConfigurationPolicyDataPrefixList
from vmngclient.endpoints.configuration.policy.list.expanded_community import ConfigurationPolicyExpandedCommunityList
from vmngclient.endpoints.configuration.policy.list.fqdn import ConfigurationPolicyFQDNList
from vmngclient.endpoints.configuration.policy.list.geo_location import ConfigurationPolicyGeoLocationList
from vmngclient.endpoints.configuration.policy.list.ips_signature import ConfigurationPolicyIPSSignatureList
from vmngclient.endpoints.configuration.policy.list.ipv6_prefix import ConfigurationPolicyIPv6PrefixList
from vmngclient.endpoints.configuration.policy.list.local_app import ConfigurationPolicyLocalAppList
from vmngclient.endpoints.configuration.policy.list.local_domain import ConfigurationPolicyLocalDomainList
from vmngclient.endpoints.configuration.policy.list.mirror import ConfigurationPolicyMirrorList
from vmngclient.endpoints.configuration.policy.list.policer import ConfigurationPolicyPolicerClassList
from vmngclient.endpoints.configuration.policy.list.port import ConfigurationPolicyPortList
from vmngclient.endpoints.configuration.policy.list.preferred_color_group import ConfigurationPreferredColorGroupList
from vmngclient.endpoints.configuration.policy.list.prefix import ConfigurationPolicyPrefixList
from vmngclient.endpoints.configuration.policy.list.protocol_name import ConfigurationPolicyProtocolNameList
from vmngclient.endpoints.configuration.policy.list.site import ConfigurationPolicySiteList
from vmngclient.endpoints.configuration.policy.list.sla import ConfigurationPolicySLAClassList
from vmngclient.endpoints.configuration.policy.list.tloc import ConfigurationPolicyTLOCList
from vmngclient.endpoints.configuration.policy.list.url_black_list import ConfigurationPolicyURLBlackList
from vmngclient.endpoints.configuration.policy.list.url_white_list import ConfigurationPolicyURLWhiteList
from vmngclient.endpoints.configuration.policy.list.vpn import ConfigurationPolicyVPNList
from vmngclient.endpoints.configuration.policy.list.zone import ConfigurationPolicyZoneList
from vmngclient.endpoints.configuration.policy.security_template import ConfigurationSecurityTemplatePolicy
from vmngclient.endpoints.configuration.policy.vedge_template import ConfigurationVEdgeTemplatePolicy
from vmngclient.endpoints.configuration.policy.vsmart_template import ConfigurationVSmartTemplatePolicy
from vmngclient.endpoints.configuration_dashboard_status import ConfigurationDashboardStatus
from vmngclient.endpoints.configuration_device_actions import ConfigurationDeviceActions
from vmngclient.endpoints.configuration_device_inventory import ConfigurationDeviceInventory
from vmngclient.endpoints.configuration_device_software_update import ConfigurationDeviceSoftwareUpdate
from vmngclient.endpoints.configuration_device_template import ConfigurationDeviceTemplate
from vmngclient.endpoints.configuration_feature_profile import (
    ConfigurationFeatureProfile,
    SDRoutingConfigurationFeatureProfile,
)
from vmngclient.endpoints.configuration_group import ConfigurationGroup
from vmngclient.endpoints.configuration_settings import ConfigurationSettings
from vmngclient.endpoints.misc import MiscellaneousEndpoints
from vmngclient.endpoints.monitoring_device_details import MonitoringDeviceDetails
from vmngclient.endpoints.monitoring_status import MonitoringStatus
from vmngclient.endpoints.real_time_monitoring.reboot_history import RealTimeMonitoringRebootHistory
from vmngclient.endpoints.sdavc_cloud_connector import SDAVCCloudConnector
from vmngclient.endpoints.tenant_backup_restore import TenantBackupRestore
from vmngclient.endpoints.tenant_management import TenantManagement
from vmngclient.endpoints.tenant_migration import TenantMigration
from vmngclient.endpoints.troubleshooting_tools.device_connectivity import TroubleshootingToolsDeviceConnectivity

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class ConfigurationPolicyListContainer:
    def __init__(self, session: vManageSession):
        self.app = ConfigurationPolicyApplicationList(session)
        self.app_probe = ConfigurationPolicyAppProbeClassList(session)
        self.as_path = ConfigurationPolicyASPathList(session)
        self.class_map = ConfigurationPolicyForwardingClassList(session)
        self.color = ConfigurationPolicyColorList(session)
        self.community = ConfigurationPolicyCommunityList(session)
        self.data_ipv6_prefix = ConfigurationPolicyDataIPv6PrefixList(session)
        self.data_prefix = ConfigurationPolicyDataPrefixList(session)
        self.expanded_community = ConfigurationPolicyExpandedCommunityList(session)
        self.fqdn = ConfigurationPolicyFQDNList(session)
        self.geo_location = ConfigurationPolicyGeoLocationList(session)
        self.ips_signature = ConfigurationPolicyIPSSignatureList(session)
        self.ipv6_prefix = ConfigurationPolicyIPv6PrefixList(session)
        self.local_app = ConfigurationPolicyLocalAppList(session)
        self.local_domain = ConfigurationPolicyLocalDomainList(session)
        self.mirror = ConfigurationPolicyMirrorList(session)
        self.policer = ConfigurationPolicyPolicerClassList(session)
        self.port = ConfigurationPolicyPortList(session)
        self.preferred_color_group = ConfigurationPreferredColorGroupList(session)
        self.prefix = ConfigurationPolicyPrefixList(session)
        self.protocol_name = ConfigurationPolicyProtocolNameList(session)
        self.site = ConfigurationPolicySiteList(session)
        self.sla = ConfigurationPolicySLAClassList(session)
        self.tloc = ConfigurationPolicyTLOCList(session)
        self.url_black_list = ConfigurationPolicyURLBlackList(session)
        self.url_white_list = ConfigurationPolicyURLWhiteList(session)
        self.vpn = ConfigurationPolicyVPNList(session)
        self.zone = ConfigurationPolicyZoneList(session)


class ConfigurationPolicyDefinitionContainer:
    def __init__(self, session: vManageSession):
        self.data = ConfigurationPolicyDataDefinition(session)
        self.rule_set = ConfigurationPolicyRuleSetDefinition(session)
        self.security_group = ConfigurationPolicySecurityGroupDefinition(session)
        self.zone_based_firewall = ConfigurationPolicyZoneBasedFirewallDefinition(session)
        self.qos_map = ConfigurationPolicyQoSMapDefinition(session)
        self.rewrite = ConfigurationPolicyRewriteRuleDefinition(session)


class ConfigurationPolicyContainer:
    def __init__(self, session: vManageSession):
        self.list = ConfigurationPolicyListContainer(session)
        self.definition = ConfigurationPolicyDefinitionContainer(session)
        self.vsmart_template = ConfigurationVSmartTemplatePolicy(session)
        self.vedge_template = ConfigurationVEdgeTemplatePolicy(session)
        self.security_template = ConfigurationSecurityTemplatePolicy(session)


class ConfigurationContainer:
    def __init__(self, session: vManageSession):
        self.policy = ConfigurationPolicyContainer(session)


class TroubleshootingToolsContainer:
    def __init__(self, session: vManageSession):
        self.device_connectivity = TroubleshootingToolsDeviceConnectivity(session)


class RealTimeMonitoringContainer:
    def __init__(self, session: vManageSession):
        self.reboot_history = RealTimeMonitoringRebootHistory(session)


class APIEndpointContainter:
    def __init__(self, session: vManageSession):
        self.administration_user_and_group = AdministrationUserAndGroup(session)
        self.certificate_management_vmanage = CertificateManagementVManage(session)
        self.client = Client(session)
        self.cluster_management = ClusterManagement(session)
        self.configuration = ConfigurationContainer(session)
        self.configuration_dashboard_status = ConfigurationDashboardStatus(session)
        self.configuration_device_actions = ConfigurationDeviceActions(session)
        self.configuration_device_software_update = ConfigurationDeviceSoftwareUpdate(session)
        self.configuration_device_template = ConfigurationDeviceTemplate(session)
        self.configuration_settings = ConfigurationSettings(session)
        self.monitoring_device_details = MonitoringDeviceDetails(session)
        self.monitoring_status = MonitoringStatus(session)
        self.sdavc_cloud_connector = SDAVCCloudConnector(session)
        self.tenant_backup_restore = TenantBackupRestore(session)
        self.tenant_management = TenantManagement(session)
        self.tenant_migration = TenantMigration(session)
        self.configuration_feature_profile = ConfigurationFeatureProfile(session)
        self.configuration_group = ConfigurationGroup(session)
        self.sd_routing_configuration_feature_profile = SDRoutingConfigurationFeatureProfile(session)
        self.configuration_device_inventory = ConfigurationDeviceInventory(session)
        self.troubleshooting_tools = TroubleshootingToolsContainer(session)
        self.misc = MiscellaneousEndpoints(session)
        self.real_time_monitoring = RealTimeMonitoringContainer(session)
        self.certificate_management_device = CertificateManagementDevice(session)
