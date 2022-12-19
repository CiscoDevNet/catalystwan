import unittest
from unittest.mock import patch

from vmngclient.api.basic_api import Device, DevicesAPI
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability


class TestDeviceAPI(unittest.TestCase):
    def setUp(self):
        self.devices = [
            Device(
                uuid="cd113ab1-a482-47c8-8946-86321610fc76",
                status="normal",
                personality=Personality.VMANAGE,
                id="169.254.10.1",
                hostname="vm200",
                reachability=Reachability.REACHABLE,
                local_system_ip="172.16.255.200",
                memUsage=53.0,
                connected_vManages=["169.254.10.1"],
                model="vmanage",
                board_serial=None,
            ),
            Device(
                uuid="4537c241-ba6f-4837-b863-95be45b74290",
                status="normal",
                personality=Personality.VBOND,
                id="169.254.10.3",
                hostname="vm135",
                reachability=Reachability.REACHABLE,
                local_system_ip="172.16.255.135",
                memUsage=26.0,
                connected_vManages=["169.254.10.1"],
                model="vedge-cloud",
                board_serial=None,
            ),
            Device(
                uuid="cd2ad6a4-1dfc-4710-92fb-8aebf4952f28",
                status="normal",
                personality=Personality.VSMART,
                id="169.254.10.6",
                hostname="vm131",
                reachability=Reachability.REACHABLE,
                local_system_ip="172.16.253.131",
                memUsage=19.0,
                connected_vManages=["169.254.10.1"],
                model="vsmart",
                board_serial=None,
            ),
            Device(
                uuid="a47dc796-48af-4d83-9715-99b18300871a",
                status="normal",
                personality=Personality.VSMART,
                id="169.254.10.4",
                hostname="vm129",
                reachability=Reachability.REACHABLE,
                local_system_ip="172.16.253.129",
                memUsage=18.0,
                connected_vManages=["169.254.10.1"],
                model="vsmart",
                board_serial=None,
            ),
        ]

    @patch("vmngclient.session.vManageSession")
    def test_controllers(self, mock_session):

        # Arrange
        # mock_session.get_data.return_value = self.data_template

        # Act
        devices_api = DevicesAPI(mock_session)
        controllers = devices_api.controllers

        # Assert
        self.assertEqual("xd", controllers)
