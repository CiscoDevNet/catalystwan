from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel


class FeatureTemplateOptionType(Enum):
    CONSTANT = "constant"
    VARIABLE = "variable"
    IGNORE = "ignore"
    NOT_IGNORE = "notIgnore"


class FeatureTemplateObjectType(Enum):
    OBJECT = "object"
    TREE = "tree"
    LIST = "list"  # TODO Use comma(,) for multiple values
    NODE_ONLY = "node-only"  # No information about the value


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
    description: str
    details: str
    optionType: List[FeatureTemplateOptionType]
    defaultOption: FeatureTemplateOptionType
    dataPath: List[str] = []
    objectType: FeatureTemplateObjectType
    dataType: dict = {}
    primaryKeys: List[str] = []
    children: List[FeatureTemplateField] = []

    def data_path(self, output):
        for child in self.children:
            child.data_path(output)
        output.update(get_path_dict([t.dataPath for t in self.children]))

        return output

    # value must be JSON serializable, return JSON serializable dict
    def payload_scheme(self, value: Any = None, help=None) -> dict:
        output = help if help else {}
        output = {}

        for child in self.children:
            for path in child.dataPath:
                output = output[path]

        output["vipObjectType"] = self.objectType.value

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
