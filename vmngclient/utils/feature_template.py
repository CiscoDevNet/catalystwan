from typing import Optional, Type, TypeVar, Union, Dict

from vmngclient.api.templates.models.supported import FeatureTemplateType, supported_models
from vmngclient.exceptions import TemplateTypeError

T = TypeVar("T")


def choose_model(type_value: Union[str, FeatureTemplateType]) -> Type[T]:  # Is FeatureTemplate better?
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
    if isinstance(type_value, FeatureTemplateType):
        type_value = type_value.value
    for model in supported_models:
        if getattr(model, "type", None) == type_value:
            return model
    raise TemplateTypeError(f"Feature template type '{type_value}' is not supported.")


def find_template_values(
    template_definition: dict,
    fields_list: list = [],
    parent_key: Optional[str] = None,
    target_key: str = "vipType",
    target_key_value_to_ignore: str = "ignore",
    target_key_for_template_value: str = "vipValue",
) -> Dict[str, Union[str, list]]:
    """Based on provided template definition generates a dictionary with template fields and values

    Args:
        template_definition: template definition provided as dict
        fields_list: list containing tuples of fields and corresponding values
        parent_key: parent key provided to keep track of fields, defaults to None
        target_key: name of the key specifying if field is used in template, defaults to 'vipType'
        target_key_value_to_ignore: value of the target key indicating
            that field is not used in template, defaults to 'ignore'
        target_key_for_template_value: name of the key specifying value of field used in template,
            defaults to 'vipValue'

    Returns:
        templated_values: dictionary containing template fields as key and values assigned to them
    """
    for key, value in template_definition.items():
        if key == target_key and value != target_key_value_to_ignore:
            fields_list.append((parent_key, template_definition[target_key_for_template_value]))
        elif isinstance(value, dict):
            find_template_values(value, fields_list, key)
        elif isinstance(value, list) and key == target_key_for_template_value:
            for item in value:
                if isinstance(item, dict):
                    fields_list.append((parent_key, [find_template_values(item, [])]))
    templated_values = {}
    for key, value in fields_list:
        templated_values[key] = value
    return templated_values
