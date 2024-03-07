from copy import deepcopy
from typing import List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import AAAParcel


class AAATemplateConverter:
    supported_template_types = ("cisco_aaa", "cedge_aaa", "aaa")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> AAAParcel:
        """
        Creates an AAAParcel object based on the provided template values.

        Args:
            name (str): The name of the AAAParcel.
            description (str): The description of the AAAParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            AAAParcel: An AAAParcel object with the provided template values.
        """

        def assign_authorization_servers(auth_server_list: List) -> None:
            for auth_server in auth_server_list:
                servers = auth_server.get("server", {})
                for server in servers:
                    key_enum = server.get("key_enum")
                    server["key_enum"] = Global[str](value=str(key_enum.value))

        def assign_rules(rules: List) -> None:
            for rule_item in rules:
                rule_item["group"] = Global[List[str]](value=rule_item["group"].value.split(","))

        parcel_values = deepcopy(template_values)
        parcel_values["parcel_name"] = name
        parcel_values["parcel_description"] = description

        if server_auth_order := template_values.get("server_auth_order"):
            parcel_values["server_auth_order"] = Global[List[str]](value=server_auth_order.value.split(","))

        for server in ["radius", "tacacs"]:
            if auth_server_list := parcel_values.get(server):
                assign_authorization_servers(auth_server_list)

        for rule in ["accounting_rule", "authorization_rule"]:
            if existing_rule := parcel_values.get(rule):
                assign_rules(existing_rule)

        for key in [
            "radius_client",
            "radius_trustsec_group",
            "rda_server_key",
            "domain_stripping",
            "auth_type",
            "port",
            "cts_auth_list",
        ]:
            parcel_values.pop(key, None)

        return AAAParcel(**parcel_values)
