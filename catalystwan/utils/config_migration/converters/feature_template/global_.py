from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import as_variable
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
        values = deepcopy(template_values)
        if source_intrf := values.get("source_intrf"):
            values["source_intrf"] = as_variable(source_intrf.value)

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "services_global": {"services_ip": {key: value for key, value in values.items()}},
        }
        return GlobalParcel(**parcel_values)  # type: ignore
