from unittest import TestCase
from unittest.mock import Mock, patch

from parameterized import parameterized  # type: ignore

from vmngclient.api.basic_api import DeviceField, DevicesAPI
from vmngclient.dataclasses import Device
from vmngclient.utils.creation_tools import create_dataclass
from vmngclient.utils.personality import Personality


class TestDevicesAPI(TestCase):
    def setUp(self) -> None:
        self.devices = [
            {  # vmanage
                "device-model": "vmanage",
                "deviceId": "1.1.1.1",
                "uuid": "aaaaaaaa-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 4.71,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.1",
                "board-serial": "11122233",
                "personality": "vmanage",
                "memUsage": 57.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm200",
                "cpuState": "normal",
                "chassis-number": "aaaaaaaa-6aa9-445c-8e49-c0aaaaaaaaa9",
            },
            {  # vsmart
                "device-model": "vsmart",
                "deviceId": "1.1.1.3",
                "uuid": "bbcccccc-6169-445c-8e49-c0bdccccccc",
                "cpuLoad": 2.76,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.3",
                "board-serial": "11223399",
                "personality": "vsmart",
                "memUsage": 28.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm129",
                "cpuState": "normal",
                "chassis-number": "abbbbbbb-6169-445c-8e49-c0bccccccccc",
            },
            {  # vbond
                "device-model": "vedge-cloud",
                "deviceId": "1.1.1.2",
                "uuid": "bbbbbbbb-6169-445c-8e49-c0bdaaaaaaa",
                "cpuLoad": 1.76,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "1.1.1.2",
                "board-serial": "11223344",
                "personality": "vbond",
                "memUsage": 26.0,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm128",
                "cpuState": "normal",
                "chassis-number": "abbbbbbb-6169-445c-8e49-c0bbbbbbbbb9",
            },
            {  # vedge
                "device-model": "vedge-cloud",
                "deviceId": "169.254.10.10",
                "uuid": "bc2a78ac-a06e-40fd-b2b7-1b1e062f3f9e",
                "cpuLoad": 1.46,
                "state_description": "All daemons up",
                "status": "normal",
                "memState": "normal",
                "local-system-ip": "172.16.254.2",
                "board-serial": "12345708",
                "personality": "vedge",
                "memUsage": 24.1,
                "reachability": "reachable",
                "connectedVManages": ["1.1.1.1"],
                "host-name": "vm1",
                "cpuState": "normal",
                "chassis-number": "bc2a78ac-a06e-40fd-b2b7-1b1e062f3f9e",
            },
        ]
        self.devices_dataclass = [create_dataclass(Device, device) for device in self.devices]
        self.controllers_dataclass = [create_dataclass(Device, device) for device in self.devices[:2]]
        self.orchestrators_dataclass = [create_dataclass(Device, self.devices[2])]
        self.edges_dataclass = [create_dataclass(Device, self.devices[3])]
        self.vsmarts_dataclass = [create_dataclass(Device, self.devices[1])]
        self.system_ips_list = [device["local-system-ip"] for device in self.devices]
        self.ips_list = [device["deviceId"] for device in self.devices]
        self.tenants = [
            {
                'flakeId': 11111,
                'orgName': 'my-org Inc',
                'samlSpInfo': '',
                'subDomain': 'sub1.domain.com',
                'vBondAddress': '1.1.1.1',
                'oldIdpMetadata': '',
                'configDBClusterServiceName': '',
                'vSmarts': ['aaaaaaaa-aaac-42f4-b2c7-1aaaaaaaaaaaa', 'bbbbbbbb-9d8a-453c-841f-4bbbbbbbbbbb'],
                'mode': 'off',
                'idpMetadata': '',
                'createdAt': 1111111111111,
                '@rid': 1111,
                'tenantId': 'aaaaaaaaaa-9ca8-42fd-8290-67aaaaaaaaaa',
                'name': 'sub1',
                'wanEdgeForecast': '100',
                'spMetadata': '',
                'state': 'READY',
                'wanEdgePresent': 1,
                'desc': 'This is sub1',
            },
            {
                'flakeId': 22222,
                'orgName': 'my-org Inc',
                'samlSpInfo': '',
                'subDomain': 'sub2.domain.com',
                'vBondAddress': '1.1.1.2',
                'oldIdpMetadata': '',
                'configDBClusterServiceName': '',
                'vSmarts': ['ccccccccccccccc-42f4-b2c7-1cccccccccc', 'ddddddddd-9d8a-453c-841f-4dddddddddd'],
                'mode': 'off',
                'idpMetadata': '',
                'createdAt': 2222222222222,
                '@rid': 2222,
                'tenantId': 'ccccccccca-9ca8-42fd-8290-67aaaccccccc',
                'name': 'sub2',
                'wanEdgeForecast': '100',
                'spMetadata': '',
                'state': 'READY',
                'wanEdgePresent': 1,
                'desc': 'This is sub2',
            },
        ]
        self.devices_vbonds = [self.devices[2]]
        self.devices_vsmatrs = [self.devices[1]]
        self.devices_edges = [self.devices[3]]

    @patch.object(DevicesAPI, 'devices')
    def test_controllers(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.controllers
        # Assert
        self.assertEqual(answer, self.controllers_dataclass)

    @patch.object(DevicesAPI, 'devices')
    def test_orchestrators(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.orchestrators
        # Assert
        self.assertEqual(answer, self.orchestrators_dataclass)

    @patch.object(DevicesAPI, 'devices')
    def test_edges(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.edges
        # Assert
        self.assertEqual(answer, self.edges_dataclass)

    @patch.object(DevicesAPI, 'devices')
    def test_vsmarts(self, mock_vsmarts):
        # Arrange
        MockDevices = Mock()
        mock_vsmarts.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.vsmarts
        # Assert
        self.assertEqual(answer, self.vsmarts_dataclass)

    @patch.object(DevicesAPI, 'devices')
    def test_system_ips(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.system_ips
        # Assert
        self.assertEqual(answer, self.system_ips_list)

    @patch.object(DevicesAPI, 'devices')
    def test_ips(self, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.ips
        # Assert
        self.assertEqual(answer, self.ips_list)

    @patch('vmngclient.session.vManageSession')
    def test_devices(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.devices
        # Act
        answer = DevicesAPI(mock_session).devices
        # Assert
        self.assertEqual(answer, self.devices_dataclass)

    def test_get_device_details(self):
        pass  # TODO fix method before test

    def test_count_devices(self):
        pass  # TODO fix method before test

    @patch('vmngclient.session.vManageSession')
    def test_get_tenants(self, mock_session):
        # Arrange
        mock_session.get_data.return_value = self.tenants
        # Act
        answer = DevicesAPI(mock_session).get_tenants()
        # Assert
        self.assertEqual(answer, self.tenants)

    @patch('vmngclient.session.vManageSession')
    def test_get_reachable_devices_for_vsmatrs(self, mock_session, personality=Personality.VSMART):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_vsmatrs)

    @patch('vmngclient.session.vManageSession')
    def test_get_reachable_devices_for_vbonds(self, mock_session, personality=Personality.VBOND):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_vbonds)

    @patch('vmngclient.session.vManageSession')
    def test_get_reachable_devices_for_edges(self, mock_session, personality=Personality.EDGE):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]
        # Act
        answer = DevicesAPI(mock_session).get_reachable_devices(personality)
        # Assert
        self.assertEqual(answer, self.devices_edges)

    @patch('vmngclient.session.vManageSession')
    def test_get_reachable_devices_for_vmanage(self, mock_session, personality=Personality.VMANAGE):
        # Arrange
        mock_session.get_data.return_value = [
            device for device in self.devices if device["personality"] == personality.value
        ]

        # Act
        def answer():
            return DevicesAPI(mock_session).get_reachable_devices(personality)

        # Assert
        self.assertRaises(AssertionError, answer)

    def test_send_certificate_state_to_controllers(self):
        pass  # TODO

    @parameterized.expand([["vm200", 0], ["vm129", 1], ["vm128", 2], ["vm1", 3]])
    @patch.object(DevicesAPI, 'devices')
    def test_get(self, hostname, device_number, mock_devices):
        # Arrange
        MockDevices = Mock()
        mock_devices.return_value = MockDevices
        session = Mock()
        test_object = DevicesAPI(session)
        test_object.devices = self.devices_dataclass
        # Act
        answer = test_object.get(DeviceField.HOSTNAME, hostname)
        # Assert
        self.assertEqual(answer, self.devices_dataclass[device_number])


class TestDevicesStateAPI(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_device_crash_info(self):
        pass

    def test_get_device_control_connections_info(self):
        pass

    def test_get_device_orchestrator_connections_info(self):
        pass

    def test_get_device_reboot_history(self):
        pass

    def test_get_system_status(self):
        pass

    def test_get_device_wan_interfaces(self):
        pass

    def test_get_colors(self):
        pass

    def test_enable_data_stream(self):
        pass

    def test_get_bfd_sessions(self):
        pass

    def test_wait_for_bfd_session_up(self):
        pass

    def test_wait_for_device_state(self):
        pass
