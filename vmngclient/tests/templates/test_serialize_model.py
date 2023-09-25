import json
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized  # type: ignore

import vmngclient.tests.templates.models as models
from vmngclient.api.template_api import TemplatesAPI
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.session import vManageSession

# Take model
# Generate payload
# Compare payload with definition


class TestFeatureTemplate2(TestCase):
    @parameterized.expand(
        [(template,) for template in map(models.__dict__.get, models.__all__)],  # type: ignore
    )
    @patch("vmngclient.session.vManageSession")
    def test_generate_feature_template_payload_definition(
        self, template: FeatureTemplate, mocked_session: vManageSession
    ):
        # Arrange
        templates_api = TemplatesAPI(mocked_session)
        with open(Path(__file__).resolve().parents[0] / Path("schemas") / Path(template.type + ".json")) as f:
            schema = json.load(f)

        with open(
            Path(__file__).resolve().parents[0] / Path("definitions") / Path(f"{template.template_name}.json")
        ) as f:
            definition = json.load(f)

        # Act
        feature_template_payload = templates_api.generate_feature_template_payload(
            template=template, schema=schema, debug=False
        )
        # Assert
        # self.assertDictEqual
        self.maxDiff = 10000
        self.assertDictEqual(
            definition["templateDefinition"],
            feature_template_payload.dict(by_alias=True)["templateDefinition"],
        )


if __name__ == "__main__":
    unittest.main()
