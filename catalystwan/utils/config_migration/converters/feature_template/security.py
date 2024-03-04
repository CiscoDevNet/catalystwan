from typing import List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import SecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.security import IntegrityType


class SecurityTemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> SecurityParcel:
        """
        Creates an AAA object based on the provided template values.

        Returns:
            AAA: An AAA object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        if template_values.get("integrity_type") is not None:
            template_values["integrity_type"] = Global[List[IntegrityType]](
                value=template_values["integrity_type"].value
            )

        if template_values.get("authentication_type") is not None:
            del template_values["authentication_type"]

        return SecurityParcel(**template_values)
