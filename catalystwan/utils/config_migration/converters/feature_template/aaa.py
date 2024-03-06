from typing import List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import AAAParcel


class AAATemplateConverter:
    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> AAAParcel:
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

        if template_values.get("server_auth_order") is not None:
            global_object = template_values["server_auth_order"]
            template_values["server_auth_order"] = Global[List[str]](value=global_object.value.split(","))

        if template_values.get("radius") is not None:
            radius_list = template_values["radius"]
            for radius in radius_list:
                servers = radius.get("server", {})
                for server in servers:
                    key_enum = server.get("key_enum")
                    server["key_enum"] = Global[str](value=str(key_enum.value))

        if template_values.get("tacacs") is not None:
            tacacs_list = template_values["tacacs"]
            for tacacs in tacacs_list:
                servers = tacacs.get("server", {})
                for server in servers:
                    key_enum = server.get("key_enum")
                    server["key_enum"] = Global[str](value=str(key_enum.value))

        if template_values.get("accounting_rule") is not None:
            accounting_rule = template_values["accounting_rule"]
            for rule_item in accounting_rule:
                rule_item["group"] = Global[List[str]](value=rule_item["group"].value.split(","))

        if template_values.get("authorization_rule") is not None:
            authorization_rule = template_values["authorization_rule"]
            for rule_item in authorization_rule:
                rule_item["group"] = Global[List[str]](value=rule_item["group"].value.split(","))

        for prop in delete_properties:
            if template_values.get(prop) is not None:
                del template_values[prop]

        return AAAParcel(**template_values)
