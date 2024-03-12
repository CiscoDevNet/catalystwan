from copy import deepcopy
from ipaddress import IPv4Address, IPv4Network
from typing import List

from catalystwan.api.configuration_groups.parcel import Global, as_global, as_variable
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    LanVpnDhcpServerParcel,
    SubnetMask,
)


class DhcpTemplateConverter:
    supported_template_types = ("dhcp", "cisco_dhcp_server")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> LanVpnDhcpServerParcel:
        """
        Create a LanVpnDhcpServerParcel object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): The template values used to populate the parcel.

        Returns:
            LanVpnDhcpServerParcel: The created LanVpnDhcpServerParcel object.

        """

        def convert_str_list_to_ipv4_list(d: dict, key: str) -> None:
            """
            Convert a list of strings representing IPv4 addresses to a list of IPv4Address objects.

            Args:
                d (dict): The dictionary containing the key-value pair to be converted.
                key (str): The key in the dictionary representing the list of strings.

            Returns:
                None. The function modifies the dictionary in-place by
                replacing the list of strings with a list of IPv4Address objects.
            """
            if str_list := d.get(key, as_global([])).value:
                d[key] = Global[List[IPv4Address]](value=[IPv4Address(ip) for ip in str_list])

        values = deepcopy(template_values)
        values.update(values.pop("options", {}))

        if address_pool := values.get("address_pool"):
            value = address_pool.value
            network = IPv4Network(value)
            address = as_global(network.network_address)
            mask = as_global(str(network.netmask), SubnetMask)
            values["address_pool"] = {"network_address": address, "subnet_mask": mask}

        for key in ("exclude", "dns_servers", "tftp_servers"):
            convert_str_list_to_ipv4_list(values, key)

        if static_leases := values.get("static_lease", []):
            mac_address_variable = "{{{{dhcp_1_staticLease_{}_macAddress}}}}"
            ip_variable = "{{{{dhcp_1_staticLease_{}_ip}}}}"
            static_lease = []
            for i, entry in enumerate(static_leases):
                static_lease.append(
                    {
                        "mac_address": entry.get("mac_address", as_variable(mac_address_variable.format(i + 1))),
                        "ip": entry.get("ip", as_variable(ip_variable.format(i + 1))),
                    }
                )
            values["static_lease"] = static_lease

        parcel_values = {
            "parcel_name": name,
            "parcel_description": description,
            **values,
        }

        return LanVpnDhcpServerParcel(**parcel_values)  # type: ignore
