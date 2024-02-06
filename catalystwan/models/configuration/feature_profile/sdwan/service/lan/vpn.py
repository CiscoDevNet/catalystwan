from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.common import RefId
from catalystwan.models.configuration.feature_profile.common import Prefix


class DnsIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_dns_address_ipv4: Union[Variable, Global[str], Default[None]] = Field(alias="primaryDnsAddressIpv4")
    secondary_dns_address_ipv4: Union[Variable, Global[str], Default[None]] = Field(alias="secondaryDnsAddressIpv4")


class DnsIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    primary_dns_address_ipv6: Union[Variable, Global[str], Default[None]] = Field(alias="primaryDnsAddressIpv6")
    secondary_dns_address_ipv6: Union[Variable, Global[str], Default[None]] = Field(alias="secondaryDnsAddressIpv6")


class HostMapping(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    host_name: Union[Variable, Global[str]] = Field(alias="hostName")
    list_of_ip: Union[Variable, Global[str]] = Field(alias="listOfIp")


class ProtocolIPv4(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"
    OSPFv3 = "opsfv3"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"
    EIGRP = "eigrp"
    LISP = "lisp"
    ISIS = "isis"


class ProtocolIPv6(str, Enum):
    BGP = "BGP"
    OSPF = "OSPF"
    CONNECTED = "connected"
    STATIC = "static"
    NETWORK = "network"
    AGGREGATE = "aggregate"


class Region(str, Enum):
    CORE_AND_ACCESS = "core-and-access"
    CORE = "core"
    ACCESS = "access"


class RoutePrefix(BaseModel):
    ip_address: Union[Variable, Global[str]] = Field(alias="ipAddress")
    subnet_mask: Union[Variable, Global[str]] = Field(alias="subnetMask")


class IPv4Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    aggregate_only: Optional[Union[Global[bool], Default[bool]]] = Field(alias="aggregateOnly", default=None)
    region: Optional[Union[Variable, Global[Region], Default[str]]] = None


class IPv6Prefix(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Union[Global[str], Variable]
    aggregate_only: Optional[Union[Global[bool], Default[bool]]] = Field(alias="aggregateOnly", default=None)
    region: Optional[Union[Variable, Global[Region], Default[str]]] = None


class OmpAdvertiseIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    omp_protocol: Union[Variable, Global[ProtocolIPv4]] = Field(alias="ompProtocol")
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    prefix_list: Optional[List[IPv4Prefix]] = None


class OmpAdvertiseIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    omp_protocol: Union[Variable, Global[ProtocolIPv6]] = Field(alias="ompProtocol")
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    prefix_list: Optional[List[IPv6Prefix]] = None


class IPv4RouteGatewayNextHop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class IPv4RouteGatewayNextHopWithTracker(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)
    tracker: Union[RefId, Default[None]]


class NextHopContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop: Optional[List[IPv4RouteGatewayNextHop]] = Field(alias="nextHop", default=None)
    next_hop_with_tracker: Optional[List[IPv4RouteGatewayNextHopWithTracker]] = Field(
        alias="nextHopWithTracker", default=None
    )


class IPv6RouteGatewayNextHop(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str]]
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class NextHopIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop: Optional[List[IPv6RouteGatewayNextHop]] = Field(alias="nextHop", default=None)


class NextHopRouteContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop_container: NextHopContainer = Field(alias="nextHopContainer")


class NextHopRouteIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    next_hop_container: NextHopIPv6Container = Field(alias="nextHopContainer")


class Null0(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    null0: Union[Global[bool], Default[bool]] = Default[bool](value=True)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class Null0IPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    null0: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class NATRoute(str, Enum):
    NAT64 = "NAT64"
    NAT66 = "NAT66"


class NAT(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat: Union[Variable, Global[NATRoute]]


class DHCP(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    dhcp: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class StaticRouteVPN(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn: Union[Global[bool], Default[bool]] = Default[bool](value=True)


class NextHopInterfaceRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str], Default[None]] = Default[None](value=None)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class NextHopInterfaceRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    address: Union[Variable, Global[str], Default[None]] = Default[None](value=None)
    distance: Union[Variable, Global[int], Default[int]] = Default[int](value=1)


class IPStaticRouteInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Variable, Global[str]] = Field(alias="interfaceName")
    next_hop: List[NextHopInterfaceRoute] = Field(alias="nextHop")


class IPv6StaticRouteInterface(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_name: Union[Variable, Global[str]] = Field(alias="interfaceName")
    next_hop: List[NextHopInterfaceRouteIPv6] = Field(alias="nextHop")


class InterfaceContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ip_static_route_interface: List[IPStaticRouteInterface] = Field(alias="ipStaticRouteInterface")


class InterfaceIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    ipv6_static_route_interface: List[IPv6StaticRouteInterface] = Field(alias="ipv6StaticRouteInterface")


class InterfaceRouteContainer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_container: InterfaceContainer = Field(alias="interfaceContainer")


class InterfaceRouteIPv6Container(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    interface_container: InterfaceIPv6Container = Field(alias="interfaceContainer")


class StaticRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: RoutePrefix
    one_of_ip_route: Union[NextHopRouteContainer, Null0, DHCP, StaticRouteVPN, InterfaceRouteContainer] = Field(
        alias="oneOfIpRoute"
    )


class StaticRouteIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: RoutePrefix
    one_of_ip_route: Union[NextHopRouteIPv6Container, Null0IPv6, NAT, InterfaceRouteIPv6Container] = Field(
        alias="oneOfIpRoute"
    )


class ServiceType(str, Enum):
    FW = "FW"
    IDS = "IDS"
    IDP = "IDP"
    NETSVC1 = "netsvc1"
    NETSVC2 = "netsvc2"
    NETSVC3 = "netsvc3"
    NETSVC4 = "netsvc4"
    TE = "TE"
    APPQOE = "appqoe"


class Service(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    service_type: Union[Variable, Global[ServiceType]] = Field(alias="serviceType")
    ipv4_addresses: Union[Variable, Global[List[str]]] = Field(alias="ipv4Addresses")
    tracking: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)


class ServiceRouteType(str, Enum):
    SIG = "SIG"
    SSE = "SSE"


class ServiceRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    service: Union[Variable, Global[ServiceRouteType], Default[ServiceRouteType]] = Default[ServiceRouteType](
        value=ServiceRouteType.SIG
    )
    vpn: Global[int] = Global[int](value=0)
    sse_instance: Optional[Union[Variable, Global[str]]] = Field(alias="sseInstance", default=None)


class StaticGreRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    interface: Union[Variable, Global[List[str]], Default[None]]
    vpn: Global[int] = Global[int](value=0)


class StaticIpsecRouteIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    prefix: Prefix
    interface: Union[Variable, Global[List[str]], Default[None]]


class Direction(str, Enum):
    INSIDE = "inside"
    OUTSIDE = "outside"


class NatPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int]] = Field(alias="natPoolName")
    prefix_length: Union[Variable, Global[int]] = Field(alias="prefixLength")
    range_start: Union[Variable, Global[str]] = Field(alias="rangeStart")
    range_end: Union[Variable, Global[str]] = Field(alias="rangeEnd")
    overload: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)
    direction: Union[Variable, Global[Direction]]
    tracking_object: Optional[dict] = Field(alias="trackingObject", default=None)


class NATPortForwardProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"


class NatPortForward(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int], Default[None]] = Field(alias="natPoolName")
    source_port: Union[Variable, Global[int]] = Field(alias="sourcePort")
    translate_port: Union[Variable, Global[int]] = Field(alias="translatePort")
    source_ip: Union[Variable, Global[str]] = Field(alias="sourceIp")
    translated_source_ip: Union[Variable, Global[str]] = Field(alias="TranslatedSourceIp")
    protocol: Union[Variable, Global[NATPortForwardProtocol]]


class StaticNat(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat_pool_name: Union[Variable, Global[int], Default[None]] = Field(alias="natPoolName")
    source_ip: Union[Variable, Global[str]] = Field(alias="sourceIp")
    translated_source_ip: Union[Variable, Global[str]] = Field(alias="TranslatedSourceIP")
    static_nat_direction: Union[Variable, Global[Direction]] = Field(alias="staticNatDirection")
    tracking_object: Optional[dict] = Field(alias="trackingObject", default=None)


class StaticNatSubnet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_ip_subnet: Union[Variable, Global[str]] = Field(alias="sourceIpSubnet")
    translated_source_ip_subnet: Union[Variable, Global[str]] = Field(alias="TranslatedSourceIpSubnet")
    prefix_length: Union[Variable, Global[int]] = Field(alias="prefixLength")
    static_nat_direction: Union[Variable, Global[Direction]] = Field(alias="staticNatDirection")
    tracking_object: Optional[dict] = Field(alias="trackingObject", default=None)


class Nat64v4Pool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    nat64_v4_pool_name: Union[Variable, Global[str]] = Field(alias="nat64V4PoolName")
    nat64_v4_pool_range_start: Union[Variable, Global[str]] = Field(alias="nat64V4PoolRangeStart")
    nat64_v4_pool_range_end: Union[Variable, Global[str]] = Field(alias="nat64V4PoolRangeEnd")
    nat64_v4_pool_overload: Union[Variable, Global[bool], Default[bool]] = Field(
        alias="nat64V4PoolOverload", default=Default[bool](value=False)
    )


class RouteLeakFromGlobalProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"


class RedistributeToServiceProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"


class RouteLeakFromServiceProtocol(str, Enum):
    STATIC = "static"
    CONNECTED = "connected"
    BGP = "bgp"
    OSPF = "ospf"


class RedistributeToGlobalProtocol(str, Enum):
    BGP = "bgp"
    OSPF = "ospf"


class RedistributeToService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Variable, Global[RedistributeToServiceProtocol]]
    policy: Union[Default[None], RefId]


class RedistributeToGlobal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    protocol: Union[Variable, Global[RedistributeToGlobalProtocol]]
    policy: Union[Default[None], RefId]


class RouteLeakFromGlobal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    route_protocol: Union[Variable, Global[RouteLeakFromGlobalProtocol]] = Field(alias="routeProtocol")
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        alias="redistributeToProtocol", default=None
    )


class RouteLeakFromService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    route_protocol: Union[Variable, Global[RouteLeakFromServiceProtocol]] = Field(alias="routeProtocol")
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        alias="redistributeToProtocol", default=None
    )


class RouteLeakBetweenServices(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    source_vpn: Union[Variable, Global[int]] = Field(alias="soureVpn")
    route_protocol: Union[Variable, Global[RouteLeakFromServiceProtocol]] = Field(alias="routeProtocol")
    route_policy: Optional[Union[Default[None], RefId]] = Field(alias="routePolicy", default=None)
    redistribute_to_protocol: Optional[List[RedistributeToService]] = Field(
        alias="redistributeToProtocol", default=None
    )


class RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    rt: Union[Global[str], Variable]


class MplsVpnIPv4RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    import_rt_list: Optional[List[RouteTarget]] = Field(alias="importRtList", default=None)
    export_rt_list: Optional[List[RouteTarget]] = Field(alias="exportRtList", default=None)


class MplsVpnIPv6RouteTarget(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    import_rt_list: Optional[List[RouteTarget]] = Field(alias="importRtList", default=None)
    export_rt_list: Optional[List[RouteTarget]] = Field(alias="exportRtList", default=None)


class LanVpnData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn_id: Union[Variable, Global[int], Default[int]] = Field(alias="vpnId")
    name: Union[Variable, Global[str], Default[None]]
    omp_admin_distance: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        alias="ompAdminDistance", default=None
    )
    omp_admin_distance_ipv6: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        alias="ompAdminDistanceIpv6", default=None
    )
    dns_ipv4: Optional[DnsIPv4] = Field(alias="dnsIpv4", default=None)
    dns_ipv6: Optional[DnsIPv6] = Field(alias="dnsIpv6", default=None)
    new_host_mapping: Optional[List[HostMapping]] = Field(alias="newHostMapping", default=None)
    omp_advertise_ipv4: Optional[List[OmpAdvertiseIPv4]] = Field(alias="ompAdvertiseIpv4", default=None)
    omp_advertise_ipv6: Optional[List[OmpAdvertiseIPv6]] = Field(alias="ompAdvertiseIpv6", default=None)
    ipv4_route: Optional[List[StaticRouteIPv4]] = Field(alias="ipv4Route", default=None)
    ipv6_route: Optional[List[StaticRouteIPv6]] = Field(alias="ipv6Route", default=None)
    service: Optional[List[Service]] = None
    service_route: Optional[List[ServiceRoute]] = Field(alias="serviceRoute", default=None)
    gre_route: Optional[List[StaticGreRouteIPv4]] = Field(alias="greRoute", default=None)
    ipsec_route: Optional[List[StaticIpsecRouteIPv4]] = Field(alias="ipsecRoute", default=None)
    nat_pool: Optional[List[NatPool]] = Field(alias="natPool", default=None)
    nat_port_forwarding: Optional[List[NatPortForward]] = Field(alias="natPortForwarding", default=None)
    static_nat: Optional[List[StaticNat]] = Field(alias="staticNat", default=None)
    static_nat_subnet: Optional[List[StaticNatSubnet]] = Field(alias="staticNatSubnet", default=None)
    nat64_v4_pool: Optional[List[Nat64v4Pool]] = Field(alias="nat64V4Pool", default=None)
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = Field(alias="routeLeakFromGlobal", default=None)
    route_leak_from_service: Optional[List[RouteLeakFromService]] = Field(alias="routeLeakFromService", default=None)
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = Field(
        alias="routeLeakBetweenServices", default=None
    )
    mpls_vpn_ipv4_route_target: Optional[MplsVpnIPv4RouteTarget] = Field(alias="mplsVpnIpv4RouteTarget", default=None)
    mpls_vpn_ipv6_route_target: Optional[MplsVpnIPv6RouteTarget] = Field(alias="mplsVpnIpv6RouteTarget", default=None)
    enable_sdra: Optional[Union[Global[bool], Default[bool]]] = Field(alias="enableSdra", default=None)


class LanVpnCreationPayload(BaseModel):
    name: str
    description: Optional[str] = None
    data: LanVpnData
    metadata: Optional[dict] = None
