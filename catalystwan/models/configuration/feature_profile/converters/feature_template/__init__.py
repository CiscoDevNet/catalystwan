from typing import Any, Dict, List

from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel

from .aaa import AAATemplateConverter
from .base import FeatureTemplateConverter
from .bfd import BFDTemplateConverter
from .normalizator import template_definition_normalization

supported_parcel_converters: Dict[Any, FeatureTemplateConverter] = {
    ("cisco_aaa", "cedge_aaa"): AAATemplateConverter,  # type: ignore[dict-item]
    ("cisco_bfd",): BFDTemplateConverter,  # type: ignore[dict-item]
}


def choose_parcel_converter(template_type: str) -> FeatureTemplateConverter:
    """
    This function is used to choose the correct parcel factory based on the template type.

    Args:
        template_type (str): The template type used to determine the correct factory.

    Returns:
        BaseFactory: The chosen parcel factory.

    Raises:
        ValueError: If the template type is not supported.
    """
    for key in supported_parcel_converters.keys():
        if template_type in key:
            return supported_parcel_converters[key]
    raise ValueError(f"Template type {template_type} not supported")


def create_parcel_from_template(template: FeatureTemplateInformation) -> AnySystemParcel:
    """
    Creates a new instance of a _ParcelBase based on the given template.

    Args:
        template (FeatureTemplateInformation): The template to use for creating the _ParcelBase instance.

    Returns:
        _ParcelBase: The created _ParcelBase instance.

    Raises:
        ValueError: If the given template type is not supported.
    """
    converter = choose_parcel_converter(template.template_type)
    template_values = template_definition_normalization(template.template_definiton)
    return converter.create_parcel(template.name, template.description, template_values)


__all__ = ["create_parcel_from_template"]


def __dir__() -> "List[str]":
    return list(__all__)
