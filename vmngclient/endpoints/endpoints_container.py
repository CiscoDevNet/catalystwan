from __future__ import annotations

from typing import TYPE_CHECKING

from vmngclient.endpoints.administration_user_and_group import AdministrationUserAndGroup
from vmngclient.endpoints.certificate_management_vmanage import CertificateManagementVManage
from vmngclient.endpoints.client import Client
from vmngclient.endpoints.cluster_management import ClusterManagement
from vmngclient.endpoints.configuration.policy.definition_builder.data import ConfigurationPolicyDataDefinitionBuilder
from vmngclient.endpoints.configuration.policy.definition_builder.zone_based_firewall import (
    ConfigurationPolicyZoneBasedFirewallDefinitionBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.app import ConfigurationPolicyApplicationListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.color import ConfigurationPolicyColorListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.data_ipv6_prefix import (
    ConfigurationPolicyDataIPv6PrefixListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.data_prefix import ConfigurationPolicyDataPrefixListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.fqdn import ConfigurationPolicyFQDNListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.geo_location import (
    ConfigurationPolicyGeoLocationListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.local_app import ConfigurationPolicyLocalAppListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.port import ConfigurationPolicyPortListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.protocol_name import (
    ConfigurationPolicyProtocolNameListBuilder,
)
from vmngclient.endpoints.configuration.policy.list_builder.site_list_builder import ConfigurationPolicySiteListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.vpn import ConfigurationPolicyVPNListBuilder
from vmngclient.endpoints.configuration.policy.list_builder.zone import ConfigurationPolicyZoneListBuilder
from vmngclient.endpoints.configuration.policy.vsmart_template import ConfigurationVSmartTemplatePolicy
from vmngclient.endpoints.configuration_dashboard_status import ConfigurationDashboardStatus
from vmngclient.endpoints.configuration_device_actions import ConfigurationDeviceActions
from vmngclient.endpoints.configuration_device_software_update import ConfigurationDeviceSoftwareUpdate
from vmngclient.endpoints.configuration_device_template import ConfigurationDeviceTemplate
from vmngclient.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from vmngclient.endpoints.configuration_group import ConfigurationGroup
from vmngclient.endpoints.configuration_settings import ConfigurationSettings
from vmngclient.endpoints.monitoring_device_details import MonitoringDeviceDetails
from vmngclient.endpoints.monitoring_status import MonitoringStatus
from vmngclient.endpoints.sdavc_cloud_connector import SDAVCCloudConnector
from vmngclient.endpoints.tenant_backup_restore import TenantBackupRestore
from vmngclient.endpoints.tenant_management import TenantManagement
from vmngclient.endpoints.tenant_migration import TenantMigration

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class ConfigurationPolicyListBuilderContainer:
    def __init__(self, session: vManageSession):
        self.data_prefix = ConfigurationPolicyDataPrefixListBuilder(session)
        self.geo_location = ConfigurationPolicyGeoLocationListBuilder(session)
        self.fqdn = ConfigurationPolicyFQDNListBuilder(session)
        self.site = ConfigurationPolicySiteListBuilder(session)
        self.vpn = ConfigurationPolicyVPNListBuilder(session)
        self.zone = ConfigurationPolicyZoneListBuilder(session)
        self.port = ConfigurationPolicyPortListBuilder(session)
        self.protocol_name = ConfigurationPolicyProtocolNameListBuilder(session)
        self.local_app = ConfigurationPolicyLocalAppListBuilder(session)
        self.app = ConfigurationPolicyApplicationListBuilder(session)
        self.color = ConfigurationPolicyColorListBuilder(session)
        self.data_ipv6_prefix = ConfigurationPolicyDataIPv6PrefixListBuilder(session)


class ConfigurationPolicyDefinitionBuilderContainer:
    def __init__(self, session: vManageSession):
        self.data = ConfigurationPolicyDataDefinitionBuilder(session)
        self.zone_based_firewall = ConfigurationPolicyZoneBasedFirewallDefinitionBuilder(session)


class ConfigurationPolicyContainer:
    def __init__(self, session: vManageSession):
        self.list_builder = ConfigurationPolicyListBuilderContainer(session)
        self.definition_builder = ConfigurationPolicyDefinitionBuilderContainer(session)
        self.vsmart_template = ConfigurationVSmartTemplatePolicy(session)


class ConfigurationContainer:
    def __init__(self, session: vManageSession):
        self.policy = ConfigurationPolicyContainer(session)


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
