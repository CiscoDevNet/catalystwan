from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel  # type: ignore

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class FeatureTemplate(BaseModel, ABC):
    name: str
    description: str

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
