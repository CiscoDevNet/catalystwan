import unittest
from unittest.mock import MagicMock, patch

from vmngclient.api.task_status_api import Task
from vmngclient.api.tenant_management_api import TenantManagementAPI
from vmngclient.model.tenant import Tenant
from vmngclient.primitives.tenant_management import (
    ControlStatus,
    SiteHealth,
    TenantStatus,
    vEdgeHealth,
    vSessionId,
    vSmartStatus,
    vSmartTenantCapacity,
    vSmartTenantMap,
)
from vmngclient.typed_list import DataSequence


class TenantManagementAPITest(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None
        self.api = TenantManagementAPI(self.session)

    def test_get_all(self):
        expected_tenants = [
            Tenant(
                name="tenant1",
                orgName="CiscoDevNet",
                subDomain="alpha.bravo.net",
                desc="This is tenant for unit tests",
                edgeConnectorEnable=True,
                edgeConnectorSystemIp="172.16.255.81",
                edgeConnectorTunnelInterfaceName="GigabitEthernet1",
                wanEdgeForecast=1,
            )
        ]
        self.api._primitives.get_all_tenants = MagicMock(return_value=expected_tenants)
        observed_tenants = self.api.get_all()
        assert expected_tenants == observed_tenants

    def test_create(self):
        tenants = [
            Tenant(
                name="tenant1",
                orgName="CiscoDevNet",
                subDomain="alpha.bravo.net",
                desc="This is tenant for unit tests",
                edgeConnectorEnable=True,
                edgeConnectorSystemIp="172.16.255.81",
                edgeConnectorTunnelInterfaceName="GigabitEthernet1",
                wanEdgeForecast=1,
            )
        ]
        task = self.api.create(tenants)
        self.assertIsInstance(task, Task)

    def test_update(self):
        pass

    def test_delete(self):
        tenant_id_list = ["1"]
        password = "password"
        task = self.api.delete(tenant_id_list, password)
        self.assertIsInstance(task, Task)

    def test_delete_auto_password(self):
        tenant_id_list = ["1"]
        self.session.password = "p4s$w0rD"
        task = self.api.delete(tenant_id_list)
        self.assertIsInstance(task, Task)

    def test_get_statuses(self):
        tenant_status = TenantStatus(
            tenantId="tenant2",
            tenantName="TeanantTwo",
            controlStatus=ControlStatus(controlUp=1, controlDown=0, partial=1),
            siteHealth=SiteHealth(fullConnectivity=2, partialConnectivity=1, noConnectivity=0),
            vEdgeHealth=vEdgeHealth(normal=3, warning=1, error=0),
            vSmartStatus=vSmartStatus(up=1, down=0),
        )
        expected_statuses = DataSequence(TenantStatus, [tenant_status])
        self.api._primitives.get_all_tenant_statuses = MagicMock(return_value=expected_statuses)
        observed_statuses = self.api.get_statuses()
        assert expected_statuses == observed_statuses

    def test_get_hosting_capacity_on_vsmarts(self):
        capacity = vSmartTenantCapacity(vSmartUuid="ABCD-1234", totalTenantCapacity=12, currentTenantCount=5)
        expected_capacities = DataSequence(vSmartTenantCapacity, [capacity])
        self.api._primitives.get_tenant_hosting_capacity_on_vsmarts = MagicMock(return_value=expected_capacities)
        observed_capacities = self.api.get_hosting_capacity_on_vsmarts()
        assert expected_capacities == observed_capacities

    def test_get_vsmart_mapping(self):
        expected_mapping = vSmartTenantMap(
            data={
                "vsmart1": [
                    Tenant(
                        name="tenant1",
                        orgName="Tenant1-organization",
                        subDomain="tenant1.organization.org",
                        flakeId=9987,
                    )
                ]
            }
        )
        self.api._primitives.get_tenant_vsmart_mapping = MagicMock(return_value=expected_mapping)
        observed_mapping = self.api.get_vsmart_mapping()
        assert expected_mapping == observed_mapping

    def test_vsession_id(self):
        expected_vsession_id = "567-DEF"
        self.api._primitives.vsession_id = MagicMock(return_value=vSessionId(VSessionId=expected_vsession_id))
        observed_vsession_id = self.api.vsession_id("1")
        assert expected_vsession_id == observed_vsession_id
