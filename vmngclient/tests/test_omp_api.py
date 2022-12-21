import unittest
from unittest.mock import patch

from vmngclient.api.omp_api import OmpAPI
from vmngclient.dataclasses import (
    OmpAdvertisedRouteData,
    OmpAdvertisedTlocData,
    OmpPeerData,
    OmpReceivedRouteData,
    OmpReceivedTlocData,
    OmpServiceData,
    OmpSummaryData,
)
from vmngclient.utils.creation_tools import create_dataclass


class TestOmpAPI(unittest.TestCase):
    @patch("vmngclient.session.Session")
    def test_omp_peers(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.omp_peer
        # Act
        answer = OmpAPI(mock_session).get_omp_peers(self.device_id)
        # Assert
        self.assertEqual(answer, self.omp_peer_dataclass)

    @patch("vmngclient.session.Session")
    def test_omp_peers_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_omp_peers(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_advertised_routes(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.advertised_routes
        # Act
        answer = OmpAPI(mock_session).get_advertised_routes(self.device_id)
        # Assert
        self.assertEqual(answer, self.advertised_routes_dataclass)

    @patch("vmngclient.session.Session")
    def test_advertised_routes_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_advertised_routes(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_received_routes(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.received_routes
        # Act
        answer = OmpAPI(mock_session).get_received_routes(self.device_id)
        # Assert
        self.assertEqual(answer, self.received_routes_dataclass)

    @patch("vmngclient.session.Session")
    def test_received_routes_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_received_routes(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_advertised_tlocs(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.advertised_tlocs
        # Act
        answer = OmpAPI(mock_session).get_advertised_tlocs(self.device_id)
        # Assert
        self.assertEqual(answer, self.advertised_tlocs_dataclass)

    @patch("vmngclient.session.Session")
    def test_advertised_tlocs_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_advertised_tlocs(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_received_tlocs(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.received_tlocs
        # Act
        answer = OmpAPI(mock_session).get_received_tlocs(self.device_id)
        # Assert
        self.assertEqual(answer, self.received_tlocs_dataclass)

    @patch("vmngclient.session.Session")
    def test_received_tlocs_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_received_tlocs(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_services(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.services
        # Act
        answer = OmpAPI(mock_session).get_services(self.device_id)
        # Assert
        self.assertEqual(answer, self.services_dataclass)

    @patch("vmngclient.session.Session")
    def test_services_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_services(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    @patch("vmngclient.session.Session")
    def test_omp_summary(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.omp_summary
        # Act
        answer = OmpAPI(mock_session).get_omp_summary(self.device_id)
        # Assert
        self.assertEqual(answer, self.omp_summary_dataclass)

    @patch("vmngclient.session.Session")
    def test_omp_summary_empty(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = []
        # Act
        answer = OmpAPI(mock_session).get_omp_summary(self.device_id)
        # Assert
        self.assertEqual(answer, [])

    def setUp(self) -> None:
        self.device_id = "1.1.1.1"
        self.omp_peer = [
            {
                "domain-id": 1,
                "vdevice-name": "169.254.10.10",
                "refresh": "supported",
                "site-id": 129,
                "type": "vsmart",
                "vdevice-host-name": "vm3",
                "up-time-date": 1643135160000,
                "vdevice-dataKey": "169.254.10.10-172.16.253.129-vsmart",
                "peer": "172.16.253.129",
                "up-time": "0:12:57:30",
                "legit": "yes",
                "lastupdated": 1643181828115,
                "state": "up",
            },
            {
                "domain-id": 1,
                "vdevice-name": "169.254.10.10",
                "refresh": "supported",
                "site-id": 130,
                "type": "vsmart",
                "vdevice-host-name": "vm3",
                "up-time-date": 1643135160000,
                "vdevice-dataKey": "169.254.10.10-172.16.255.130-vsmart",
                "peer": "172.16.255.130",
                "up-time": "0:12:57:30",
                "legit": "yes",
                "lastupdated": 1643181828115,
                "state": "up",
            },
        ]
        self.omp_peer_dataclass = [create_dataclass(OmpPeerData, item) for item in self.omp_peer]
        self.advertised_routes = [
            {
                "overlay-id": "1",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "prefix": "100.100.3.0/24",
                "ip": "172.16.254.2",
                "label": "1069",
                "encap": "ipsec",
                "site-id": "3",
                "originator": "172.16.254.2",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "path-id": "65",
                "protocol": "connected",
                "vdevice-dataKey": "169.254.10.10-10",
                "metric": "0",
                "lastupdated": 1643179668956,
                "to-peer": "172.16.253.129",
            },
            {
                "overlay-id": "1",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "prefix": "100.100.3.0/24",
                "ip": "172.16.254.2",
                "label": "1069",
                "encap": "ipsec",
                "site-id": "3",
                "originator": "172.16.254.2",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "path-id": "65",
                "protocol": "connected",
                "vdevice-dataKey": "169.254.10.10-10",
                "metric": "0",
                "lastupdated": 1643179668956,
                "to-peer": "172.16.255.130",
            },
        ]
        self.advertised_routes_dataclass = [
            create_dataclass(OmpAdvertisedRouteData, item) for item in self.advertised_routes
        ]
        self.received_routes = [
            {
                "overlay-id": "1",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "prefix": "10.0.5.0/24",
                "ip": "172.16.254.4",
                "from-peer": "172.16.253.129",
                "label": "1047",
                "encap": "ipsec",
                "site-id": "5",
                "originator": "172.16.254.4",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "path-id": "42",
                "protocol": "connected",
                "vdevice-dataKey": "169.254.10.10-10",
                "metric": "0",
                "lastupdated": 1643182041519,
                "attribute-type": "installed",
                "status": "C I R",
            },
            {
                "overlay-id": "1",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "prefix": "100.100.3.0/24",
                "ip": "172.16.254.2",
                "from-peer": "0.0.0.0",
                "label": "1069",
                "encap": "ipsec",
                "site-id": "3",
                "originator": "172.16.254.2",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "path-id": "65",
                "protocol": "connected",
                "vdevice-dataKey": "169.254.10.10-10",
                "metric": "0",
                "lastupdated": 1643182041520,
                "attribute-type": "installed",
                "status": "C Red R",
            },
        ]
        self.received_routes_dataclass = [create_dataclass(OmpReceivedRouteData, item) for item in self.received_routes]
        self.advertised_tlocs = [
            {
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "ip": "172.16.254.2",
                "tloc-auth-type": "sha1-hmac ah-sha1-hmac",
                "preference": "0",
                "weight": "1",
                "encap": "ipsec",
                "site-id": "3",
                "originator": "172.16.254.2",
                "vdevice-host-name": "vm3",
                "tloc-public-ip": "10.101.3.3",
                "tloc-public-port": "12406",
                "tloc-private-ip": "10.101.3.3",
                "vdevice-dataKey": "169.254.10.10-ipv4-172.16.254.2",
                "tloc-private-port": "12406",
                "tloc-spi": "286",
                "lastupdated": 1643179953349,
                "tloc-encrypt-type": "aes256",
                "tloc-proto": "0",
                "address-family": "ipv4",
                "to-peer": "172.16.253.129",
            },
            {
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "ip": "172.16.254.2",
                "tloc-auth-type": "sha1-hmac ah-sha1-hmac",
                "preference": "0",
                "weight": "1",
                "encap": "ipsec",
                "site-id": "3",
                "originator": "172.16.254.2",
                "vdevice-host-name": "vm3",
                "tloc-public-ip": "10.101.3.3",
                "tloc-public-port": "12406",
                "tloc-private-ip": "10.101.3.3",
                "vdevice-dataKey": "169.254.10.10-ipv4-172.16.254.2",
                "tloc-private-port": "12406",
                "tloc-spi": "286",
                "lastupdated": 1643179953351,
                "tloc-encrypt-type": "aes256",
                "tloc-proto": "0",
                "address-family": "ipv4",
                "to-peer": "172.16.255.130",
            },
        ]
        self.advertised_tlocs_dataclass = [
            create_dataclass(OmpAdvertisedTlocData, item) for item in self.advertised_tlocs
        ]
        self.received_tlocs = [
            {
                "bfd-status": "up",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "ip": "172.16.254.1",
                "tloc-auth-type": "sha1-hmac ah-sha1-hmac",
                "preference": "0",
                "from-peer": "172.16.253.129",
                "weight": "1",
                "encap": "ipsec",
                "site-id": "2",
                "originator": "172.16.254.1",
                "vdevice-host-name": "vm3",
                "tloc-public-ip": "10.101.2.2",
                "tloc-public-port": "12386",
                "tloc-private-ip": "10.101.2.2",
                "vdevice-dataKey": "169.254.10.10-ipv4-172.16.254.1",
                "tloc-private-port": "12386",
                "tloc-spi": "263",
                "lastupdated": 1643185163270,
                "tloc-encrypt-type": "aes256",
                "tloc-proto": "0",
                "address-family": "ipv4",
            },
            {
                "bfd-status": "up",
                "color": "default",
                "vdevice-name": "169.254.10.10",
                "ip": "172.16.254.4",
                "tloc-auth-type": "sha1-hmac ah-sha1-hmac",
                "preference": "0",
                "from-peer": "172.16.255.130",
                "weight": "1",
                "encap": "ipsec",
                "site-id": "5",
                "originator": "172.16.254.4",
                "vdevice-host-name": "vm3",
                "tloc-public-ip": "10.102.5.5",
                "tloc-public-port": "12406",
                "tloc-private-ip": "10.102.5.5",
                "vdevice-dataKey": "169.254.10.10-ipv4-172.16.254.4",
                "tloc-private-port": "12406",
                "tloc-spi": "288",
                "lastupdated": 1643185163286,
                "tloc-encrypt-type": "aes256",
                "tloc-proto": "0",
                "address-family": "ipv4",
            },
        ]
        self.received_tlocs_dataclass = [create_dataclass(OmpReceivedTlocData, item) for item in self.received_tlocs]
        self.services = [
            {
                "path-id": "65",
                "vdevice-dataKey": "169.254.10.10-10-VPN-172.16.254.2",
                "vdevice-name": "169.254.10.10",
                "service": "VPN",
                "from-peer": "0.0.0.0",
                "lastupdated": 1643250832867,
                "originator": "172.16.254.2",
                "label": "1077",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "address-family": "ipv4",
                "status": "C Red R",
            },
            {
                "vdevice-dataKey": "169.254.10.10-10-VPN-172.16.254.2",
                "vdevice-name": "169.254.10.10",
                "service": "VPN",
                "lastupdated": 1643250832869,
                "originator": "172.16.254.2",
                "vpn-id": "10",
                "vdevice-host-name": "vm3",
                "address-family": "ipv4",
                "to-peer": "172.16.255.130",
            },
        ]
        self.services_dataclass = [create_dataclass(OmpServiceData, item) for item in self.services]
        self.omp_summary = [
            {
                "tlocs-sent": 4,
                "policy-sent": 0,
                "mcast-routes-sent": 0,
                "packets-sent": 81579,
                "vdevice-name": "169.254.10.10",
                "inform-sent": 14,
                "packets-received": 81956,
                "routes-received": 18,
                "tlocs-received": 22,
                "mcast-routes-installed": 0,
                "update-sent": 84,
                "devicetype": "vedge",
                "mcast-routes-received": 0,
                "hello-received": 81472,
                "alert-sent": 0,
                "update-received": 468,
                "vsmart-peers": 2,
                "operstate": "UP",
                "policy-received": 0,
                "handshake-received": 2,
                "handshake-sent": 2,
                "alert-received": 0,
                "services-sent": 4,
                "vdevice-host-name": "vm3",
                "inform-received": 14,
                "vdevice-dataKey": "169.254.10.10--",
                "tlocs-installed": 10,
                "services-installed": 0,
                "ompuptime": "9:11:16:34",
                "services-received": 2,
                "lastupdated": 1645494228477,
                "routes-sent": 4,
                "hello-sent": 81479,
                "routes-installed": 8,
                "adminstate": "UP",
            }
        ]
        self.omp_summary_dataclass = [create_dataclass(OmpSummaryData, item) for item in self.omp_summary]
