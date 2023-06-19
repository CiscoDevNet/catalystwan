from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, root_validator
from vmngclient.api.templates.device_variable import DeviceVariable

from vmngclient.utils.device_model import DeviceModel

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class FeatureTemplate(BaseModel, ABC):
    name: str
    description: str
    device_models: List[DeviceModel]
    _device_specific_variables: Dict[str, DeviceVariable]

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
        cls._device_specific_variables = {}
        for value in values:
            if isinstance(values[value], DeviceVariable):
                cls._device_specific_variables[value] = values[value]

        for var in cls._device_specific_variables:
            del values[var]

        return values
