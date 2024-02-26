from catalystwan.models.configuration.feature_profile.sdwan.system import LoggingParcel


class LoggingTemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> LoggingParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        if template_values.get("disk_enable"):
            template_values["disk"] = {
                "disk_enable": template_values["enable"],
                "file": {"disk_file_size": template_values["size"], "disk_file_rotate": template_values["rotate"]},
            }
            del template_values["enable"]
            del template_values["size"]
            del template_values["rotate"]

        return LoggingParcel(**template_values)
