# Copyright 2024 Cisco Systems, Inc. and its affiliates

# type: ignore
import unittest
from unittest.mock import MagicMock, patch

from catalystwan.api.monitoring_status_api import MonitoringStatusAPI
from catalystwan.endpoints.monitoring_status import (
    DisabledDeviceListResponse,
    EnabledIndexDeviceListResponse,
    Status,
    StatusEnum,
    UpdateIndexResponse,
    UpdateStatus,
)
from catalystwan.typed_list import DataSequence


class TestMonitoringStatusAPI(unittest.TestCase):
    def test_get_statistic_settings(self):
        # Arrange
        self.api._endpoints.get_statistics_settings.return_value = self.returned_get_statistic_settings
        # Act
        result = self.api.get_statistic_settings()
        # Assert
        assert result == self.expected_get_statistic_settings

    def test_update_statistics_settings(self):
        # Arrange
        self.api._endpoints.update_statistics_settings.return_value = self.returned_update_statistics_settings
        # Act
        result = self.api.update_statistics_settings(self.update_statistics_settings_payload)
        # Assert
        assert result == self.expected_update_statistics_settings

    def test_get_disabled_devices_by_index(self):
        # Arrange
        self.api._endpoints.get_disabled_device_list.return_value = self.returned_list_disabled_devices
        # Act
        result = self.api.get_disabled_devices_by_index(self.indexName)
        # Assert
        assert result == self.expected_list_disabled_devices

    def test_update_disabled_devices_by_index(self):
        # Arrange
        self.api._endpoints.update_statistics_device_list.return_value = self.returned_update_list_disabled_devices
        # Act
        result = self.api.update_disabled_devices_by_index(self.indexName, self.update_disabled_devices_by_index_list)
        # Assert
        assert result == self.expected_update_list_disabled_devices

    def test_get_enabled_index_for_device(self):
        # Arrange
        self.api._endpoints.get_enabled_index_for_device.return_value = self.returned_list_enabled_indexes
        # Act
        result = self.api.get_enabled_index_for_device(self.device_id)
        # Assert
        assert result == self.expected_list_enabled_indexes

    @patch("catalystwan.session.ManagerSession")
    def setUp(self, mock_session) -> None:
        self.session = mock_session
        self.session.api_version = None
        self.session.session_type = None
        self.session.password = "P4s$w0rD"  # pragma: allowlist secret
        self.api = MonitoringStatusAPI(self.session)
        self.api._endpoints = MagicMock()
        self.device_id = "1.1.1.1"
        self.indexName = "aggregatedappsdpisummary"
        self.get_statistic_settings = [
            Status(indexName="interfacestatistics", status=StatusEnum.enable, displayName="Interface Statistics"),
            Status(indexName="eioltestatistics", status=StatusEnum.enable, displayName="EIO LTE Statistics"),
            Status(indexName="sulstatistics", status=StatusEnum.enable, displayName="SUL Statistics"),
        ]
        self.returned_get_statistic_settings = DataSequence(Status, self.get_statistic_settings)
        self.expected_get_statistic_settings = DataSequence(Status, self.get_statistic_settings)
        self.update_statistics_settings_payload = [
            UpdateStatus(indexName="interfacestatistics", status=StatusEnum.disable),
            UpdateStatus(indexName="eioltestatistics", status=StatusEnum.disable),
            UpdateStatus(indexName="sulstatistics", status=StatusEnum.disable),
        ]
        self.update_statistics_settings = [
            Status(indexName="interfacestatistics", status=StatusEnum.disable, displayName="Interface Statistics"),
            Status(indexName="eioltestatistics", status=StatusEnum.disable, displayName="EIO LTE Statistics"),
            Status(indexName="sulstatistics", status=StatusEnum.disable, displayName="SUL Statistics"),
        ]
        self.returned_update_statistics_settings = DataSequence(Status, self.update_statistics_settings)
        self.expected_update_statistics_settings = DataSequence(Status, self.update_statistics_settings)
        self.update_disabled_devices_by_index_list = ["127.0.0.1", "10.0.1.0"]
        self.expected_update_list_disabled_devices = True
        self.returned_update_list_disabled_devices = UpdateIndexResponse(response=True)
        self.returned_list_disabled_devices = DisabledDeviceListResponse(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
        self.expected_list_disabled_devices = ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        self.expected_list_enabled_indexes = [
            "interfacestatistics",
            "eioltestatistics",
            "sulstatistics",
            "qosstatistics",
            "devicesystemstatusstatistics",
            "bridgemacstatistics",
            "dpistatistics",
            "approutestatsstatistics",
            "wlanclientinfostatistics",
            "flowlogstatistics",
            "urlf",
            "fwall",
            "vnfstatistics",
            "umbrella",
            "apphostingstatistics",
            "utddaqioxstatistics",
            "ipsalert",
            "aggregatedappsdpistatistics",
            "bridgeinterfacestatistics",
            "artstatistics",
            "trackerstatistics",
            "cloudxstatistics",
        ]
        self.returned_list_enabled_indexes = EnabledIndexDeviceListResponse(self.expected_list_enabled_indexes)
