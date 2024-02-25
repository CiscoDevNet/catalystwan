# flake8: noqa

# import enum
# from typing import List, Literal, Optional, Union
# from catalystwan.api.configuration_groups.parcel import _ParcelBase, Global, as_global
# from catalystwan.models.configuration.common import AuthType, Priority, Version
# from pydantic import AliasPath, BaseModel, ConfigDict, Field
# from catalystwan.utils.config_migration.converters.recast import (
#     DefaultGlobalBool,
#     DefaultGlobalStr,
# )

# class Server(BaseModel):
#     name: Global[str]
#     vpn: Optional[Union[DefaultGlobalStr, Global[str]]] = None
#     source_interface: Optional[Global[str]] = Field(default=None, serialization_alias="sourceInterface", validation_alias="sourceInterface")
#     priority: Optional[Union[DefaultGlobalLiteral, Global[Priority]]] = "information"
#     enable_tls: Optional[Union[DefaultGlobalBool, Global[bool]]] = Field(default=as_global(False), serialization_alias="tlsEnable", validation_alias="tlsEnable")
#     custom_profile: Optional[Union[DefaultGlobalBool, Global[bool]]] = Field(
#         default=as_global(False), serialization_alias="tlsPropertiesCustomProfile", validation_alias="tlsPropertiesCustomProfile"
#     )
#     profile_properties: Optional[Global[str]] = Field(default=None, serialization_alias="tlsPropertiesProfile", validation_alias="tlsPropertiesProfile")
#     model_config = ConfigDict(populate_by_name=True)


# class Ipv6Server(BaseModel):
#     name: Global[str]
#     vpn: Optional[Union[DefaultGlobalStr, Global[str]]] = None
#     source_interface: Optional[Global[str]] = Field(default=None, serialization_alias="sourceInterface", validation_alias="sourceInterface")
#     priority: Optional[Union[DefaultGlobalLiteral, Global[Priority]]] = "information"
#     enable_tls: Optional[Union[DefaultGlobalBool, Global[bool]]] = Field(default=as_global(False), serialization_alias="tlsEnable", validation_alias="tlsEnable")
#     custom_profile: Optional[Union[DefaultGlobalBool, Global[bool]]] = Field(
#         default=as_global(False), serialization_alias="tlsPropertiesCustomProfile", validation_alias="tlsPropertiesCustomProfile"
#     )
#     profile_properties: Optional[Global[str]] = Field(default=None, serialization_alias="tlsPropertiesProfile", validation_alias="tlsPropertiesProfile")
#     model_config = ConfigDict(populate_by_name=True)

# #
# class File(BaseModel):
#     disk_file_size: Optional[Global[int]] = Field(default=None, serialization_alias="diskFileSize", validation_alias="diskFileSize")
#     disk_file_rotate: Optional[Global[int]] = Field(default=None, serialization_alias="diskFileRotate", validation_alias="diskFileRotate")


# class Disk(BaseModel):
#     disk_enable: Optional[Global[bool]] = Field(default=False, serialization_alias="diskEnable", validation_alias="diskEnable")
#     file: File

# class Logging(_ParcelBase):
#     disk: Optional[Disk] = Field(default=None, validation_alias=AliasPath("data", "disk"))
#     tls_profile: Optional[List[TlsProfile]] = Field(default=None, validation_alias=AliasPath("data", "tlsProfile"))
#     server: Optional[List[Server]] = Field(default=None, validation_alias=AliasPath("data", "server"))
#     ipv6_server: Optional[List[Ipv6Server]] = Field(default=None, validation_alias=AliasPath("data", "ipv6Server"))
