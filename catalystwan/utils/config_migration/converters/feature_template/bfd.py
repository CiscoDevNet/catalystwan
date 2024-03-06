from catalystwan.models.configuration.feature_profile.sdwan.system import BFDParcel


class BFDTemplateConverter:
    supported_template_types = ("cisco_bfd",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> BFDParcel:
        """
        Creates an BFD object based on the provided template values.

        Returns:
            BFD: An BFD object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        if template_values.get("color") is not None:
            template_values["colors"] = template_values["color"]
            del template_values["color"]

        return BFDParcel(**template_values)
