from typing import Union

from catalystwan.api.configuration_groups.parcel import as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.other import ThousandEyesParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.thousandeyes import (
    ProxyConfigNone,
    ProxyConfigPac,
    ProxyConfigStatic,
)


class ThousandEyesTemplateConverter:
    """
    A class for converting template values into a ThousandEyesParcel object.
    """

    supported_template_types = ("cisco_thousandeyes",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> ThousandEyesParcel:
        """
        Creates a ThousandEyesParcel object based on the provided template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            ThousandEyesParcel: A ThousandEyesParcel object with the provided values.
        """
        virtual_application = template_values["virtual_application"][0]["te"]

        if virtual_application.get("te_mgmt_ip"):
            virtual_application["te_mgmt_ip"] = as_variable("{{thousand_eyes_mgmt_ip}}")

        proxy_type = virtual_application.get("proxy_type", as_global("none"))
        if proxy_type is None:
            proxy_type == as_global("none")
        proxy_type = proxy_type.value

        proxy_config: Union[ProxyConfigNone, ProxyConfigPac, ProxyConfigStatic] = ProxyConfigNone()
        if proxy_type == "none":
            proxy_config = ProxyConfigNone()
        elif proxy_type == "pac":
            proxy_config = ProxyConfigPac(pac_url=virtual_application["proxy_pac"]["pac_url"])
        elif proxy_type == "static":
            proxy_config = ProxyConfigStatic(
                proxy_host=virtual_application["proxy_static"]["proxy_host"],
                proxy_port=virtual_application["proxy_static"]["proxy_port"],
            )

        virtual_application["proxy_config"] = proxy_config

        for key in ["proxy_type", "proxy_pac", "proxy_static", "proxy_port"]:
            virtual_application.pop(key, None)

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            "virtual_application": [virtual_application],
        }
        return ThousandEyesParcel(**parcel_values)  # type: ignore
