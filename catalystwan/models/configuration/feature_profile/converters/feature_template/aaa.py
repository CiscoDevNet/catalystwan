from catalystwan.models.configuration.feature_profile.sdwan.system import AAA


class AAATemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> AAA:
        """
        Creates an AAA object based on the provided template values.

        Returns:
            AAA: An AAA object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        delete_properties = (
            "radius_client",
            "radius_trustsec_group",
            "rda_server_key",
            "domain_stripping",
            "auth_type",
            "port",
            "cts_auth_list",
        )

        for prop in delete_properties:
            if template_values.get(prop) is not None:
                del template_values[prop]

        return AAA(**template_values)
