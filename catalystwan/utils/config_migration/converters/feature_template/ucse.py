from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.models.configuration.feature_profile.sdwan.other import UcseParcel
from catalystwan.models.configuration.feature_profile.sdwan.other.ucse import LomType


class UcseTemplateConverter:
    """
    A class for converting template values into a UcseParcel object.
    """

    supported_template_types = ("ucse",)

    @staticmethod
    def create_parcel(name: str, description: str, template_values: dict) -> UcseParcel:
        """
        Creates a UcseParcel object based on the provided template values.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            UcseParcel: A UcseParcel object with the provided values.
        """
        parcel_values = deepcopy(template_values)

        for interface_values in parcel_values.get("interface", []):
            ip = interface_values.pop("ip", None)
            if ip:
                interface_values["address"] = ip.get("static_case", {}).get("address")

        imc = parcel_values.get("imc", {})
        static_case = imc.get("ip", {}).get("static_case")
        if static_case:
            imc["ip"] = static_case

        access_port = imc.get("access_port", {})
        shared_lom = access_port.get("shared_lom")
        if shared_lom:
            lom_type = list(shared_lom.keys())[0]
            shared_lom.clear()
            access_port["shared_lom"]["lom_type"] = Global[LomType](value=lom_type)

        for key in ["module_type", "subslot_name"]:
            parcel_values.pop(key, None)

        parcel_values.update({"parcel_name": name, "parcel_description": description})
        return UcseParcel(**parcel_values)
