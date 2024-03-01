from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase, as_default, as_global

Priority = Literal["information", "debugging", "notice", "warn", "error", "critical", "alert", "emergency"]
TlsVersion = Literal["TLSv1.1", "TLSv1.2"]
AuthType = Literal["Server", "Mutual"]
CypherSuite = Literal[
    "rsa-aes-cbc-sha2",
    "rsa-aes-gcm-sha2",
    "ecdhe-rsa-aes-gcm-sha2",
    "aes-128-cbc-sha",
    "aes-256-cbc-sha",
    "dhe-aes-cbc-sha2",
    "dhe-aes-gcm-sha2",
    "ecdhe-ecdsa-aes-gcm-sha2",
    "ecdhe-rsa-aes-cbc-sha2",
]


class TlsProfile(BaseModel):
    profile: Global[str]
    version: Union[Global[TlsVersion], Default[TlsVersion]] = Field(
        default=as_default("TLSv1.1", TlsVersion), serialization_alias="tlsVersion", validation_alias="tlsVersion"
    )
    auth_type: Default[AuthType] = Field(
        default=as_default("Server", AuthType), serialization_alias="authType", validation_alias="authType"
    )  # Value can't be changed in the UI
    ciphersuite_list: Union[Global[List[CypherSuite]], Default[None]] = Field(
        default=Default[None](value=None), serialization_alias="cipherSuiteList", validation_alias="cipherSuiteList"
    )
    model_config = ConfigDict(populate_by_name=True)


class Server(BaseModel):
    name: Global[str]
    vpn: Union[Global[int], Default[int]] = Field(default=as_default(0))
    source_interface: Union[Global[str], Default[None]] = Field(
        default=Default[None](value=None), serialization_alias="sourceInterface", validation_alias="sourceInterface"
    )
    priority: Union[Global[Priority], Default[Priority]] = Field(default=as_default("information", Priority))
    enable_tls: Union[Global[bool], Default[bool]] = Field(
        default=as_default(False), serialization_alias="tlsEnable", validation_alias="tlsEnable"
    )
    custom_profile: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        serialization_alias="tlsPropertiesCustomProfile",
        validation_alias="tlsPropertiesCustomProfile",
    )
    profile_properties: Optional[Global[str]] = Field(
        default=None, serialization_alias="tlsPropertiesProfile", validation_alias="tlsPropertiesProfile"
    )
    model_config = ConfigDict(populate_by_name=True)


class File(BaseModel):
    disk_file_size: Optional[Union[Global[int], Default[int]]] = Field(
        default=as_default(10), serialization_alias="diskFileSize", validation_alias="diskFileSize"
    )
    disk_file_rotate: Optional[Union[Global[int], Default[int]]] = Field(
        default=as_default(10), serialization_alias="diskFileRotate", validation_alias="diskFileRotate"
    )


class Disk(BaseModel):
    disk_enable: Optional[Global[bool]] = Field(
        default=None, serialization_alias="diskEnable", validation_alias="diskEnable"
    )
    file: File = Field(default_factory=File)


class LoggingParcel(_ParcelBase):
    type_: Literal["logging"] = Field(default="logging", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    disk: Disk = Field(default_factory=Disk, validation_alias=AliasPath("data", "disk"))
    tls_profile: Optional[List[TlsProfile]] = Field(default=[], validation_alias=AliasPath("data", "tlsProfile"))
    server: Optional[List[Server]] = Field(default=[], validation_alias=AliasPath("data", "server"))
    ipv6_server: Optional[List[Server]] = Field(default=[], validation_alias=AliasPath("data", "ipv6Server"))

    def set_disk(self, enable: bool, disk_file_size: int = 10, disk_file_rotate: int = 10):
        self.disk.disk_enable = as_global(enable)
        self.disk.file.disk_file_size = as_global(disk_file_size)
        self.disk.file.disk_file_rotate = as_global(disk_file_rotate)

    def add_tls_profile(
        self, profile: str, version: TlsVersion = "TLSv1.1", ciphersuite_list: Optional[List[CypherSuite]] = None
    ):
        if not self.tls_profile:
            self.tls_profile = []
        self.tls_profile.append(
            TlsProfile(
                profile=as_global(profile),
                version=as_global(version, TlsVersion),
                ciphersuite_list=Global[List[CypherSuite]](value=ciphersuite_list)
                if ciphersuite_list
                else Default[None](value=None),
            )
        )

    def add_ipv4_server(
        self,
        name: str,
        vpn: int = 0,
        source_interface: Optional[str] = None,
        priority: Priority = "information",
        enable_tls: bool = False,
        custom_profile: bool = False,
        profile_properties: Optional[str] = None,
    ):
        item = self._create_server_item(
            name, vpn, source_interface, priority, enable_tls, custom_profile, profile_properties
        )
        if not self.server:
            self.server = []
        self.server.append(item)
        return item

    def add_ipv6_server(
        self,
        name: str,
        vpn: int = 0,
        source_interface: Optional[str] = None,
        priority: Priority = "information",
        enable_tls: bool = False,
        custom_profile: bool = False,
        profile_properties: Optional[str] = None,
    ):
        item = self._create_server_item(
            name, vpn, source_interface, priority, enable_tls, custom_profile, profile_properties
        )
        if not self.ipv6_server:
            self.ipv6_server = []
        self.ipv6_server.append(item)
        return item

    def _create_server_item(
        self,
        name: str,
        vpn: int,
        source_interface: Optional[str] = None,
        priority: Priority = "information",
        enable_tls: bool = False,
        custom_profile: bool = False,
        profile_properties: Optional[str] = None,
    ):
        return Server(
            name=as_global(name),
            vpn=as_global(vpn),
            source_interface=as_global(source_interface) if source_interface else Default[None](value=None),
            priority=as_global(priority, Priority),
            enable_tls=as_global(enable_tls),
            custom_profile=as_global(custom_profile) if custom_profile else None,
            profile_properties=as_global(profile_properties) if profile_properties else None,
        )
