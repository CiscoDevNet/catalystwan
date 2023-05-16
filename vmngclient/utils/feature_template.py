from typing import Type, TypeVar, Union

from vmngclient.api.templates.models.supported import FeatureTemplateType, supported_models
from vmngclient.exceptions import TemplateTypeError

T = TypeVar("T")


def chose_model(type_value: Union[str, FeatureTemplateType]) -> Type[T]:
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
