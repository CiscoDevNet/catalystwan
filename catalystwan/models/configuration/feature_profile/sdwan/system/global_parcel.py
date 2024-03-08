from __future__ import annotations

from typing import Literal, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default


class ServicesIp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    http_server: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpHttpServer",
        validation_alias="servicesGlobalServicesIpHttpServer",
    )
    https_server: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpHttpsServer",
        validation_alias="servicesGlobalServicesIpHttpsServer",
    )
    ftp_passive: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpFtpPassive",
        validation_alias="servicesGlobalServicesIpFtpPassive",
    )
    domain_lookup: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpDomainLookup",
        validation_alias="servicesGlobalServicesIpDomainLookup",
    )
    arp_proxy: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpArpProxy",
        validation_alias="servicesGlobalServicesIpArpProxy",
    )
    rcmd: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpRcmd",
        validation_alias="servicesGlobalServicesIpRcmd",
    )
    line_vty: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="servicesGlobalServicesIpLineVty",
        validation_alias="servicesGlobalServicesIpLineVty",
    )
    cdp: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="servicesGlobalServicesIpCdp",
        validation_alias="servicesGlobalServicesIpCdp",
    )
    lldp: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="servicesGlobalServicesIpLldp",
        validation_alias="servicesGlobalServicesIpLldp",
    )
    source_intrf: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="servicesGlobalServicesIpSourceIntrf",
        validation_alias="servicesGlobalServicesIpSourceIntrf",
    )
    tcp_keepalives_in: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="globalOtherSettingsTcpKeepalivesIn",
        validation_alias="globalOtherSettingsTcpKeepalivesIn",
    )
    keepalives_out: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="globalOtherSettingsTcpKeepalivesOut",
        validation_alias="globalOtherSettingsTcpKeepalivesOut",
    )
    small_servers: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="globalOtherSettingsTcpSmallServers",
        validation_alias="globalOtherSettingsTcpSmallServers",
    )
    udp_small_servers: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="globalOtherSettingsUdpSmallServers",
        validation_alias="globalOtherSettingsUdpSmallServers",
    )
    console_logging: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="globalOtherSettingsConsoleLogging",
        validation_alias="globalOtherSettingsConsoleLogging",
    )
    ip_source_route: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="globalOtherSettingsIPSourceRoute",
        validation_alias="globalOtherSettingsIPSourceRoute",
    )
    vty_line_logging: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="globalOtherSettingsVtyLineLogging",
        validation_alias="globalOtherSettingsVtyLineLogging",
    )
    snmp_ifindex_persist: (Union[Variable, Global[bool], Default[bool]]) = Field(
        default=as_default(True),
        serialization_alias="globalOtherSettingsSnmpIfindexPersist",
        validation_alias="globalOtherSettingsSnmpIfindexPersist",
    )
    ignore_bootp: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True),
        serialization_alias="globalOtherSettingsIgnoreBootp",
        validation_alias="globalOtherSettingsIgnoreBootp",
    )
    nat64_udp_timeout: Union[Variable, Global[bool], Default[int]] = Field(
        default=as_default(300),
        serialization_alias="globalSettingsNat64UdpTimeout",
        validation_alias="globalSettingsNat64UdpTimeout",
    )
    nat64_tcp_timeout: Union[Variable, Global[bool], Default[int]] = Field(
        default=as_default(3600),
        serialization_alias="globalSettingsNat64TcpTimeout",
        validation_alias="globalSettingsNat64TcpTimeout",
    )
    http_authentication: Union[Variable, Global[bool], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="globalSettingsHttpAuthentication",
        validation_alias="globalSettingsHttpAuthentication",
    )
    ssh_version: Union[Variable, Global[bool], Default[None]] = Field(
        default=Default[None](value=None),
        serialization_alias="globalSettingsSSHVersion",
        validation_alias="globalSettingsSSHVersion",
    )


class ServicesGlobal(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    services_ip: ServicesIp = Field(default_factory=ServicesIp)


class GlobalParcel(_ParcelBase):
    type_: Literal["global"] = Field(default="global", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    services_global: ServicesGlobal = Field(
        default_factory=ServicesGlobal, validation_alias=AliasPath("data", "services_global")
    )
