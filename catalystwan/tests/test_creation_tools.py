# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
import datetime
import json
import unittest
from typing import Optional

from attrs import define, field
from parameterized import parameterized

from catalystwan.dataclasses import TLOC, DataclassBase, Device, PacketSetup, TacacsServer, TenantTacacsServer
from catalystwan.utils.creation_tools import FIELD_NAME, asdict, convert_attributes, create_dataclass
from catalystwan.utils.personality import Personality
from catalystwan.utils.reachability import Reachability


@define
class _TestObjectD:
    d: int


@define
class _TestObjectC:
    c: int
    dd: Optional[_TestObjectD] = None


@define
class _TestObjectB:
    rnd: int = field(metadata={FIELD_NAME: "RANDOM"})


@define
class _TestObjectA:
    a: int = field(metadata={FIELD_NAME: "A"})
    b: _TestObjectB = field(metadata={FIELD_NAME: "BBB"})
    c: Optional[_TestObjectC] = None


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
                    "site-id": None,
                    "site-name": None,
                },
            ),
            (_TestObjectA(1, _TestObjectB(2)), {"BBB": {"RANDOM": 2}, "A": 1, "c": None}),
            (
                _TestObjectA(1, _TestObjectB(2), _TestObjectC(1)),
                {"BBB": {"RANDOM": 2}, "A": 1, "c": {"c": 1, "dd": None}},
            ),
            (
                _TestObjectA(1, _TestObjectB(2), _TestObjectC(1, _TestObjectD(111))),
                {"BBB": {"RANDOM": 2}, "A": 1, "c": {"c": 1, "dd": {"d": 111}}},
            ),
            (
                TenantTacacsServer(1, "2", [TacacsServer(*range(7)), TacacsServer(*range(2, 9))]),
                {
                    "timeout": 1,
                    "authentication": "2",
                    "server": [
                        {
                            "address": 0,
                            "authPort": 1,
                            "vpn": 2,
                            "vpnIpSubnet": 3,
                            "key": 4,
                            "secretKey": 5,
                            "priority": 6,
                        },
                        {
                            "address": 2,
                            "authPort": 3,
                            "vpn": 4,
                            "vpnIpSubnet": 5,
                            "key": 6,
                            "secretKey": 7,
                            "priority": 8,
                        },
                    ],
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
                Device(1, "vbond", *range(2), "reachable", 1, site_id="100", site_name="SITE_100"),
                '{"deviceId": 0, "host-name": 1, "local-system-ip": 1, "memState": null, "cpuState": null, '
                '"cpuLoad": null, "connectedVManages": [], "device-model": null, "board-serial": null, '
                '"vedgeCertificateState": null, "chasisNumber": null, "site-id": "100", "site-name": "SITE_100", '
                '"uuid": 1, "personality": "vbond", "reachability": "reachable", "status": null, "memUsage": null, '
                '"state_description": null}',
            ),
        ]
    )
    def test_asdict_json(self, obj, serialized_obj):
        # Arrange, Act
        output = json.dumps(asdict(obj))
        # Assert
        print(output)
        self.assertEqual(output, serialized_obj)

    def test_convert_attributes(self):
        # Arrange
        @define(field_transformer=convert_attributes)
        class ConvertibleData(DataclassBase):
            date_time_1: datetime.datetime = field(metadata={FIELD_NAME: "fromUnixEpochTimestamp"})
            date_time_2: datetime.datetime = field(metadata={FIELD_NAME: "fromString"})

        conv_data_dict = {
            "fromUnixEpochTimestamp": 1689324694991,
            "fromString": "2023-07-14T07:11:09+00:00",
        }
        # Act
        conv_data = create_dataclass(ConvertibleData, conv_data_dict)
        # Assert
        assert isinstance(conv_data.date_time_1, datetime.datetime)
        assert isinstance(conv_data.date_time_2, datetime.datetime)


if __name__ == "__main__":
    unittest.main()
