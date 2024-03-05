from catalystwan.models.configuration.feature_profile.sdwan.system import GlobalParcel


class GlobalTemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> GlobalParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        template_values["services_global"] = {}
        template_values["services_global"]["services_ip"] = {}

        keys_to_delete = []
        for key, value in template_values.items():
            template_values["services_global"]["services_ip"][key] = value
            keys_to_delete.append(key)

        for key in keys_to_delete:
            del template_values[key]

        template_values["name"] = name
        template_values["description"] = description
        return GlobalParcel(**template_values)
