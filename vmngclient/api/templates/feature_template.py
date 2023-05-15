from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List

from jinja2 import DebugUndefined, Environment, FileSystemLoader, meta  # type: ignore
from pydantic import BaseModel

from vmngclient.utils.device_model import DeviceModel

if TYPE_CHECKING:
    from vmngclient.session import vManageSession


class FeatureTemplate(BaseModel, ABC):
    name: str
    description: str
    device_models: List[DeviceModel]

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

    @classmethod
    def get(cls, session: vManageSession, name: str) -> FeatureTemplate:
        """
        1. Request to get templateID based on template name
        2. Based on templateID get FeatureTemplateInfo -> inside we have FeatureTemplateInfo.template_definition -> that holds json with all these vip values/objects etc.
        3. We create instance of FeatureTemplate which we will be filling
        4. Request to get template schema by FeatureTemplate instance - we want to have FeatureTemplateField object based on our type
        5. Based on FeatureTemplateField.dataPath we can retrive all values from TemplateDefinition ???
            5.1 If we are able to get all values from TemplateDefinition, we can fill our model (FeatureTemplate) with these values
        ...

        """
        # 1
        template_info = (
            session.api.templates._get_feature_templates(summary=False).filter(name=name).single_or_default()
        )
        template_definition_as_dict = json.loads(template_info.template_definiton)

        # 2
        endpoint = f"/dataservice/template/feature/types/definition/{template.template_type}/{template.version}"
        schema = session.get(url=endpoint).json()
        fr_template_fields = [
            FeatureTemplateField(**field) for field in schema["fields"]
        ]  # TODO add dataclass for this list, to include also name, xmlPath, namespace etc.
        template_fields = {field.key: field for field in fr_template_fields}

        # 3
        # Based on template_info.template_type we can predict which model is needed
        # First idea is to gather all template types in form of: template_type_as_string : OurModelClassNameToImport and based on the template_info.template_type get proper class
        from vmngclient.api.templates.models.cisco_aaa_model import (
            CiscoAAAModel,  # , RadiusGroup, RadiusServer, User, DomainStripping
        )

        # 4
        # fr_template_fields contain all fields with data paths
        """
        Iterate over all keys in requested Model
        If there is field with
        """
        # for name, field in CiscoAAAModel.__fields__.items():
        #     # t = field.type_

        #     # These can fill the `name` and `description` fields
        #     if getattr(template_info, name, None):
        #         print(name)
        #         print(f"    {template_info.__getattribute__(name)}")

        #     # if we have field in template_definition_as_dict means it can be simple value or nested one
        #     # nested one include children
        #     # children can be Enum, other datamodel or List[datamodel]
        #     if template_definition_as_dict.get(name):
        #         print(name)
        #         print(f"    {template_definition_as_dict.get(name)}")
        #         data_path = template_fields.get(name).dataPath
        #         print(f"        {data_path}")
        #         if template_definition_as_dict.get(name)['vipObjectType'] == 'tree':
        #             print(f"Nested")
        dict_with_all_values_from_template_definition = {}

        our_template = CiscoAAAModel(**dict_with_all_values_from_template_definition)

        return our_template


def get_datamodel_value():
    pass


def feed_datamodel_with_values(datamodel: BaseModel, values: Dict):
    pass


def get_value_from_datapath(datapath: List[str]) -> Any:
    if not datapath:
        return
