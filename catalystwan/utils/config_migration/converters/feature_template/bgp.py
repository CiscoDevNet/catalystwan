from copy import deepcopy
from typing import Dict, List, cast

from catalystwan.api.configuration_groups.parcel import as_variable
from catalystwan.models.configuration.feature_profile.sdwan.transport import BGPParcel


class BGPTemplateConverter:
    supported_template_types = ("bgp", "cisco_bgp")

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> BGPParcel:
        """
        Creates a BannerParcel object based on the provided template values.

        Args:
            name (str): The name of the BannerParcel.
            description (str): The description of the BannerParcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            BannerParcel: A BannerParcel object with the provided template values.
        """
        device_specific_ipv4_neighbor_address = "{{{{lbgp_1_neighbor_{index}_address}}}}"

        parcel_values = {"parcel_name": name, "parcel_description": description, **deepcopy(template_values["bgp"])}

        shutdown = parcel_values.get("shutdown")
        neighbors = cast(List[Dict], parcel_values.get("neighbor", []))
        if neighbors:
            for i, neighbor in enumerate(neighbors):
                if neighbor.get("address") is None:
                    neighbor["address"] = as_variable(device_specific_ipv4_neighbor_address.format(index=(i + 1)))
                if if_name := neighbor.get("update_source", {}).get("if_name"):
                    neighbor["if_name"] = if_name
                    neighbor.pop("update_source")
                if shutdown is not None:
                    neighbor["shutdown"] = shutdown

        for key in ["address_family", "shutdown"]:
            parcel_values.pop(key, None)

        return BGPParcel(**parcel_values)  # type: ignore
