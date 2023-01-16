import unittest
from unittest.mock import patch

from vmngclient.api.basic_api import DeviceStateAPI
from vmngclient.api.packet_capture_api import PacketCaptureAPI
from vmngclient.dataclasses import Device, PacketSetup, Status


class TestPacketCaptureApi(unittest.TestCase):
    def setUp(self):
        self.status = Status("COMPLETED", 1)
        self.status_response = {"fileDownloadStatus": "COMPLETED", "fileSize": 1}
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
        self.packet_setup = PacketSetup("id", True)

    @patch("vmngclient.session.vManageSession")
    def test_get_status(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = self.status_response
        # Act
        answer = PacketCaptureAPI(mock_session).get_status(self.packet_setup)
        # Assert
        self.assertEqual(answer, self.status)

    @patch("vmngclient.session.vManageSession")
    def test_download_capture_session(self, mock_session):
        # Act
        answer = PacketCaptureAPI(mock_session).download_capture_session(self.packet_setup, self.device)
        # Assert
        self.assertEqual(answer, True)

    @patch("vmngclient.session.vManageSession")
    def test_get_interface_name(self, mock_session):
        # Arrange
        interface_response = {"data": [{"ifname": "GE01"}]}
        mock_session.get_json.return_value = interface_response
        # Act
        answer = PacketCaptureAPI(mock_session).get_interface_name(self.device)
        # Assert
        self.assertEqual(answer, "GE01")

    @patch("vmngclient.session.vManageSession")
    def test_start_stop(self, mock_session):
        # Arrange
        mock_session.get_json.return_value = None
        packet_capture = PacketCaptureAPI(mock_session)
        packet_capture.packet_channel = self.packet_setup
        # Act
        with packet_capture.start_stop(self.device) as answer:
            pass
        # Assert
        self.assertEqual(answer, None)

    @patch("vmngclient.api.packet_capture_api.time.sleep")
    @patch.object(PacketCaptureAPI, "download_capture_session")
    @patch.object(PacketCaptureAPI, "get_status")
    @patch("vmngclient.session.vManageSession")
    def test_channel(self, mock_session, mock_get_status, mock_download, mock_sleep):
        # Arrange
        device_capture_response = {"sessionId": "id", "isNewSession": True}
        mock_session.post.return_value.json.return_value = device_capture_response
        mock_get_status.return_value = self.status
        # Act
        with PacketCaptureAPI(mock_session).channel(self.device) as answer:
            pass
        # Assert
        self.assertEqual(answer, self.packet_setup)

    @patch("vmngclient.api.packet_capture_api.time.sleep")
    @patch("vmngclient.session.vManageSession")
    def test_channel_raise_error(self, mock_session, mock_sleep):
        # Arrange
        device_capture_response = {"sessionId": "id", "isNewSession": False}
        mock_session.post.return_value.json.return_value = device_capture_response
        # Act
        with self.assertRaises(PermissionError) as error:
            with PacketCaptureAPI(mock_session).channel(self.device):
                pass
        # Assert
        self.assertEqual(error.expected, PermissionError)

    @patch.object(PacketCaptureAPI, "start_stop")
    @patch.object(PacketCaptureAPI, "channel")
    @patch.object(DeviceStateAPI, "enable_data_stream")
    @patch("vmngclient.session.vManageSession")
    def test_get_packets(self, mock_session, mock_enable, mock_channel, mock_start_stop):
        # Arrange
        mock_enable.return_value.__enter__.return_value = None
        mock_channel.return_value.__enter__.return_value = None
        mock_start_stop.return_value.__enter__.return_value = None
        packet_capture = PacketCaptureAPI(mock_session)
        packet_capture.status = self.status
        # Act
        answer = packet_capture.get_packets(self.device, duration_seconds=1)
        # Assert
        self.assertEqual(answer, self.status)

    @patch.object(PacketCaptureAPI, "start_stop")
    @patch.object(PacketCaptureAPI, "channel")
    @patch.object(DeviceStateAPI, "enable_data_stream")
    @patch("vmngclient.session.vManageSession")
    def test_get_packets_handle_permission_error(self, mock_session, mock_enable, mock_channel, mock_start_stop):
        # Arrange
        mock_enable.return_value.__enter__.return_value = None
        mock_channel.return_value.__enter__.side_effect = PermissionError()
        mock_start_stop.return_value.__enter__.return_value = None
        packet_capture = PacketCaptureAPI(mock_session)
        failed_status = Status("IMPOSSIBLE", None)
        # Act
        answer = packet_capture.get_packets(self.device, duration_seconds=1)
        # Assert
        self.assertEqual(answer, failed_status)
