import unittest
from unittest.mock import MagicMock, patch

from vmngclient.api.monitoring_status_api import MonitoringStatusAPI
from vmngclient.endpoints.monitoring_status import DisabledDevice, EnabledIndex
from vmngclient.typed_list import DataSequence


class TestMonitoringStatusAPI(unittest.TestCase):
    @patch("vmngclient.session.Session")
    def test_get_enabled_index_for_device(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.list_enabled_indexes
        monitoring_status_api = MonitoringStatusAPI(mock_session)
        # Act
        result = monitoring_status_api.get_enabled_index_for_device(self.device_id)
        # Assert
        self.assertEqual(result, self.list_enabled_indexes_datasequence)

    @patch("vmngclient.session.Session")
    def test_get_disabled_devices_by_index(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.get_list_disabled_devices_response
        monitoring_status_api = MonitoringStatusAPI(mock_session)
        # Act
        result = monitoring_status_api.get_disabled_devices_by_index(self.indexName)
        # Assert
        self.assertEqual(result, self.get_list_disabled_devices_datasequence)

    @patch("vmngclient.session.Session")
    def test_update_disabled_devices_by_index(self, mock_session):
        # Arrange
        mock_session.put.return_value = self.update_list_disabled_devices_response
        monitoring_status_api = MonitoringStatusAPI(mock_session)
        # Act
        result = monitoring_status_api.update_disabled_devices_by_index(self.indexName, self.device_id)
        # Assert
        self.assertEqual(result, self.update_list_disabled_devices_return)

    def setUp(self) -> None:
        self.device_id = "1.1.1.1"
        self.indexName = "aggregatedappsdpisummary"
        self.list_enabled_indexes = [
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
        self.list_enabled_indexes_datasequence = DataSequence.from_flatlist(
            EnabledIndex, "indexName", self.list_enabled_indexes
        )
        self.update_list_disabled_devices_response = MagicMock(status_code=200, response=True)
        self.update_list_disabled_devices_return = True
        self.get_list_disabled_devices_response = ["172.16.255.14"]
        self.get_list_disabled_devices_datasequence = DataSequence.from_flatlist(
            DisabledDevice, "ip_address", self.get_list_disabled_devices_response
        )
