import unittest
from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal
from unittest.mock import patch

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.utils.config_migration.converters.feature_template import template_definition_normalization

TestLiteral = Literal["castable_literal"]


class TestNormalizer(unittest.TestCase):
    def setUp(self):
        self.template_values = {
            "key-one": "Simple string !@#$%^&*()-=[';/.,`~]",
            "keyone": "Simplestring!@#$%^&*()-=[';/.,`~]",
            "bool-value-as-string": "true",
            "boolvalueasstring": "false",
            "simple-int": 1,
            "simpleint": 333333331231,
            "simple-ints-in-list": [1, 2, 4, 5, 6, 7, 8, 9],
            "simple-int-in-list": [1],
            "simplestringsinlist": ["1232132", "!@#$%^&*()-=[';/.,`~]", ""],
            "objects-in-list": [
                {"color": "lte", "hello-interval": 300000, "pmtu-discovery": "false"},
                {"color": "mpls", "pmtu-discovery": "false"},
                {"color": "biz-internet"},
                {"color": "public-internet"},
            ],
            "nested-objects": [{"next-hop": [{"distance": 1}]}],
            "ipv4-address": "10.0.0.2",
            "ipv6addr": "2000:0:2:3::",
        }
        self.expected_result = {
            "key_one": Global[str](value="Simple string !@#$%^&*()-=[';/.,`~]"),
            "keyone": Global[str](value="Simplestring!@#$%^&*()-=[';/.,`~]"),
            "bool_value_as_string": Global[bool](value=True),
            "boolvalueasstring": Global[bool](value=False),
            "simple_int": Global[int](value=1),
            "simpleint": Global[int](value=333333331231),
            "simple_ints_in_list": Global[List[int]](value=[1, 2, 4, 5, 6, 7, 8, 9]),
            "simple_int_in_list": Global[List[int]](value=[1]),
            "simplestringsinlist": Global[List[str]](value=["1232132", "!@#$%^&*()-=[';/.,`~]", ""]),
            "objects_in_list": [
                {
                    "color": Global[str](value="lte"),
                    "hello_interval": Global[int](value=300000),
                    "pmtu_discovery": Global[bool](value=False),
                },
                {"color": Global[str](value="mpls"), "pmtu_discovery": Global[bool](value=False)},
                {"color": Global[str](value="biz-internet")},
                {"color": Global[str](value="public-internet")},
            ],
            "nested_objects": [{"next_hop": [{"distance": Global[int](value=1)}]}],
            "ipv4_address": Global[IPv4Address](value=IPv4Address("10.0.0.2")),
            "ipv6addr": Global[IPv6Address](value=IPv6Address("2000:0:2:3::")),
        }

    def test_normalizer_handles_various_types_of_input(self):
        # Arrange
        expected_result = self.expected_result
        # Act
        returned_result = template_definition_normalization(self.template_values)
        # Assert
        self.assertDictEqual(expected_result, returned_result)

    def test_normalizer_handles_super_nested_input(self):
        # Arrange
        super_nested_input = {
            "super_nested": {"level1": {"level2": {"level3": {"key_one": "value_one", "key_two": "value_two"}}}}
        }
        expected_result = {
            "super_nested": {
                "level1": {
                    "level2": {
                        "level3": {"key_one": Global[str](value="value_one"), "key_two": Global[str](value="value_two")}
                    }
                }
            }
        }

        # Act
        returned_result = template_definition_normalization(super_nested_input)

        # Assert
        self.assertDictEqual(expected_result, returned_result)

    @patch("catalystwan.utils.config_migration.converters.feature_template.normalizer.CastableLiterals", [TestLiteral])
    def test_normalizer_literal_casting_when_literal_in_system_literals(self):
        # Arrange
        simple_input = {"in": "castable_literal"}
        expected_result = {"in": Global[TestLiteral](value="castable_literal")}

        # Act
        returned_result = template_definition_normalization(simple_input)

        # Assert
        self.assertDictEqual(expected_result, returned_result)
