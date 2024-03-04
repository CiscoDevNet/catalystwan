# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from catalystwan.api.basic_api import DeviceStateAPI
from catalystwan.api.speedtest_api import SpeedtestAPI
from catalystwan.dataclasses import Device, Speedtest


class TestSpeedTestAPI(unittest.TestCase):
    def setUp(self):
        self.device = Device(
            personality="vedge",
            uuid="mock_uuid",
            id="mock_ip",
            hostname="mock_host",
            reachability="reachable",
            local_system_ip="mock_ip",
            status="normal",
            memUsage=1.0,
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
        )
        self.device_unreachable = Device(
            personality="vedge",
            uuid="mock_uuid",
            id="mock_ip",
            hostname="mock_host",
            reachability="unreachable",
            local_system_ip="mock_ip",
            status="normal",
            memUsage=1.0,
            connected_vManages=["192.168.0.1"],
            model="vedge-cloud",
        )

    @patch("catalystwan.api.speedtest_api.sleep")
    @patch("catalystwan.session.ManagerSession")
    def test_perform(self, mock_session, mock_sleep):
        # Arrange
        mock_session.post.return_value.json.return_value = {
            "sessionId": "id",
            "data": [{"up_speed": "up_speed", "down_speed": "down_speed"}],
        }
        mock_session.get_json.return_value = {"status": "status"}
        speed_test_api = SpeedtestAPI(mock_session)
        speed_test_api.speedtest_output = Speedtest("ip", "device_name", "ip", "device_name", None, None, None)
        speed_test_api_compare = SpeedtestAPI(mock_session)
        speed_test_api_compare.speedtest_output = Speedtest(
            "ip", "device_name", "ip", "device_name", "status", "up_speed", "down_speed"
        )
        # Act
        speed_test_api._SpeedtestAPI__perform(self.device, self.device, "blue", "red", 1)
        # Assert
        self.assertEqual(speed_test_api.speedtest_output, speed_test_api_compare.speedtest_output)

    @patch("catalystwan.session.ManagerSession")
    def test_perform_handle_error(self, mock_session):
        # Arrange
        mock_session.post.return_value.json.return_value = {"sessionId": "id", "data": []}
        mock_session.get_json.return_value = {"status": "status"}
        speed_test_api = SpeedtestAPI(mock_session)
        speed_test_api.speedtest_output = Speedtest("ip", "device_name", "ip", "device_name", None, None, None)
        speed_test_api_compare = SpeedtestAPI(mock_session)
        speed_test_api_compare.speedtest_output = Speedtest(
            "ip", "device_name", "ip", "device_name", "No speed received", None, None
        )
        # Act
        speed_test_api._SpeedtestAPI__perform(self.device, self.device, "blue", "red", 1)
        # Assert
        self.assertEqual(speed_test_api.speedtest_output, speed_test_api_compare.speedtest_output)

    @patch.object(SpeedtestAPI, "_SpeedtestAPI__perform")
    @patch.object(DeviceStateAPI, "enable_data_stream")
    @patch.object(DeviceStateAPI, "get_colors")
    @patch("catalystwan.session.ManagerSession")
    def test_speedtest(self, mock_session, mock_get_colors, mock_enable, mock_perform):
        # Arrange
        mock_enable.return_value.__enter__.return_value = None
        speed_test_api = SpeedtestAPI(mock_session)
        speed_test_api_compare = SpeedtestAPI(mock_session)
        speed_test_api_compare.speedtest_output = Speedtest(
            self.device.local_system_ip,
            self.device.hostname,
            self.device.local_system_ip,
            self.device.hostname,
            "",
            0.0,
            0.0,
        )
        # Act
        answer = speed_test_api.speedtest(self.device, self.device, 1)
        # Assert
        self.assertEqual(answer, speed_test_api_compare.speedtest_output)

    @patch.object(SpeedtestAPI, "_SpeedtestAPI__perform")
    @patch.object(DeviceStateAPI, "enable_data_stream")
    @patch.object(DeviceStateAPI, "get_colors")
    @patch("catalystwan.session.ManagerSession")
    def test_speedtest_not_reachable(self, mock_session, mock_get_colors, mock_enable, mock_perform):
        # Arrange
        mock_enable.return_value.__enter__.return_value = None
        speed_test_api = SpeedtestAPI(mock_session)
        speed_test_api_compare = SpeedtestAPI(mock_session)
        speed_test_api_compare.speedtest_output = Speedtest(
            self.device.local_system_ip,
            self.device.hostname,
            self.device.local_system_ip,
            self.device.hostname,
            "Source is unreachable and destination device is unreachable",
            0.0,
            0.0,
        )
        # Act
        answer = speed_test_api.speedtest(self.device_unreachable, self.device_unreachable, 1)
        # Assert
        self.assertEqual(answer, speed_test_api_compare.speedtest_output)

    @patch.object(SpeedtestAPI, "_SpeedtestAPI__perform")
    @patch.object(DeviceStateAPI, "enable_data_stream")
    @patch.object(DeviceStateAPI, "get_colors")
    @patch("catalystwan.session.ManagerSession")
    def test_speedtest_handle_error(self, mock_session, mock_get_colors, mock_enable, mock_perform):
        # Arrange
        mock_enable.return_value.__enter__.return_value = None
        mock_perform.side_effect = HTTPError("url", 400, "error_400", "msg", 1)
        speed_test_api = SpeedtestAPI(mock_session)
        speed_test_api_compare = SpeedtestAPI(mock_session)
        speed_test_api_compare.speedtest_output = Speedtest(
            self.device.local_system_ip,
            self.device.hostname,
            self.device.local_system_ip,
            self.device.hostname,
            "HTTP Error 400: error_400",
            0.0,
            0.0,
        )
        # Act
        answer = speed_test_api.speedtest(self.device, self.device, 1)
        # Assert
        self.assertEqual(answer, speed_test_api_compare.speedtest_output)
