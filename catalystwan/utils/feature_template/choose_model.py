from typing import Any

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
