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
        return NTPParcel(parcel_name=name, parcel_description=description, **template_values)
