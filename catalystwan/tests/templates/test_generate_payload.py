# Copyright 2023 Cisco Systems, Inc. and its affiliates

#  type: ignore
import json
import unittest
from pathlib import Path
from typing import ClassVar, List, Optional
from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized
from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.template_api import TemplatesAPI
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.session import ManagerSession


class MockedFeatureTemplate(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    template_name: str = "test"
    template_description: str = "test"
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "test_type"

    num: Optional[str]


class MockedFeatureTemplateAlias(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    template_name: str = "test"
    template_description: str = "test"
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "test_type"

    num: str = Field(alias="as-num")


class RSA(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    key: str = Field(alias="key-string")
    key_type: str = Field(alias="key-type", json_schema_extra={"data_path": ["type", "RSA"]})


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    password: str = Field(json_schema_extra={"data_path": ["list"]})
    pubkey_chain: List[RSA] = Field(default=[], alias="pubkey-chain")


class MockedFeatureTemplateChildren(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    template_name: str = "test"
    template_description: str = "test"
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "test_type"

    user: List[User]


class DataPathFeatureTemplate(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    template_name: str = "test"
    template_description: str = "test"
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "test_type"

    as_num: str = Field(alias="as-num", json_schema_extra={"data_path": ["authentication", "dot1x", "default"]})


password = "pass"  # pragma: allowlist secret

mocked_feature_template_children_1 = MockedFeatureTemplateChildren(
    user=[User(name="user1", password=password), User(name="user2", password=password)]
)

mocked_feature_template_children_2 = MockedFeatureTemplateChildren(
    user=[
        User(name="user1", password=password, pubkey_chain=[RSA(key="*****", key_type="RSA")]),
        User(name="user2", password=password),
    ]
)


class TestFeatureTemplate(TestCase):
    @parameterized.expand(
        [
            ("basic.json", None, MockedFeatureTemplate(num="num")),
            ("alias.json", None, MockedFeatureTemplateAlias(num="12")),
            ("data_path.json", None, DataPathFeatureTemplate(as_num="12")),
            ("children.json", None, mocked_feature_template_children_1),
            ("children_nested.json", None, mocked_feature_template_children_2),
            ("children_nested_datapath.json", None, mocked_feature_template_children_2),
        ]
    )
    @patch("catalystwan.session.ManagerSession")
    def test_get(
        self,
        filename: str,
        definition_name: Optional[str],
        mocked_template: Optional[FeatureTemplate],
        mocked_session: ManagerSession,
    ):
        # Arrange
        templates_api = TemplatesAPI(mocked_session)
        with open(Path(__file__).resolve().parents[0] / Path("schemas") / Path("basic") / Path(filename), "r") as file:
            schema = json.load(file)

        if definition_name is None:
            definition_name = filename

        with open(
            Path(__file__).resolve().parents[0] / Path("definitions") / Path("basic") / Path(definition_name), "r"
        ) as file:
            definition = json.load(file)

        if mocked_template is None:
            mocked_template = MockedFeatureTemplate()

        # Act
        a = templates_api.generate_feature_template_payload(mocked_template, schema).model_dump(
            by_alias=True, exclude_none=True, mode="json"
        )["templateDefinition"]
        print(json.dumps(a))
        # Assert
        self.assertDictEqual(a, definition)


if __name__ == "__main__":
    unittest.main()
