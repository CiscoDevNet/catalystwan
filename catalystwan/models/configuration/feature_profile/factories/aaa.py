from catalystwan.models.configuration.feature_profile.factories.base import BaseFactory
from catalystwan.models.configuration.feature_profile.sdwan.system import AAA


class AAAFactory(BaseFactory):
    DELETE_PROPERTIES: tuple = (
        "radius_client",
        "radius_trustsec_group",
        "rda_server_key",
        "domain_stripping",
        "auth_type",
        "port",
        "cts_auth_list",
    )

    def create_parcel(self):
        """
        Creates an AAA object based on the provided template values.

        Returns:
            AAA: An AAA object with the provided template values.
        """
        return AAA(**self.template_values)
