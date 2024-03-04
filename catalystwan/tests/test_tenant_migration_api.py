# Copyright 2023 Cisco Systems, Inc. and its affiliates

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from packaging.version import Version  # type: ignore

from catalystwan.api.task_status_api import Task
from catalystwan.api.tenant_migration_api import ImportTask, TenantMigrationAPI
from catalystwan.endpoints.tenant_migration import ImportInfo, MigrationInfo
from catalystwan.models.tenant import Tenant, TenantExport


class TestTenantMigrationAPI(unittest.TestCase):
    @patch("catalystwan.session.ManagerSession")
    def setUp(self, session_mock):
        self.session = session_mock
        self.api = TenantMigrationAPI(self.session)

    def test_export_tenant(self):
        tenant = Tenant(desc="Test Tenant", name="test_tenant", subdomain="test_subdomain", org_name="test_org")
        task = self.api.export_tenant(tenant=tenant)
        self.assertIsInstance(task, Task)

    def test_export_migration_tenant(self):
        tenant = TenantExport(
            name="test_tenant",
            desc="Test Tenant Description",
            subdomain="test_subdomain",
            org_name="test_org",
            is_destination_overlay_mt=False,
            migration_key="Cisco12345",
        )
        task = self.api.export_tenant(tenant=tenant)
        self.assertIsInstance(task, Task)

    def test_download(self):
        content = b"\xFFtest_data"
        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = Path(tmpdir) / "test.tar.gz"
            self.session.endpoints.tenant_migration.download_tenant_data = MagicMock(return_value=content)
            self.api.download(download_path)
            assert open(download_path, "rb").read() == content

    def test_import_tenant(self):
        self.session.api_version = Version("20.12")
        migration_key = "Cisco12345"
        migration_id = "dcbed267-eb0d-4dcd-9c12-2536e8562f75"
        with tempfile.TemporaryDirectory() as tmpdir:
            import_file = Path(tmpdir) / "tenant.tar.gz"
            with open(import_file, "wb") as f:
                f.write(b"\xFEtest_data")
            self.session.endpoints.tenant_migration.import_tenant_data = MagicMock(
                return_value=ImportInfo(
                    processId="123",
                    migrationTokenURL=(
                        "/dataservice/tenantmigration/migrationToken?"
                        "migrationId=dcbed267-eb0d-4dcd-9c12-2536e8562f75"
                    ),
                )
            )
            task = self.api.import_tenant(import_file, migration_key)
            self.assertIsInstance(task, ImportTask)
            assert task.import_info.migration_token_query_params.migration_id == migration_id

    def test_import_tenant_with_key(self):
        self.session.api_version = Version("20.13")
        migration_key = "Cisco12345"
        migration_id = "dcbed267-eb0d-4dcd-9c12-2536e8562f75"
        with tempfile.TemporaryDirectory() as tmpdir:
            import_file = Path(tmpdir) / "tenant.tar.gz"
            with open(import_file, "wb") as f:
                f.write(b"\xFEtest_data")
            self.session.endpoints.tenant_migration.import_tenant_data_with_key = MagicMock(
                return_value=ImportInfo(
                    processId="123",
                    migrationTokenURL=(
                        "/dataservice/tenantmigration/migrationToken?"
                        "migrationId=dcbed267-eb0d-4dcd-9c12-2536e8562f75"
                    ),
                )
            )
            task = self.api.import_tenant(import_file, migration_key)
            self.assertIsInstance(task, ImportTask)
            assert task.import_info.migration_token_query_params.migration_id == migration_id

    def test_store_token(self):
        token_data = "test_token1987"
        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = Path(tmpdir) / "token.txt"
            migration_id = "123"
            self.session.endpoints.tenant_migration.get_migration_token = MagicMock(return_value=token_data)
            self.api.store_token(migration_id, download_path)
            assert open(download_path, "r").read() == token_data

    def test_migrate_network(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            token_file = Path(tmpdir) / "token_file.txt"
            with open(token_file, "wb") as f:
                f.write(b"token_text")
            self.api.session.endpoints.tenant_migration.migrate_network = MagicMock(
                return_value=MigrationInfo(processId="123")
            )
            task = self.api.migrate_network(token_file)
            self.assertIsInstance(task, Task)
