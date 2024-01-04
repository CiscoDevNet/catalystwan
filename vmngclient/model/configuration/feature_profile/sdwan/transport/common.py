from typing import List, Literal, Optional, Union

from pydantic import Field

from vmngclient.api.configuration_groups.parcel import Default, Global, Parcel, Variable

IPV4Address = str
IPv6Address = str


class DNSIPv4(Parcel):
    primary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv4"
    )
    secondary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv4"
    )


class DNSIPv6(Parcel):
    primary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv6"
    )
    secondary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv6"
    )


class HostMapping(Parcel):
    host_name: Union[Global[str], Variable] = Field(alias="hostName")
    list_of_ips: Union[Global[list[str]], Variable] = Field(alias="listOfIp")


class NextHop(Parcel):
    address: Union[Global[str], Variable] = Field()
    distance: Union[Default[int], Global[int], Default[int]] = Field(
        default=Default[int](value=1)
    )


class IPv4Prefix(Parcel):
    ip_address: Union[Global[IPV4Address], Variable] = Field()
    subnet_mask: Union[Global[str], Variable] = Field()


class WANIPv4StaticRoute(Parcel):
    prefix: IPv4Prefix = Field()
    gateway: Global[Literal["nextHop", "null0", "dhcp"]] = Field(
        default=Global(value="nextHop"), alias="gateway"
    )
    next_hops: Optional[List[NextHop]] = Field(default_factory=list, alias="nextHop")
    distance: Optional[Global[int]] = Field(default=None, alias="distance")

    def set_to_next_hop(
        self,
        prefix: Optional[Global[str]] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global[Literal["nextHop", "null0", "dhcp"]](value="nextHop")
        self.next_hops = next_hops or []
        self.distance = None

    def set_to_null0(
        self,
        prefix: Optional[IPv4Prefix] = None,
        distance: Union[Global[int], int] = 1,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="null0")
        self.next_hops = None
        if isinstance(distance, int):
            self.distance = Global(value=distance)
        else:
            self.distance = distance

    def set_to_dhcp(
        self,
        prefix: Optional[IPv4Prefix] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="dhcp")
        self.next_hops = None
        self.distance = None


class NextHopContainer(Parcel):
    next_hop: list[NextHop] = Field(default=[], alias="nextHop")


class Ipv6StaticRouteNull0(Parcel):
    null0: Union[Default[bool], Global[bool]] = Field(default=Default[bool](value=True))


class IPv6StaticRouteNextHop(Parcel):
    next_hop_container: Optional[NextHopContainer] = Field(default=None)


class IPv6StaticRouteNAT(Parcel):
    nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]] = Field()


class WANIPv6StaticRoute(Parcel):
    prefix: Global[IPv6Address] = Field()
    gateway: Union[
        Ipv6StaticRouteNull0, IPv6StaticRouteNextHop, IPv6StaticRouteNAT
    ] = Field(alias="oneOfIpRoute")

    def set_to_next_hop(
        self,
        prefix: Optional[IPv6Address] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = IPv6StaticRouteNextHop(
            next_hop_container=NextHopContainer(next_hops=next_hops)
        )

    def set_to_null0(
        self,
        prefix: Optional[IPv6Address] = None,
        enabled: Union[Default[bool], Global[bool]] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        if enabled is None:
            enabled = Default[bool](value=True)
        self.gateway = Ipv6StaticRouteNull0(null0=enabled)

    def set_to_nat(
        self,
        prefix: Optional[IPv6Address],
        nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]],
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = IPv6StaticRouteNAT(nat=nat)
