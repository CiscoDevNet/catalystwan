from typing import List

from catalystwan.api.configuration_groups.parcel import Global, as_default
from catalystwan.models.configuration.feature_profile.sdwan.system import SecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.security import IntegrityType


class SecurityTemplateConverter:
    """
    A class for converting template values into a SecurityParcel object.

    Attributes:
        supported_template_types (tuple): A tuple of supported template types.
    """

    supported_template_types = (
        "cisco_security",
        "security",
        "security-vsmart",
        "security-vedge",
    )

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> SecurityParcel:
        """
        Creates a SecurityParcel object based on the provided template values.

        Args:
            name (str): The name of the SecurityParcel.
            description (str): The description of the SecurityParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            SecurityParcel: A SecurityParcel object with the provided template values.
        """
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
        }
        if integrity_type := template_values.get("integrity_type", as_default([])).value:
            parcel_values["integrity_type"] = Global[List[IntegrityType]](value=integrity_type)  # type: ignore
        return SecurityParcel(**parcel_values)  # type: ignore
