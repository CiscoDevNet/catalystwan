from copy import deepcopy

from catalystwan.models.configuration.feature_profile.sdwan.system import NTPParcel


class NTPTemplateConverter:
    supported_template_types = ("cisco_ntp", "ntp")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> NTPParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        parcel_values = deepcopy(template_values)
        parcel_values["parcel_name"] = name
        parcel_values["parcel_description"] = description
        return NTPParcel(**parcel_values)
