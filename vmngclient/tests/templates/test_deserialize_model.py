# type: ignore
import json
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.api.templates.models.cisco_aaa_model import (
    CiscoAAAModel,
    DomainStripping,
    RadiusGroup,
    RadiusServer,
    User,
)
from vmngclient.dataclasses import FeatureTemplateInfo
from vmngclient.typed_list import DataSequence
from vmngclient.utils.creation_tools import create_dataclass

users = [
    User(name="admin", password="str", secret="zyx", privilege="15"),
    User(name="user", password="rnd", secret="dnr", privilege="14"),
]


cisco_aaa = CiscoAAAModel(
    name="iuo",
    description="zyx",
    device_models=["vedge-C8000V"],
    user=users,
    authentication_group=True,
    accounting_group=False,
    radius=[
        RadiusGroup(
            group_name="xyz", vpn=1, source_interface="GIG11", server=[RadiusServer(address="1.1.1.1", key="21")]
        )
    ],
    domain_stripping=DomainStripping.NO,
)


class TestFeatureTemplate(TestCase):
    def setUp(self):
        with open(
            Path(__file__).resolve().parents[0] / Path("definitions") / Path(CiscoAAAModel.type + "_definition.json")
        ) as f:
            self.definition = json.load(f)
        self.feature_template_response = {
            "last_updated_by": "admin",
            "resource_group": "global",
            "id": "xxx",
            "factory_default": "False",
            "name": "iuo",
            "devices_attached": 1,
            "description": "zyx",
            "last_updated_on": 1111111111111,
            "template_type": "cedge_aaa",
            "device_type": ["vedge-C8000V"],
            "version": "15.0.0",
            "template_definiton": f"{json.dumps(self.definition)}",
        }

        self.get_feature_templates_response = DataSequence(
            FeatureTemplateInfo, [create_dataclass(FeatureTemplateInfo, self.feature_template_response)]
        )

    @parameterized.expand([(cisco_aaa,)])
    @patch("vmngclient.session.vManageSession")
    def test_get(self, template, mock_session):
        # Arrange
        mock_session.api.templates._get_feature_templates.return_value = self.get_feature_templates_response

        # Act
        feature_template_from_get = FeatureTemplate.get(session=mock_session, name=template.name)

        # Assert
        self.assertEqual(feature_template_from_get, cisco_aaa)


if __name__ == "__main__":
    unittest.main()
