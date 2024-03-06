import json
import os
import unittest
from typing import Any, List, cast

from catalystwan.session import create_manager_session
from catalystwan.utils.feature_template.find_template_values import find_template_values


class TestFindTemplateValues(unittest.TestCase):
    def setUp(self) -> None:
        self.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
        self.templates = self.session.api.templates._get_feature_templates(summary=False)

    def test_find_template_value(self):
        for template in self.templates:
            definition = json.loads(template.template_definiton)
            with self.subTest(template_name=template.name):
                parsed_values = find_template_values(definition)
                self.assertFalse(
                    self.is_key_present(parsed_values, ["vipType", "vipValue", "vipVariableName", "vipObjectType"])
                )

    def is_key_present(self, d: dict, keys: List[Any]):
        """
        Checks if any key from keys is present within the dictionary d
        """
        for key, value in d.items():
            if key in keys:
                return True
            if isinstance(value, dict):
                if self.is_key_present(value, keys):
                    return True
            if isinstance(value, list):
                for v in value:
                    if isinstance(v, dict):
                        if self.is_key_present(v, keys):
                            return True
        return False

    def tearDown(self) -> None:
        self.session.close()
