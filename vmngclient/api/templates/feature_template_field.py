from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from vmngclient.api.templates.device_variable import DeviceVariable


class FeatureTemplateOptionType(str, Enum):
    CONSTANT = "constant"
    VARIABLE = "variable"
    IGNORE = "ignore"
    NOT_IGNORE = "notIgnore"
    VARIABLE_NAME = "variableName"


class FeatureTemplateObjectType(str, Enum):
    OBJECT = "object"
    TREE = "tree"
    LIST = "list"  # TODO Use comma(,) for multiple values
    NODE_ONLY = "node-only"  # No information about the value


class VipVariable(BaseModel, frozen=True):
    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True

    value: Any = Field(alias="vipValue")
    type: FeatureTemplateOptionType = Field(alias="vipType")
    object_type: FeatureTemplateObjectType = Field(alias="vipObjectType")
    device_specific_name: Optional[str] = Field(default=None, alias="vipVariableName")
    primary_key: Optional[Any] = Field(default=None, alias="vipPrimaryKey")


def get_path_dict(paths: List[List[str]]) -> dict:
    """Builds a tree like structure out of a list of paths"""

    def _recurse(tmp_dict: dict, chain: List[str]):
        if len(chain) == 0:
            return

        key, *tail = chain

        if key not in tmp_dict:
            tmp_dict[key] = dict()  # Value for every new dict. Changed in-place.

        _recurse(tmp_dict[key], tail)
        return

    new_path_dict: Dict[str, Any] = {}
    for path in paths:
        _recurse(new_path_dict, path)

    return new_path_dict


class FeatureTemplateField(BaseModel):
    # TODO aliases
    key: str
    description: str = ""
    details: str = ""
    optionType: List[FeatureTemplateOptionType]
    defaultOption: FeatureTemplateOptionType
    dataPath: List[str] = []
    objectType: FeatureTemplateObjectType
    dataType: Dict[str, Any] = {}
    primaryKeys: List[str] = []
    children: List[FeatureTemplateField] = []

    @validator("dataType", pre=True)
    def convert_data_type_to_dict(cls, value):
        if isinstance(value, str):
            return {"type": value}
        return value

    def data_path(self, output):
        for child in self.children:
            output.update(child.data_path(output))
        output.update(get_path_dict([t.dataPath for t in self.children]))

        return output

    # value must be JSON serializable, return JSON serializable dict
    def payload_scheme(self, value: Any = None, help=None) -> dict:
        output: dict = {}

        for child in self.children:
            for path in child.dataPath:
                if not output.get(path):
                    output[path] = {}
                output = output[path]

        output["vipObjectType"] = self.objectType.value

        if isinstance(value, DeviceVariable):
            vip_variable = VipVariable(
                vipValue="",
                vipType=FeatureTemplateOptionType.VARIABLE_NAME,
                vipObjectType=self.objectType,
                vipVariableName=value.name,
            )

            return {self.key: vip_variable.dict(by_alias=True, exclude_none=True)}
        else:
            if value:
                output["vipType"] = FeatureTemplateOptionType.CONSTANT.value
                if self.children:
                    children_output = []

                    for obj in value:  # obj is User
                        child_payload = {}
                        for child in self.children:
                            child_payload.update(child.payload_scheme(obj[child.key]))
                        children_output.append(child_payload)
                    output["vipValue"] = children_output
                else:
                    if self.dataType.get("type") == "enum": # TODO BaseModel
                        variables = [
                            VipVariable(
                                vipValue=e,
                                vipType=FeatureTemplateOptionType.CONSTANT,
                                vipObjectType=FeatureTemplateObjectType.OBJECT
                            ) for e in value
                        ]
                        value = variables
                    output["vipValue"] = value
            else:
                if "default" in self.dataType:
                    output["vipValue"] = self.dataType["default"] if value is None else value
                    output["vipType"] = self.defaultOption.value
                else:
                    output["vipValue"] = []
                    output["vipType"] = FeatureTemplateOptionType.IGNORE.value

        # TODO
        # DataType to dataclass Model
        # No default values for everything

        if self.primaryKeys:
            output["vipPrimaryKey"] = self.primaryKeys

        real_output = {self.key: output}
        return real_output
