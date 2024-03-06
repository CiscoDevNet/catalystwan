from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import ConsoleBaudRate


class SystemToBasicTemplateConverter:
    supported_template_types = ("cisco_system", "system-vsmart", "system-vedge")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> BasicParcel:
        """
        Creates an AAA object based on the provided template values.

        Returns:
            AAA: An AAA object with the provided template values.
        """
        template_values["name"] = name
        template_values["parcel_description"] = description
        if template_values.get("console_baud_rate") is not None:
            value = template_values["console_baud_rate"].value
            if value == "":
                value = "9600"  # Default value for console baud rate
            template_values["console_baud_rate"] = Global[ConsoleBaudRate](value=value)

        if template_values.get("site_id") is not None:
            del template_values["site_id"]
        if template_values.get("system_ip") is not None:
            del template_values["system_ip"]
        if template_values.get("host_name") is not None:
            del template_values["host_name"]
        if template_values.get("enable") is not None:
            del template_values["enable"]
        return BasicParcel(**template_values)
