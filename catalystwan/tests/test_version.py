# Copyright 2023 Cisco Systems, Inc. and its affiliates

import unittest

from packaging.version import Version  # type: ignore
from parameterized import parameterized  # type: ignore

from catalystwan.version import NullVersion, parse_api_version, parse_vmanage_version


class TestNullVersion(unittest.TestCase):
    def test_null_version_properties(self):
        # Arrange, Act
        version = NullVersion()

        # Assert
        self.assertEqual(version.micro, 0)
        self.assertEqual(version.minor, 0)
        self.assertEqual(version.major, 0)
        self.assertEqual(version.base_version, "0")
        self.assertEqual(version.public, "NullVersion")
        self.assertEqual(version.local, None)
        self.assertEqual(version.dev, None)
        self.assertEqual(version.post, None)
        self.assertEqual(version.pre, None)
        self.assertEqual(version.release, (0,))
        self.assertEqual(version.epoch, 0)

        self.assertFalse(version.is_devrelease)
        self.assertFalse(version.is_postrelease)
        self.assertFalse(version.is_prerelease)

    def test_str(self):
        # Arrange, Act
        version = NullVersion()

        # Assert
        self.assertEqual(version.__str__(), "NullVersion")

    @parameterized.expand(
        [
            (Version("0"),),
            (Version("1.0.0"),),
            (Version("1.0.0-111"),),
            (Version("20.12"),),
        ]
    )
    def test_compare(self, version: Version):
        # Arrange, Act
        null_version = NullVersion()

        # Assert
        self.assertTrue(version > null_version)


class TestVersion(unittest.TestCase):
    @parameterized.expand(
        [
            ("1.0.0", Version("1.0.0")),
            ("0", Version("0")),
            ("20.12.0-914-xy", Version("20.12")),
            ("random_string", NullVersion()),
        ]
    )
    def test_parse_api_version(self, version: str, result: Version):
        # Arrange, Act
        parsed_version = parse_api_version(version)

        # Assert
        self.assertEqual(parsed_version, result)

    @parameterized.expand(
        [
            ("1.0.0", Version("1.0.0")),
            ("0", Version("0")),
            ("20.12.0-914-xy", Version("20.12.0-914")),
            ("abc-20.1.9", Version("20.1.9")),
            ("smart-li-20.13.999-3077", Version("20.13.999-3077")),
            ("random_string", NullVersion()),
        ]
    )
    def test_parse_vmanage_version(self, version: str, result: Version):
        # Arrange, Act
        parsed_version = parse_vmanage_version(version)

        # Assert
        self.assertEqual(parsed_version, result)

    def test_parse_api_version_object(self):
        # Arrange, Act
        parsed_version = parse_api_version("Not a Version!")

        # Assert
        self.assertTrue(isinstance(parsed_version, NullVersion))
        self.assertFalse(isinstance(Version("20.11"), NullVersion))


if __name__ == "__main__":
    unittest.main()
