# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class User(FeatureTemplateValidator):
    name: str
    password: Optional[str] = None
    secret: Optional[str] = None
    privilege: Optional[str] = None
    pubkey_chain: List[str] = Field(default=[], json_schema_extra={"vmanage_key": "pubkey-chain", "vip_type": "ignore"})


class RadiusServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    address: str
    auth_port: int = Field(default=1812, json_schema_extra={"vmanage_key": "auth-port"})
    acct_port: int = Field(default=1813, json_schema_extra={"vmanage_key": "acct-port"})
    timeout: int = Field(default=5)
    retransmit: int = 3
    key: str
    secret_key: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "secret-key"})
    key_enum: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "key-enum"})
    key_type: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "key-type"})


class RadiusGroup(FeatureTemplateValidator):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_name: str = Field(json_schema_extra={"vmanage_key": "group-name"})
    vpn: Optional[int] = None
    source_interface: Optional[str] = Field(json_schema_extra={"vmanage_key": "source-interface"})
    server: List[RadiusServer] = []


class DomainStripping(str, Enum):
    YES = "yes"
    NO = "no"
    RIGHT_TO_LEFT = "right-to-left"


class TacacsServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    address: str
    port: int = 49
    timeout: int = Field(default=5)
    key: str
    secret_key: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "secret-key"})
    key_enum: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "key-enum"})


class TacacsGroup(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    group_name: str = Field(json_schema_extra={"vmanage_key": "group-name"})
    vpn: int = 0
    source_interface: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "source-interface"})
    server: List[TacacsServer] = []


class CiscoAAAModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    user: Optional[List[User]] = None
    authentication_group: bool = Field(default=False, json_schema_extra={"vmanage_key": "authentication_group"})
    accounting_group: bool = True
    radius: Optional[List[RadiusGroup]] = None
    domain_stripping: Optional[DomainStripping] = Field(
        default=None, json_schema_extra={"vmanage_key": "domain-stripping"}
    )
    port: int = 1700
    tacacs: Optional[List[TacacsGroup]] = None
    server_auth_order: str = Field(default="local", json_schema_extra={"vmanage_key": "server-auth-order"})

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cedge_aaa"
