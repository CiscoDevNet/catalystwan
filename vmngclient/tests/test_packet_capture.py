import unittest
from unittest.mock import Mock, patch

from vmngclient.dataclasses import Device
from vmngclient.api.packet_capture_api import PacketCaptureAPI
from vmngclient.dataclasses import Status, PacketSetup
class TestPacketCaptureApi(unittest.TestCase):

    def setUp(self):
        mock_session = Mock()
        self.mock_packet_capture_obj = PacketCaptureAPI(mock_session)
        self.mock_status_obj = Status("mock_status", 1)
        self.status_response = {"fileDownloadStatus":"mock_status",
                            "fileSize" : 1}
    
    @patch("vmngclient.session.vManageSession")
    def test_get_status(self, mock_session):
        
        # Arrange
        status_response = {"fileDownloadStatus":"mock_status",
                            "fileSize" : 1}
        mock_session.get_json.return_value = status_response
        packet_setup = PacketSetup("id",True)
        #Act
        answer = PacketCaptureAPI(mock_session).get_status(packet_setup)
        # Assert
        self.assertEqual(answer,self.mock_status_obj)
