# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest
from unittest.mock import patch
from uuid import uuid4

from parameterized import parameterized  # type: ignore

from catalystwan.api.mtt_aaa_api import TenantAaaAPI, TenantRadiusAPI, TenantTacacsAPI
from catalystwan.dataclasses import TenantAAA, TenantRadiusServer, TenantTacacsServer
from catalystwan.utils.creation_tools import create_dataclass


class TestAaaAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.aaa = {
            "authOrder": ["radius", "tacacs", "local"],
            "authFallback": True,
            "adminAuthOrder": True,
            "auditDisable": False,
            "accounting": False,
        }
        self.p_aaa = {
            "authOrder": ["radius", "local"],
            "authFallback": True,
            "adminAuthOrder": True,
            "auditDisable": True,
            "accounting": True,
        }
        self.aaa_dataclass = create_dataclass(TenantAAA, self.aaa)
        self.p_aaa_dataclass = create_dataclass(TenantAAA, self.p_aaa)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_del_aaa(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.aaa
        mock_session.delete.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantAaaAPI(mock_session).del_aaa()
        # Assert
        self.assertEqual(answer, expected_outcome)

    @parameterized.expand([[200, True], [400, False]])
    @patch("requests.Response")
    @patch("catalystwan.session.Session")
    def test_add_aaa(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.aaa
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantAaaAPI(mock_session).add_aaa(self.aaa_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.Session")
    def test_get_aaa(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.aaa
        # Act
        answer = TenantAaaAPI(mock_session).get_aaa()
        # Assert
        self.assertEqual(answer, self.aaa_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_put_aaa(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantAaaAPI(mock_session).put_aaa(self.p_aaa_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)


class TestRadiusAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.radius_server_list = [
            {
                "address": "10.0.5.143",
                "authPort": 1812,
                "acctPort": 1813,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
            {
                "address": "10.0.5.144",
                "authPort": 1812,
                "acctPort": 1813,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
            {
                "address": "10.0.5.145",
                "authPort": 1812,
                "acctPort": 1813,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
        ]

        self.p_radius_server_list = [
            {
                "address": "10.0.5.143",
                "authPort": 1812,
                "acctPort": 1813,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
            {
                "address": "10.0.5.144",
                "authPort": 1812,
                "acctPort": 1813,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
        ]
        self.radius_server = {"timeout": 5, "retransmit": 3, "server": self.radius_server_list}
        self.p_radius_server = {"timeout": 5, "retransmit": 3, "server": self.p_radius_server_list}
        self.radius_server_dataclass = create_dataclass(TenantRadiusServer, self.radius_server)
        self.p_radius_server_dataclass = create_dataclass(TenantRadiusServer, self.p_radius_server)

    @parameterized.expand([[204, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_del_radius(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.radius_server
        mock_session.delete.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantRadiusAPI(mock_session).delete_radius()
        # Assert
        self.assertEqual(answer, expected_outcome)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_add_radius(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.radius_server
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantRadiusAPI(mock_session).add_radius(self.radius_server_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.Session")
    def test_get_radius(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.radius_server
        # Act
        answer = TenantRadiusAPI(mock_session).get_radius()
        # Assert
        self.assertEqual(answer, self.radius_server_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_put_radius(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantRadiusAPI(mock_session).put_radius(self.p_radius_server_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)


class TestTacacsAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.tacacs_server_list = [
            {
                "address": "10.0.5.141",
                "authPort": 49,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
            {
                "address": "10.0.5.142",
                "authPort": 49,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 2,
            },
            {
                "address": "10.0.5.151",
                "authPort": 49,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 3,
            },
        ]

        self.p_tacacs_server_list = [
            {
                "address": "10.0.5.141",
                "authPort": 49,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 1,
            },
            {
                "address": "10.0.5.142",
                "authPort": 49,
                "vpn": 1,
                "vpnIpSubnet": "192.168.1.0/24",
                "key": "testing",
                "secretKey": str(uuid4()),
                "priority": 2,
            },
        ]
        self.tacacs_server = {"timeout": 5, "authentication": "PAP", "server": self.tacacs_server_list}
        self.p_tacacs_server = {"timeout": 5, "retransmit": "ASCII", "server": self.p_tacacs_server_list}
        self.tacacs_server_dataclass = create_dataclass(TenantTacacsServer, self.tacacs_server)
        self.p_tacacs_server_dataclass = create_dataclass(TenantTacacsServer, self.p_tacacs_server)

    @parameterized.expand([[204, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_del_tacacs(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.tacacs_server
        mock_session.delete.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantTacacsAPI(mock_session).delete_tacacs()
        # Assert
        self.assertEqual(answer, expected_outcome)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_add_tacacs(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.get_data.return_value = self.tacacs_server
        mock_session.post.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantTacacsAPI(mock_session).add_tacacs(self.tacacs_server_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)

    @patch("catalystwan.session.Session")
    def test_get_tacacs(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.tacacs_server
        # Act
        answer = TenantTacacsAPI(mock_session).get_tacacs()
        # Assert
        self.assertEqual(answer, self.tacacs_server_dataclass)

    @parameterized.expand([[200, True], [400, False]])
    @patch("catalystwan.session.Session")
    @patch("requests.Response")
    def test_put_tacacs(self, status_code, expected_outcome, mock_session, mock_response):
        # Arrange
        mock_session.put.return_value = mock_response
        mock_response.status_code = status_code
        # Act
        answer = TenantTacacsAPI(mock_session).put_tacacs(self.p_tacacs_server_dataclass)
        # Assert
        self.assertEqual(answer, expected_outcome)
