from typing import Optional, Type, TypeVar, Union

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
    data: dict,
    final_list: list = [],
    target_key: str = "vipType",
    target_key_for_value: str = "vipValue",
    parent_key: Optional[str] = None,
):
    for key, value in data.items():
        if key == target_key and value != "ignore":
            final_list.append((parent_key, data[target_key_for_value]))
        elif isinstance(value, dict):
            find_template_values(value, final_list, target_key, target_key_for_value, key)
        elif isinstance(value, list) and key == target_key_for_value:
            for item in value:
                if isinstance(item, dict):
                    final_list.append((parent_key, [find_template_values(item, [])]))
    result = {}
    for key, value in final_list:
        result[key] = value
    return result
