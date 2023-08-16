# type: ignore

from vmngclient.api.templates.models.cisco_vpn_model import CiscoVPNModel, Dns, DnsIpv6, Host, NextHop, Routev4, Routev6
from vmngclient.utils.device_model import DeviceModel

basic_cisco_vpn = CiscoVPNModel(
    name="Basic_Cisco_VPN_Model", description="Primitive", device_models=[DeviceModel.VEDGE_C8000V]
)  # type: ignore


complex_cisco_vpn = CiscoVPNModel(
    name="Complex_CiscoVPN_Model",
    description="Complex",
    device_models=[DeviceModel.VEDGE_C8000V],
    vpn_id=123,
    vpn_name="VPN",
    layer4=True,
    omp_admin_distance_ipv4=255,
    dns=[Dns(dns_addr="255.255.255.0")],
    host=[Host(hostname="random", ip=["1.1.1.1", "2.2.2.2"])],
    dns_ipv6=[DnsIpv6(dns_addr="30a8:b25e:3db5:fe9f:231f:7478:4181:9234")],
    route_v4=[Routev4(prefix="1.1.1.1/24", null0=True, distance=5, next_hop=[NextHop(address="1.1.1.1")])],
    route_v6=[
        Routev6(prefix="2001:db8:1234::/48", next_hop=[NextHop(address="2001:db8:1234:0000:0000:0000:0000:0000")])
    ],
)
