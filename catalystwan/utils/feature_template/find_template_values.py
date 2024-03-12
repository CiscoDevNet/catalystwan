from typing import Any, Dict, List, Optional, Union

from catalystwan.api.templates.device_variable import DeviceVariable


def find_template_values(
    template_definition: dict,
    templated_values: Optional[dict] = None,
    target_key: str = "vipType",
    target_key_value_to_ignore: str = "ignore",
    target_key_for_template_value: str = "vipValue",
    device_specific_variables: Optional[Dict[str, DeviceVariable]] = None,
    path: Optional[List[str]] = None,
) -> Dict[str, Union[str, list, dict]]:
    """Based on provided template definition generates a dictionary with template fields and values

    Args:
        template_definition: template definition provided as dict
        templated_values: dictionary, empty at the beginning and filed out with names of fields as keys
            and values of those fields as values
        target_key: name of the key specifying if field is used in template, defaults to 'vipType'
        target_key_value_to_ignore: value of the target key indicating
            that field is not used in template, defaults to 'ignore'
        target_key_for_template_value: name of the key specifying value of field used in template,
            defaults to 'vipValue'
        path: a list of keys indicating current path, defaults to None
    Returns:
        templated_values: dictionary containing template fields as key and values assigned to those fields as values
    """
    if path is None:
        path = []
    if templated_values is None:
        templated_values = {}
    # if value object is reached, try to extract the value
    if target_key in template_definition:
        if template_definition[target_key] == target_key_value_to_ignore:
            return templated_values

        value = template_definition[target_key]
        template_value = template_definition.get(target_key_for_template_value)

        field_key = path[-1]
        # TODO: Handle nested DeviceVariable
        if value == "variableName":
            if device_specific_variables is not None:
                device_specific_variables[field_key] = DeviceVariable(name=template_definition["vipVariableName"])
            return template_definition
        if template_value is None:
            return template_definition

        if template_definition["vipType"] == "variable":
            if device_specific_variables is not None and template_value:
                device_specific_variables[field_key] = DeviceVariable(name=template_value)
        elif template_definition["vipObjectType"] == "list":
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = []
            for item in template_value:
                current_nesting[field_key].append(process_list_value(item))
        elif template_definition["vipObjectType"] != "tree":
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = template_value
        elif isinstance(template_value, dict):
            find_template_values(
                value, templated_values, device_specific_variables=device_specific_variables, path=path
            )
        elif isinstance(template_value, list):
            current_nesting = get_nested_dict(templated_values, path[:-1])
            current_nesting[field_key] = []
            for item in template_value:
                item_value = find_template_values(item, {}, device_specific_variables=device_specific_variables)
                if item_value:
                    current_nesting[field_key].append(item_value)
        return templated_values

    # iterate the dict to extract values and assign them to their fields
    for key, value in template_definition.items():
        if isinstance(value, dict) and value != target_key_value_to_ignore:
            find_template_values(
                value, templated_values, device_specific_variables=device_specific_variables, path=path + [key]
            )
    return templated_values


def get_nested_dict(d: dict, path: List[str], populate: bool = True):
    current_dict = d
    for path_key in path:
        if path_key not in current_dict and populate:
            current_dict[path_key] = {}
        current_dict = current_dict[path_key]
    return current_dict


def process_list_value(item: Any, target_key: str = "vipType", target_key_for_template_value: str = "vipValue"):
    if isinstance(item, dict):
        if target_key in item:
            if item["vipObjectType"] == "list":
                result = []
                for nested_item in item[target_key_for_template_value]:
                    result.append(process_list_value(nested_item))
                return result
            elif item["vipObjectType"] == "tree":
                return find_template_values(item[target_key_for_template_value])
            else:
                return item[target_key_for_template_value]
        else:
            return find_template_values(item)
    else:
        return item
