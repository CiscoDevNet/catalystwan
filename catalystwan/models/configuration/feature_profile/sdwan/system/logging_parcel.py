from typing import List, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase, as_global
from catalystwan.models.configuration.feature_profile.sdwan.system.literals import AuthType, Priority, Version
from catalystwan.utils.pydantic_validators import ConvertBoolToStringModel


class TlsProfile(ConvertBoolToStringModel):
    profile: str
    version: Optional[Version] = Field(default="TLSv1.1", json_schema_extra={"data_path": ["tls-version"]})
    auth_type: AuthType = Field(json_schema_extra={"vmanage_key": "auth-type"})
    ciphersuite_list: Optional[List] = Field(
        default=None, json_schema_extra={"data_path": ["ciphersuite"], "vmanage_key": "ciphersuite-list"}
    )
    model_config = ConfigDict(populate_by_name=True)


class Server(BaseModel):
    name: Global[str]
    vpn: Optional[Global[str]] = None
    source_interface: Optional[Global[str]] = Field(
        default=None, serialization_alias="sourceInterface", validation_alias="sourceInterface"
    )
    priority: Optional[Global[Priority]] = Field(default="information")
    enable_tls: Optional[Global[bool]] = Field(
        default=as_global(False), serialization_alias="tlsEnable", validation_alias="tlsEnable"
    )
    custom_profile: Optional[Global[bool]] = Field(
        default=as_global(False),
        serialization_alias="tlsPropertiesCustomProfile",
        validation_alias="tlsPropertiesCustomProfile",
    )
    profile_properties: Optional[Global[str]] = Field(
        default=None, serialization_alias="tlsPropertiesProfile", validation_alias="tlsPropertiesProfile"
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Server(BaseModel):
    name: Global[str]
    vpn: Optional[Global[str]] = None
    source_interface: Optional[Global[str]] = Field(
        default=None, serialization_alias="sourceInterface", validation_alias="sourceInterface"
    )
    priority: Optional[Global[Priority]] = Field(default="information")
    enable_tls: Optional[Global[bool]] = Field(
        default=as_global(False), serialization_alias="tlsEnable", validation_alias="tlsEnable"
    )
    custom_profile: Optional[Global[bool]] = Field(
        default=as_global(False),
        serialization_alias="tlsPropertiesCustomProfile",
        validation_alias="tlsPropertiesCustomProfile",
    )
    profile_properties: Optional[Global[str]] = Field(
        default=None, serialization_alias="tlsPropertiesProfile", validation_alias="tlsPropertiesProfile"
    )
    model_config = ConfigDict(populate_by_name=True)


class File(BaseModel):
    disk_file_size: Optional[Union[Global[int], Default[int]]] = Field(
        default=Default[int](value=10), serialization_alias="diskFileSize", validation_alias="diskFileSize"
    )
    disk_file_rotate: Optional[Union[Global[int], Default[int]]] = Field(
        default=Default[int](value=10), serialization_alias="diskFileRotate", validation_alias="diskFileRotate"
    )


class Disk(BaseModel):
    disk_enable: Optional[Global[bool]] = Field(
        default=False, serialization_alias="diskEnable", validation_alias="diskEnable"
    )
    file: File


class LoggingParcel(_ParcelBase):
    disk: Optional[Disk] = Field(default=None, validation_alias=AliasPath("data", "disk"))
    tls_profile: Optional[List[TlsProfile]] = Field(default=[], validation_alias=AliasPath("data", "tlsProfile"))
    server: Optional[List[Server]] = Field(default=[], validation_alias=AliasPath("data", "server"))
    ipv6_server: Optional[List[Ipv6Server]] = Field(default=[], validation_alias=AliasPath("data", "ipv6Server"))
