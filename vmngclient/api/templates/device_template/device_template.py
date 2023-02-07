from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Final, List, Union

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel  # type: ignore

from vmngclient.api.template_api import TemplatesAPI
from vmngclient.dataclasses import FeatureTemplateInformation
from vmngclient.session import vManageSession

logger = logging.getLogger(__name__)


class GeneralTemplate(BaseModel):
    templateId: str
    templateType: str
    subTemplates: List[GeneralTemplate] = []

    @classmethod
    def get(cls, session: vManageSession, name: str) -> GeneralTemplate:
        templates_api = TemplatesAPI(session)
        template = templates_api.get_single_feature_template(name)
        return cls(templateId=template.id, templateType=template.type)

    class Config:
        arbitrary_types_allowed = True


class DeviceTemplate(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str
    description: str
    general_templates: Union[List[str], List[GeneralTemplate]]
    device_role: str = ""
    device_type: str = ""

    def generate_payload(self, session: vManageSession) -> str:
        env = Environment(
            loader=FileSystemLoader(self.payload_path.parent),
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=DebugUndefined,
        )
        template = env.get_template(self.payload_path.name)
        if isinstance(self.general_templates[0], str):
            self.general_templates = list(
                map(lambda x: GeneralTemplate.get(session, x), self.general_templates)  # type: ignore
            )
        output = template.render(self.dict())

        ast = env.parse(output)
        if meta.find_undeclared_variables(ast):
            print(meta.find_undeclared_variables(ast))
            raise Exception
        return output

    def validate(self, session: vManageSession) -> bool:
        fr_templates = TemplatesAPI(session).get_feature_templates()
        return self._validate_names(fr_templates)

    def _validate_names(self, fr_templates: List[FeatureTemplateInformation]) -> bool:
        templates = set(template.name for template in fr_templates)
        templates_exist = True
        for template in self.feature_templates:
            if template not in set(templates):
                logger.error(f"{template} does not exists.")
                templates_exist = False

        return templates_exist

    def create(self, session: vManageSession) -> str:
        if not self.validate(session):
            raise TypeError("Device Template is invalid.")
        endpoint = "/dataservice/template/device/feature/"
        payload = json.loads(self.generate_payload(session))
        response = session.post(endpoint, json=payload)

        return response.text

    payload_path: Final[Path] = Path(__file__).parent / "device_template_payload.json.j2"
