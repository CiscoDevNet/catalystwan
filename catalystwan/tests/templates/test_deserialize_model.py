# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
import json
import unittest
from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase
from unittest.mock import patch

import pytest
from parameterized import parameterized

import catalystwan.tests.templates.models as models
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.dataclasses import FeatureTemplateInfo
from catalystwan.typed_list import DataSequence
from catalystwan.utils.creation_tools import create_dataclass


class TestFeatureTemplate(TestCase):
    def setUp(self):
        template: FeatureTemplate
        feature_template_response: List[Dict[str, Any]] = []

        for template in map(models.__dict__.get, models.__all__):
            definition: Dict[str, Any]
            with open(
                Path(__file__).resolve().parents[0] / Path("definitions") / Path(template.template_name + ".json")
            ) as f:
                definition = json.load(f)
            feature_template_response.append(
                {
                    "last_updated_by": "admin",
                    "resource_group": "global",
                    "id": "xxx",
                    "factory_default": "False",
                    "name": template.template_name,
                    "devices_attached": 1,
                    "description": template.template_description,
                    "last_updated_on": 1111111111111,
                    "template_type": template.type,
                    "device_type": ["vedge-C8000V"],
                    "version": "15.0.0",
                    "template_definiton": f"{json.dumps(definition)}",
                }
            )

        self.get_feature_templates_response = DataSequence(
            FeatureTemplateInfo,
            [create_dataclass(FeatureTemplateInfo, response) for response in feature_template_response],
        )

    @parameterized.expand([(template,) for template in map(models.__dict__.get, models.__all__)])
    @pytest.mark.skip(reason="Deserialization to be refactored")
    @patch("catalystwan.session.ManagerSession")
    def test_get(self, template: FeatureTemplate, mock_session):
        # Arrange
        mock_session.api.templates._get_feature_templates.return_value = self.get_feature_templates_response

        # Act
        feature_template_from_get = FeatureTemplate.get(session=mock_session, name=template.template_name)

        # Assert
        self.assertEqual(feature_template_from_get, template)


if __name__ == "__main__":
    unittest.main()
