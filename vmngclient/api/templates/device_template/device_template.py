from __future__ import annotations

import logging
from pathlib import Path
from typing import Final, List

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel, validator

logger = logging.getLogger(__name__)


class GeneralTemplate(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    subTemplates: List[GeneralTemplate] = []

    templateId: str = ""
    templateType: str = ""


class DeviceTemplate(BaseModel):
    """
    ## Example:

    >>> templates = [
            "default_system", # Cisco System
            "default_logging", # Cisco Logging
            "default_banner", # Banner
        ]
    >>> device_template = DeviceTemplate(
            name="python",
            description="python",
            general_templates=templates
        )
    >>> session.api.templates.create(device_template)
    """

    name: str
    description: str
    general_templates: List[GeneralTemplate]
    device_role: str = ""
    device_type: str = ""

    def generate_payload(self) -> str:
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
            logger.info(meta.find_undeclared_variables(ast))
            raise Exception("There are undeclared variables.")
        return output

    @validator("general_templates", pre=True)
    def parse_templates(cls, value):
        output = []
        for template in value:
            if isinstance(template, str):
                output.append(GeneralTemplate(name=template))
            else:
                output.append(template)
        return output

    payload_path: Final[Path] = Path(__file__).parent / "device_template_payload.json.j2"


class DeviceSpecificValue(BaseModel):
    property: str
