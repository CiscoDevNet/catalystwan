from typing import Any, Dict, Optional, Union

from vmngclient.api.templates.device_variable import DeviceVariable
from vmngclient.api.templates.models.supported import available_models
from vmngclient.exceptions import TemplateTypeError


def choose_model(type_value: str) -> Any:
    """Chooses correct model based on provided type

    With provided type of feature template searches supported by vmngclient models
    and returns correct for given type of feature template class.

    Args:
        type_value: type of feature template

    Returns:
        model

    Raises:
            TemplateTypeError: Raises when the model is not supported by vmngclient.
    """
    if type_value not in available_models:
        for model in available_models.values():
            if model.type == type_value:  # type: ignore
                return model
        raise TemplateTypeError(f"Feature template type '{type_value}' is not supported.")

    return available_models[type_value]


def find_template_values(
    template_definition: dict,
    templated_values: dict = {},
    parent_key: Optional[str] = None,
    target_key: str = "vipType",
    target_key_value_to_ignore: str = "ignore",
    target_key_for_template_value: str = "vipValue",
    device_specific_variables: Optional[Dict[str, DeviceVariable]] = None,
) -> Dict[str, Union[str, list]]:
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
    for key, value in template_definition.items():
        if key == target_key and value != target_key_value_to_ignore:
            if value == "variableName" and (device_specific_variables is not None) and parent_key:
                device_specific_variables[parent_key] = DeviceVariable(name=template_definition["vipVariableName"])
            else:
                templated_values[parent_key] = template_definition[target_key_for_template_value]
        elif isinstance(value, dict) and value != target_key_value_to_ignore:
            find_template_values(value, templated_values, key, device_specific_variables=device_specific_variables)
        elif (
            isinstance(value, list)
            and key == target_key_for_template_value
            and template_definition.get(target_key) != target_key_value_to_ignore
            and all([isinstance(v, dict) for v in value])
        ):
            templated_values[parent_key] = []
            for item in value:
                templated_values[parent_key].append(
                    find_template_values(item, {}, device_specific_variables=device_specific_variables)
                )
    return templated_values
