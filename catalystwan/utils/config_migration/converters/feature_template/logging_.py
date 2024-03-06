from typing import List

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.system import LoggingParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import CypherSuite


class LoggingTemplateConverter:
    supported_template_types = ("cisco_logging", "logging")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> LoggingParcel:
        """
        Creates an Logging object based on the provided template values.

        Returns:
            Logging: An Logging object with the provided template values.
        """
        template_values["name"] = name
        template_values["description"] = description

        if template_values.get("tls_profile"):
            tls_profiles = template_values["tls_profile"]
            for profile in tls_profiles:
                del profile["auth_type"]
                if profile.get("ciphersuite_list"):
                    profile["ciphersuite_list"] = Global[List[CypherSuite]](value=profile["ciphersuite_list"].value)

        if template_values.get("server"):
            servers = template_values["server"]
            for server in servers:
                server["name"] = Global[str](value=str(server["name"].value))

        if template_values.get("ipv6_server"):
            ipv6_servers = template_values["ipv6_server"]
            for server in ipv6_servers:
                server["name"] = Global[str](value=str(server["name"].value))

        if template_values.get("enable") is not None:
            template_values["disk"] = {
                "disk_enable": template_values["enable"],
                "file": {"disk_file_size": template_values["size"], "disk_file_rotate": template_values["rotate"]},
            }
            del template_values["enable"]
            del template_values["size"]
            del template_values["rotate"]

        return LoggingParcel(**template_values)
