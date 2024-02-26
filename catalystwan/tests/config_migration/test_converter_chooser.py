import unittest

from parameterized import parameterized  # type: ignore

from catalystwan.exceptions import CatalystwanException
from catalystwan.utils.config_migration.converters.feature_template import choose_parcel_converter
from catalystwan.utils.config_migration.converters.feature_template.aaa import AAATemplateConverter
from catalystwan.utils.config_migration.converters.feature_template.bfd import BFDTemplateConverter


class TestParcelConverterChooser(unittest.TestCase):
    @parameterized.expand(
        [("cisco_aaa", AAATemplateConverter), ("cedge_aaa", AAATemplateConverter), ("cisco_bfd", BFDTemplateConverter)]
    )
    def test_choose_parcel_converter_returns_correct_converter_when_supported(self, template_type, expected):
        # Arrange, Act
        converter = choose_parcel_converter(template_type)
        # Assert
        self.assertEqual(converter, expected)

    def test_choose_parcel_converter_throws_exception_when_template_type_not_supported(self):
        # Arrange
        not_supported_type = "!@#$%^&*()"
        # Act, Assert
        with self.assertRaises(CatalystwanException, msg=f"Template type {not_supported_type} not supported"):
            choose_parcel_converter(not_supported_type)
