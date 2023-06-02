import unittest
from unittest.mock import patch

from vmngclient.api.task_status_api import Task
from vmngclient.api.tenant_management_api import TenantManagementAPI
from vmngclient.model.tenant import Tenant
from vmngclient.primitives.tenant_management import vSmartTenantMap
from vmngclient.typed_list import DataSequence


class TenantManagementAPITest(unittest.TestCase):
    @patch("vmngclient.session.vManageSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.api = TenantManagementAPI(self.session)

    def test_get_all(self):
        tenants = self.api.get_all()
        self.assertIsInstance(tenants, DataSequence)

    def test_create(self):
        tenants = [Tenant(id="1", name="Tenant 1")]
        task = self.api.create(tenants)
        self.assertIsInstance(task, Task)

    def test_delete(self):
        tenant_id_list = ["1"]
        password = "password"
        task = self.api.delete(tenant_id_list, password)
        self.assertIsInstance(task, Task)

    def test_get_statuses(self):
        statuses = self.api.get_statuses()
        self.assertIsInstance(statuses, DataSequence)

    def test_get_hosting_capacity_on_vsmarts(self):
        capacity = self.api.get_hosting_capacity_on_vsmarts()
        self.assertIsInstance(capacity, DataSequence)

    def test_get_vsmart_mapping(self):
        mapping = self.api.get_vsmart_mapping()
        self.assertIsInstance(mapping, vSmartTenantMap)

    def test_vsession_id(self):
        tenant_id = "1"
        vsession_id = self.api.vsession_id(tenant_id)
        self.assertIsInstance(vsession_id, str)
