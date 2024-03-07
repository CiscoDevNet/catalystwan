from catalystwan.models.configuration.feature_profile.sdwan.system import GlobalParcel


class GlobalTemplateConverter:
    supported_template_types = ("cedge_global",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> GlobalParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            GlobalParcel: A GlobalParcel object with the provided template values.
        """
        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "services_global": {"services_ip": {key: value for key, value in template_values.items()}},
        }
        return GlobalParcel(**parcel_values)  # type: ignore
