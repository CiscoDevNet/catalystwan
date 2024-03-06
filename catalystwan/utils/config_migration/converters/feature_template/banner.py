from catalystwan.models.configuration.feature_profile.sdwan.system import BannerParcel


class BannerTemplateConverter:
    supported_template_types = ("cisco_banner",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> BannerParcel:
        """
        Creates an AAA object based on the provided template values.

        Returns:
            AAA: An AAA object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description
        return BannerParcel(**template_values)
