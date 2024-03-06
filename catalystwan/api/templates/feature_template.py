# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Union, cast

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, model_validator

from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.utils.device_model import DeviceModel
from catalystwan.utils.dict import FlattenedDictValue, flatten_dict
from catalystwan.utils.feature_template.find_template_values import find_template_values
from catalystwan.utils.pydantic_field import get_extra_field

if TYPE_CHECKING:
    from catalystwan.session import ManagerSession


class FeatureTemplateValidator(BaseModel, ABC):
    @model_validator(mode="before")
    @classmethod
    def map_fields(cls, values: Union[Any, Dict[str, Union[List[FlattenedDictValue], Any]]]):
        if not isinstance(values, dict):
            return values
        for field_name, field_info in cls.model_fields.items():
            vmanage_key = get_extra_field(field_info, "vmanage_key")
            if vmanage_key in values:
                payload_name = vmanage_key
            elif field_info.alias in values:
                payload_name = field_info.alias
            elif field_name in values:
                payload_name = field_name
            else:
                continue
            data_path = get_extra_field(field_info, "data_path", [])
            value = values.pop(payload_name)
            if value and isinstance(value, list) and all([isinstance(v, FlattenedDictValue) for v in value]):
                for template_value in value:
                    if template_value.data_path == data_path:
                        values[field_name] = template_value.value
                        break
            else:
                values[field_name] = value
        return values


class FeatureTemplate(FeatureTemplateValidator, ABC):
    template_name: str
    template_description: str
    device_models: List[DeviceModel] = []
    device_specific_variables: Dict[str, DeviceVariable] = {}

    def generate_payload(self, session: ManagerSession) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        template = env.get_template(self.payload_path.name)
        output = template.render(self.model_dump(mode="json"))

        ast = env.parse(output)
        if meta.find_undeclared_variables(ast):
            print(meta.find_undeclared_variables(ast))
            raise Exception
        return output

    def generate_cli(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def payload_path(self) -> Path:
        raise NotImplementedError()

    @property
    def type(self) -> str:
        raise NotImplementedError()

    @model_validator(mode="before")
    @classmethod
    def remove_device_variables(cls, values):
        if "device_specific_variables" not in values:
            values["device_specific_variables"] = {}
        to_delete = {}

        # TODO: Add support for nested models with DeviceVariable
        for key, value in values.items():
            if isinstance(value, DeviceVariable):
                to_delete[key] = value
                field_key = cls.model_fields[key].json_schema_extra.get("vmanage_key", cls.model_fields[key].alias)
                values["device_specific_variables"][field_key] = DeviceVariable(name=value.name)

        for var in to_delete:
            if var in values:
                del values[var]

        return values

    @classmethod
    def get(cls, session: ManagerSession, name: str) -> FeatureTemplate:
        """Gets feature template model corresponding to existing feature template based on provided name

        Args:
            session: ManagerSession
            name: name of the existing feature template

        Returns:
            FeatureTemplate: filed out feature template model
        """
        from catalystwan.utils.feature_template.choose_model import choose_model

        template_info = (
            session.api.templates._get_feature_templates(summary=False).filter(name=name).single_or_default()
        )
        template_definition_as_dict = json.loads(cast(str, template_info.template_definiton))

        feature_template_model = choose_model(type_value=template_info.template_type)

        device_specific_variables: Dict[str, DeviceVariable] = {}
        values_from_template_definition = find_template_values(
            template_definition_as_dict, device_specific_variables=device_specific_variables
        )
        flattened_values = flatten_dict(values_from_template_definition)

        return feature_template_model(
            template_name=template_info.name,
            template_description=template_info.description,
            device_models=[DeviceModel(model) for model in template_info.device_type],
            device_specific_variables=device_specific_variables,
            **flattened_values,
        )
