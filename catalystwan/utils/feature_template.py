# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.models.supported import available_models
from catalystwan.exceptions import TemplateTypeError


def choose_model(type_value: str) -> Any:
    """Chooses correct model based on provided type

    With provided type of feature template searches supported by catalystwan models
    and returns correct for given type of feature template class.

    Args:
        type_value: type of feature template

    Returns:
        model

    Raises:
            TemplateTypeError: Raises when the model is not supported by catalystwan.
    """
    if type_value not in available_models:
        for model in available_models.values():
            if model.type == type_value:  # type: ignore
                return model
        raise TemplateTypeError(f"Feature template type '{type_value}' is not supported.")

    return available_models[type_value]


class FlattenedTemplateValue(BaseModel):
    value: Any
    data_path: List[str]


def flatten_template_definition(template_definition: Dict[str, Any]) -> Dict[str, List[FlattenedTemplateValue]]:
    def get_flattened_dict(
        template_definition: Dict[str, Any],
        flattened_dict: Dict[str, List[FlattenedTemplateValue]] = {},
        path: List[str] = [],
    ):
        for key, value in template_definition.items():
            if isinstance(value, dict):
                get_flattened_dict(value, flattened_dict, path=path + [key])
            else:
                if key not in flattened_dict:
                    flattened_dict[key] = []
                if isinstance(value, list) and all([isinstance(v, dict) for v in value]):
                    flattened_value = FlattenedTemplateValue(
                        value=[get_flattened_dict(v, {}) for v in value], data_path=path
                    )
                    flattened_dict[key].append(flattened_value)
                else:
                    flattened_dict[key].append(FlattenedTemplateValue(value=value, data_path=path))
        return flattened_dict

    flattened_dict: Dict[str, List[FlattenedTemplateValue]] = {}
    get_flattened_dict(template_definition, flattened_dict)
    return flattened_dict


def find_template_values(
    template_definition: dict,
    templated_values: dict = {},
    parent_key: Optional[str] = None,
    target_key: str = "vipType",
    target_key_value_to_ignore: str = "ignore",
    target_key_for_template_value: str = "vipValue",
    device_specific_variables: Optional[Dict[str, DeviceVariable]] = None,
    path: List[str] = [],
) -> Dict[str, Union[str, list, dict]]:
    """Based on provided template definition generates a dictionary with template fields and values

    Args:
        template_definition: template definition provided as dict
        templated_values: dictionary, empty at the beginning and filed out with names of fields as keys
            and values of those fields as values
        parent_key: parent key provided to keep track of fields, defaults to None
        target_key: name of the key specifying if field is used in template, defaults to 'vipType'
        target_key_value_to_ignore: value of the target key indicating
            that field is not used in template, defaults to 'ignore'
        target_key_for_template_value: name of the key specifying value of field used in template,
            defaults to 'vipValue'

    Returns:
        templated_values: dictionary containing template fields as key and values assigned to those fields as values
    """
    # if value object is reached, try to extract the value
    if target_key in template_definition and template_definition[target_key] != target_key_value_to_ignore:
        value = template_definition[target_key]
        template_value = template_definition[target_key_for_template_value]
        current_dict = templated_values
        for path_key in path[:-1]:
            if path_key not in current_dict:
                current_dict[path_key] = {}
            current_dict = current_dict[path_key]
        current_dict[path[-1]] = template_value

        if value == "variableName" and (device_specific_variables is not None) and parent_key:
            device_specific_variables[parent_key] = DeviceVariable(name=template_definition["vipVariableName"])
        elif template_definition["vipObjectType"] != "tree":
            current_dict[path[-1]] = template_value
        elif isinstance(template_value, dict):
            find_template_values(
                value, templated_values, parent_key, device_specific_variables=device_specific_variables, path=path
            )
        elif isinstance(template_value, list):
            current_dict[path[-1]] = []
            for item in template_value:
                current_dict[path[-1]].append(
                    find_template_values(item, {}, device_specific_variables=device_specific_variables)
                )

        return templated_values

    # iterate the dict to extract values and assign them to their fields
    for key, value in template_definition.items():
        if isinstance(value, dict) and value != target_key_value_to_ignore:
            find_template_values(
                value, templated_values, key, device_specific_variables=device_specific_variables, path=path + [key]
            )
        elif (
            isinstance(value, list)
            and key == target_key_for_template_value
            and template_definition.get(target_key) != target_key_value_to_ignore
            and all([isinstance(v, dict) for v in value])
        ):
            templated_values[parent_key] = []
            for item in value:
                templated_values[parent_key].append(
                    find_template_values(
                        item, {}, device_specific_variables=device_specific_variables, path=path + [key]
                    )
                )
    return templated_values
