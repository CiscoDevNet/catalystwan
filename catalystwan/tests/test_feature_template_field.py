# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
import unittest
from unittest import TestCase

from parameterized import parameterized

from catalystwan.api.templates.feature_template_field import get_path_dict


class TestGetPathDict(TestCase):
    @parameterized.expand(
        [
            ([], {}),
            (["a"], {"a": {}}),
            (["a", "b"], {"a": {}, "b": {}}),
            ([["a", "b"]], {"a": {"b": {}}}),
            ([["a", "b"], ["c"]], {"a": {"b": {}}, "c": {}}),
            ([["a", "b"], ["c"]], {"a": {"b": {}}, "c": {}}),
            ([["a", "b"], ["c"], ["a", "d"]], {"a": {"b": {}, "d": {}}, "c": {}}),
        ]
    )
    def test_get_path_dict(self, paths, answer):
        # Arrange, Act
        output = get_path_dict(paths)

        # Assert
        self.assertEqual(output, answer)


if __name__ == "__main__":
    unittest.main()
