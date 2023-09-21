from ipaddress import IPv4Network

from pydantic import BaseModel, Field, validator


class DataPrefixListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    ip_prefix: str = Field(alias="ipPrefix", description="IP4 network prefixes separated by comma")

    @validator("ip_prefix")
    def check_network_prefixes(cls, ip_prefix: str):
        nets = [IPv4Network(net.strip()) for net in ip_prefix.split(",")]
        if len(nets) < 1:
            raise ValueError("No network prefix provided")
        return ip_prefix


class SiteListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    site_id: str = Field(alias="siteId")


class VPNListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    vpn: str = Field(alias="vpn", description="0-65530 range or single number")

    @validator("vpn")
    def check_vpn_range(cls, vpns_str: str):
        vpns = [int(vpn) for vpn in vpns_str.split("-")]
        if len(vpns) > 2:
            raise ValueError("VPN range should consist two integers separated by hyphen")
        for vpn in vpns:
            if vpn < 0 or vpn > 65530:
                raise ValueError("VPN should be in range 0-65530")
        if len(vpns) == 2 and vpns[0] >= vpns[1]:
            raise ValueError("Second VPN in range should be greater than first")
        return vpns_str


class ZoneListEntry(BaseModel):
    class Config:
        allow_population_by_field_name = True

    vpn: str = Field(alias="vpn", description="0-65530 single number")

    @validator("vpn")
    def check_vpn_range(cls, vpn_str: str):
        vpn = int(vpn_str)
        if vpn < 0 or vpn > 65530:
            raise ValueError("VPN should be in range 0-65530")
        return vpn_str
