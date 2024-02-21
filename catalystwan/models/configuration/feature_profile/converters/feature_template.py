from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.models.configuration.feature_profile.converters.normalizator import template_definition_normalization
from catalystwan.models.configuration.feature_profile.factories import AnyFactory, supported_parcel_factories


def choose_parcel_factory(template_type: str) -> AnyFactory:
    """
    This function is used to choose the correct parcel factory based on the template type.

    Args:
        template_type (str): The template type used to determine the correct factory.

    Returns:
        BaseFactory: The chosen parcel factory.

    Raises:
        ValueError: If the template type is not supported.
    """
    for key in supported_parcel_factories.keys():
        if template_type in key:
            return supported_parcel_factories[key]
    raise ValueError(f"Template type {template_type} not supported")


def create_parcel_from_template(template: FeatureTemplateInformation) -> _ParcelBase:
    """
    Creates a new instance of a _ParcelBase based on the given template.

    Args:
        template (FeatureTemplateInformation): The template to use for creating the _ParcelBase instance.

    Returns:
        _ParcelBase: The created _ParcelBase instance.

    Raises:
        ValueError: If the given template type is not supported.
    """
    factory = choose_parcel_factory(template.template_type)
    template_values = template_definition_normalization(template.template_definiton)
    print(template_values)
    factory_instance = factory(template.name, template.description, template_values)  # type: ignore[operator]
    return factory_instance.create_parcel()
