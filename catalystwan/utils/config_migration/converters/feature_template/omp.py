from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import OMPParcel


class OMPTemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> OMPParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        # advertise_ipv4: AdvertiseIpv4 = AdvertiseIpv4,
        # advertise_ipv6: AdvertiseIpv6 = AdvertiseIpv6,

        if template_values.get("advertise") is not None:
            template_values["advertise_ipv4"] = template_values["advertise"]
            del template_values["advertise"]
            set_true_protocols = {}
            for definition in template_values["advertise_ipv4"]:
                protocol = definition["protocol"].value
                set_true_protocols[protocol] = Global[bool](value=True)
            template_values["advertise_ipv4"] = set_true_protocols

        if template_values.get("ipv6_advertise") is not None:
            template_values["advertise_ipv6"] = template_values["ipv6_advertise"]
            del template_values["ipv6_advertise"]
            set_true_protocols = {}
            for definition in template_values["advertise_ipv6"]:
                protocol = definition["protocol"].value
                set_true_protocols[protocol] = Global[bool](value=True)
            template_values["advertise_ipv6"] = set_true_protocols

        print(template_values)
        return OMPParcel(**template_values)
