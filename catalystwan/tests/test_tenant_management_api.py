# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import MagicMock, patch

from catalystwan.api.task_status_api import Task
from catalystwan.api.tenant_management_api import TenantManagementAPI
from catalystwan.endpoints.tenant_management import (
    ControlStatus,
    SiteHealth,
    TenantStatus,
    TenantUpdateRequest,
    vEdgeHealth,
    vSessionId,
    vSmartPlacementUpdateRequest,
    vSmartStatus,
    vSmartTenantCapacity,
    vSmartTenantMap,
)
from catalystwan.models.tenant import Tenant
from catalystwan.typed_list import DataSequence


class TenantManagementAPITest(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.session.api_version = None
        self.session.session_type = None
        self.api = TenantManagementAPI(self.session)

    def test_get(self):
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
        self.api._endpoints.get_all_tenants = MagicMock(return_value=expected_tenants)
        observed_tenants = self.api.get()
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
        # Arrange
        tenant_update_request = TenantUpdateRequest(
            tenantId="apo605#",
            subDomain="doamin.tenant.net",
            desc="Tenant1 description",
            wanEdgeForecast=1,
            edgeConnectorEnable=False,
        )
        self.api._endpoints.update_tenant = MagicMock()
        # Act
        self.api.update(tenant_update_request=tenant_update_request)
        # Assert
        self.api._endpoints.update_tenant.assert_called_once_with(
            tenant_id=tenant_update_request.tenant_id, tenant_update_request=tenant_update_request
        )

    def test_update_vsmart_placement(self):
        # Arrange
        src_uuid = "123190GDS*!"
        dst_uuid = "!_0ac%$asfDS"
        tenant_id = "apo605#"
        vsmart_placement_update = vSmartPlacementUpdateRequest(
            srcvSmartUuid=src_uuid,
            destvSmartUuid=dst_uuid,
        )
        self.api._endpoints.update_tenant_vsmart_placement = MagicMock()
        # Act
        self.api.update_vsmart_placement(tenant_id=tenant_id, src_vsmart_uuid=src_uuid, dst_vsmart_uuid=dst_uuid)
        # Assert
        self.api._endpoints.update_tenant_vsmart_placement.assert_called_once_with(
            tenant_id=tenant_id, vsmart_placement_update_request=vsmart_placement_update
        )

    def test_delete(self):
        tenant_id_list = ["1"]
        password = "password"  # pragma: allowlist secret
        task = self.api.delete(tenant_id_list, password)
        self.assertIsInstance(task, Task)

    def test_delete_auto_password(self):
        tenant_id_list = ["1"]
        self.session.password = "p4s$w0rD"  # pragma: allowlist secret
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
        self.api._endpoints.get_all_tenant_statuses = MagicMock(return_value=expected_statuses)
        observed_statuses = self.api.get_statuses()
        assert expected_statuses == observed_statuses

    def test_get_hosting_capacity_on_vsmarts(self):
        capacity = vSmartTenantCapacity(vSmartUuid="ABCD-1234", totalTenantCapacity=12, currentTenantCount=5)
        expected_capacities = DataSequence(vSmartTenantCapacity, [capacity])
        self.api._endpoints.get_tenant_hosting_capacity_on_vsmarts = MagicMock(return_value=expected_capacities)
        observed_capacities = self.api.get_hosting_capacity_on_vsmarts()
        assert expected_capacities == observed_capacities

    def test_get_vsmart_mapping(self):
        expected_mapping = vSmartTenantMap(
            data={
                "vsmart1": [
                    Tenant(
                        name="tenant1",
                        orgName="Tenant1-organization",
                        desc="Tenant1 description",
                        subDomain="tenant1.organization.org",
                        flakeId=9987,
                    )
                ]
            }
        )
        self.api._endpoints.get_tenant_vsmart_mapping = MagicMock(return_value=expected_mapping)
        observed_mapping = self.api.get_vsmart_mapping()
        assert expected_mapping == observed_mapping

    def test_vsession_id(self):
        expected_vsession_id = "567-DEF"
        self.api._endpoints.vsession_id = MagicMock(return_value=vSessionId(VSessionId=expected_vsession_id))
        observed_vsession_id = self.api.vsession_id("1")
        assert expected_vsession_id == observed_vsession_id
