# type: ignore
import json
import unittest
from pathlib import Path
from unittest import TestCase

from parameterized import parameterized

from vmngclient.api.template_api import TemplatesAPI
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.api.templates.models.cisco_aaa_model import CiscoAAAModel, User

users = [User(name="admin", password="str", secret="zyx", privilege="15")]
cisco_aaa = CiscoAAAModel(
    name="xyz",
    description="zyx",
    device_models=["vmanage"],
    user=users,
    authentication_group=True,
    accounting_group=True,
)


class TestFeatureTemplate(TestCase):
    @parameterized.expand([(cisco_aaa,)])
    def test_generate_feature_template_payload(self, template: FeatureTemplate):
        # Arrange
        api = TemplatesAPI("tmp")
        print(Path)
        with open(Path(__file__).resolve().parents[0] / Path("schemas") / Path(CiscoAAAModel.type + ".json")) as f:
            schema = json.load(f)

        with open(
            Path(__file__).resolve().parents[0] / Path("definitions") / Path(CiscoAAAModel.type + "_definition.json")
        ) as f:
            definition = json.load(f)

        # Act
        feature_template_payload = api.generate_feature_template_payload(template=template, schema=schema, debug=False)

        # Assert
        self.assertEqual(definition, feature_template_payload)


if __name__ == "__main__":
    unittest.main()
