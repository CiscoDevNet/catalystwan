from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, cast

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic.v1 import BaseModel, root_validator

from vmngclient.api.templates.device_variable import DeviceVariable
from vmngclient.utils.device_model import DeviceModel

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class FeatureTemplate(BaseModel, ABC):
    template_name: str
    template_description: str
    device_models: List[DeviceModel] = []
    device_specific_variables: Dict[str, DeviceVariable] = {}

    def generate_payload(self, session: vManageSession) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        template = env.get_template(self.payload_path.name)
        output = template.render(self.dict())

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

    @root_validator(pre=True)
    def remove_device_variables(cls, values):
        if "device_specific_variables" not in values:
            values["device_specific_variables"] = {}
        to_delete = {}

        # TODO: Add support for nested models with DeviceVariable
        for key, value in values.items():
            if isinstance(value, DeviceVariable):
                to_delete[key] = value
                field_key = cls.__fields__[key].field_info.extra.get("vmanage_key", cls.__fields__[key].alias)
                values["device_specific_variables"][field_key] = DeviceVariable(name=value.name)

        for var in to_delete:
            if var in values:
                del values[var]

        return values

    @classmethod
    def get(cls, session: vManageSession, name: str) -> FeatureTemplate:
        """Gets feature template model corresponding to existing feature template based on provided name

        Args:
            session: vManageSession
            name: name of the existing feature template

        Returns:
            FeatureTemplate: filed out feature template model
        """
        from vmngclient.utils.feature_template import choose_model, find_template_values

        template_info = (
            session.api.templates._get_feature_templates(summary=False).filter(name=name).single_or_default()
        )

        template_definition_as_dict = json.loads(cast(str, template_info.template_definiton))

        feature_template_model = choose_model(type_value=template_info.template_type)

        device_specific_variables: Dict[str, DeviceVariable] = {}
        values_from_template_definition = find_template_values(
            template_definition_as_dict, device_specific_variables=device_specific_variables
        )

        return feature_template_model(
            template_name=template_info.name,
            template_description=template_info.description,
            device_models=[DeviceModel(model) for model in template_info.device_type],
            device_specific_variables=device_specific_variables,
            **values_from_template_definition,
        )
