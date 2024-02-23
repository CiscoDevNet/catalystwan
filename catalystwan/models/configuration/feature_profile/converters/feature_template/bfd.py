from catalystwan.models.configuration.feature_profile.sdwan.system import BFD


class BFDTemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> BFD:
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

        return BFD(**template_values)
