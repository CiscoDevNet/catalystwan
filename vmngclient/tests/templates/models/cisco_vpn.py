from vmngclient.api.templates.models.cisco_vpn_model import CiscoVPNModel
from vmngclient.utils.device_model import DeviceModel

basic_cisco_vpn = CiscoVPNModel(
    name="Basic_Cisco_VPN_Model", description="Primitive", device_models=[DeviceModel.VEDGE_C8000V]
)  # type: ignore
