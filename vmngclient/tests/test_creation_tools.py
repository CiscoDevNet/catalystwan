# type: ignore
import json
import unittest

from parameterized import parameterized

from vmngclient.dataclasses import TLOC, Device, PacketSetup, TacacsServer, TenantTacacsServer
from vmngclient.utils.creation_tools import asdict
from vmngclient.utils.personality import Personality
from vmngclient.utils.reachability import Reachability


class TestCreationTools(unittest.TestCase):
    @parameterized.expand(
        [
            (TLOC(1, 1), {"color": 1, "encapsulation": 1}),
            (PacketSetup(1, 2), {"sessionId": 1, "isNewSession": 2}),
            (
                Device(1, "vbond", *range(2), "reachable", 1),
                {
                    "deviceId": 0,
                    "host-name": 1,
                    "local-system-ip": 1,
                    "memState": None,
                    "cpuState": None,
                    "cpuLoad": None,
                    "connectedVManages": [],
                    "device-model": None,
                    "board-serial": None,
                    "vedgeCertificateState": None,
                    "chasisNumber": None,
                    "uuid": 1,
                    "personality": Personality.VBOND,
                    "reachability": Reachability.REACHABLE,
                    "status": None,
                    "memUsage": None,
                    "state_description": None,
                },
            ),
            (
                TenantTacacsServer(1, "2", TacacsServer(*range(7))),
                {
                    "timeout": 1,
                    "authentication": "2",
                    "server": {
                        "address": 0,
                        "authPort": 1,
                        "vpn": 2,
                        "vpnIpSubnet": 3,
                        "key": 4,
                        "secretKey": 5,
                        "priority": 6,
                    },
                },
            ),
        ]
    )
    def test_asdict(self, obj, serialized_obj):
        # Arrange, Act
        output = asdict(obj)
        print(output)
        # Assert
        self.assertEqual(output, serialized_obj)

    @parameterized.expand(
        [
            (TLOC(1, 1), '{"color": 1, "encapsulation": 1}'),
            (PacketSetup(1, 2), '{"sessionId": 1, "isNewSession": 2}'),
            (
                Device(1, "vbond", *range(2), "reachable", 1),
                '{"deviceId": 0, "host-name": 1, "local-system-ip": 1, "memState": null, "cpuState": null, '
                '"cpuLoad": null, "connectedVManages": [], "device-model": null, "board-serial": null, '
                '"vedgeCertificateState": null, "chasisNumber": null, "uuid": 1, "personality": "vbond", '
                '"reachability": "reachable", "status": null, "memUsage": null, "state_description": null}',
            ),
        ]
    )
    def test_asdict_json(self, obj, serialized_obj):
        # Arrange, Act
        output = json.dumps(asdict(obj))
        # Assert
        print(output)
        self.assertEqual(output, serialized_obj)


if __name__ == "__main__":
    unittest.main()
