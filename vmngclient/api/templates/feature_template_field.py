from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic.v1 import BaseModel, Field, validator
from pydantic.v1.fields import ModelField  # type: ignore

from vmngclient.api.templates.device_variable import DeviceVariable
from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.dict import merge


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


class VipVariable(BaseModel):
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
    def payload_scheme(
        self, value: Any = None, help=None, current_path=None, priority_order=None, vip_type=None
    ) -> dict:
        output: dict = {}
        rel_output: dict = {}
        rel_output.update(get_path_dict([self.dataPath]))

        output["vipObjectType"] = self.objectType.value

        def nest_value_in_output(value: Any) -> dict:
            pointer = rel_output
            for path in self.dataPath:
                pointer = pointer[path]
            pointer[self.key] = value
            return rel_output

        if isinstance(value, DeviceVariable):
            vip_variable = VipVariable(
                vipValue="",
                vipType=FeatureTemplateOptionType.VARIABLE_NAME,
                vipObjectType=self.objectType,
                vipVariableName=value.name,
            )
            return nest_value_in_output(vip_variable.dict(by_alias=True, exclude_none=True))

        else:
            if value is not None:
                output["vipType"] = vip_type or FeatureTemplateOptionType.CONSTANT.value
                if self.children:
                    children_output = []

                    for obj in value:  # obj is User, atomic value. Loop every child
                        child_payload: dict = {}
                        for child in self.children:  # Child in schema
                            if current_path is None:
                                current_path = []
                            obj: FeatureTemplate  # type: ignore
                            model_field: ModelField = next(
                                filter(
                                    lambda f: f.field_info.extra.get("data_path", []) == child.dataPath
                                    and (f.alias == child.key or f.field_info.extra.get("vmanage_key") == child.key),
                                    obj.__fields__.values(),
                                )
                            )
                            obj_value = getattr(obj, model_field.name)
                            po = model_field.field_info.extra.get("priority_order")
                            vip_type = model_field.field_info.extra.get("vip_type")
                            merge(
                                child_payload,
                                child.payload_scheme(
                                    obj_value,
                                    help=output,
                                    current_path=self.dataPath + [self.key],
                                    priority_order=po,
                                    vip_type=vip_type,
                                ),
                            )
                            if priority_order:
                                child_payload.update({"priority-order": priority_order})
                        children_output.append(child_payload)
                    output["vipValue"] = children_output
                else:
                    output["vipValue"] = value
            else:
                if value is None:
                    return {}
                if "default" in self.dataType:
                    return {}
                    # output["vipValue"] = self.dataType["default"] if value is None else value
                    # output["vipType"] = self.defaultOption.value
                else:
                    output["vipValue"] = []
                    output["vipType"] = FeatureTemplateOptionType.IGNORE.value

        # TODO
        # DataType to dataclass Model
        # No default values for everything

        if self.primaryKeys:
            output["vipPrimaryKey"] = self.primaryKeys

        return nest_value_in_output(output)
