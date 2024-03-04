# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="call-arg"
from unittest import TestCase
from unittest.mock import patch

from catalystwan.api.device_action_api import DecommissionAction, RebootAction, ValidateAction
from catalystwan.dataclasses import Device


class TestRebootActionAPI(TestCase):
    def setUp(self) -> None:
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

    @patch("catalystwan.session.ManagerSession")
    def test_execute(self, mock_session):
        # Arrange
        reboot_action = RebootAction(mock_session, self.device)
        mock_id = "mock_id"
        mock_session.post.return_value.json.return_value = {"id": mock_id}
        # Act
        reboot_action.execute()
        # Assert
        self.assertEqual(reboot_action.action_id, mock_id)

    @patch("catalystwan.session.ManagerSession")
    def test_execute_raise_exception(self, mock_session):
        # Arrange
        reboot_action = RebootAction(mock_session, self.device)
        mock_session.post.return_value.json.return_value = {}
        # Act&Assert
        self.assertRaises(Exception, reboot_action.execute)


class TestValidateActionAPI(TestCase):
    def setUp(self) -> None:
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

    @patch("catalystwan.session.ManagerSession")
    def test_execute(self, mock_session):
        # Arrange
        reboot_action = ValidateAction(mock_session, self.device)
        mock_id = "mock_id"
        mock_session.post.return_value.json.return_value = {"id": mock_id}
        # Act
        reboot_action.execute()
        # Assert
        self.assertEqual(reboot_action.action_id, mock_id)

    @patch("catalystwan.session.ManagerSession")
    def test_execute_raise_exception(self, mock_session):
        # Arrange
        reboot_action = ValidateAction(mock_session, self.device)
        mock_session.post.return_value.json.return_value = {}
        # Act&Assert
        self.assertRaises(Exception, reboot_action.execute)


class TestDecommissionActionAPI(TestCase):
    def setUp(self) -> None:
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

    @patch("requests.Response")
    @patch("catalystwan.session.ManagerSession")
    def test_execute(self, mock_session, mock_response):
        # Arrange
        mock_response.status_code = 200
        reboot_action = DecommissionAction(mock_session, self.device)
        mock_session.put.return_value = mock_response
        # Act
        reboot_action.execute()
        # Assert
        self.assertEqual(mock_response.status_code, 200)

    @patch("requests.Response")
    @patch("catalystwan.session.ManagerSession")
    def test_execute_raise_exception(self, mock_session, mock_response):
        # Arrange
        mock_response.status_code = 404
        # Arrange
        reboot_action = DecommissionAction(mock_session, self.device)
        mock_session.put.return_value = mock_response
        # Act&Assert
        self.assertRaises(Exception, reboot_action.execute)
