import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertIPToStringModel


class Application(str, Enum):
    SIG = "sig"


class TunnelSet(str, Enum):
    SECURE_INTERNET_GATEWAY_UMBRELLA = "secure-internet-gateway-umbrella"
    SECURE_INTERNET_GATEWAY_ZSCALER = "secure-internet-gateway-zscaler"


class TunnelDcPreference(str, Enum):
    PRIMARY_DC = "primary-dc"
    SECONDARY_DC = "secondary-dc"


class IkeCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA2 = "aes256-cbc-sha2"
    AES128_CBC_SHA1 = "aes128-cbc-sha1"
    AES128_CBC_SHA2 = "aes128-cbc-sha2"


class IkeGroup(str, Enum):
    TWO = "2"
    FOURTEEN = "14"
    FIFTEEN = "15"
    SIXTEEN = "16"


class IpsecCiphersuite(str, Enum):
    AES256_CBC_SHA1 = "aes256-cbc-sha1"
    AES256_CBC_SHA384 = "aes256-cbc-sha384"
    AES256_CBC_SHA256 = "aes256-cbc-sha256"
    AES256_CBC_SHA512 = "aes256-cbc-sha512"
    AES256_GCM = "aes256-gcm"
    NULL_SHA1 = "null-sha1"
    NULL_SHA384 = "null-sha384"
    NULL_SHA256 = "null-sha256"
    NULL_SHA512 = "null-sha512"


class PerfectForwardSecrecy(str, Enum):
    GROUP_2 = "group-2"
    GROUP_14 = "group-14"
    GROUP_15 = "group-15"
    GROUP_16 = "group-16"
    NONE = "none"


class Interface(ConvertIPToStringModel):
    if_name: str = Field(alias="if-name")
    auto: bool
    shutdown: bool
    description: Optional[str]
    unnumbered: bool = True
    address: Optional[ipaddress.IPv4Interface]
    tunnel_source: ipaddress.IPv4Address = Field(alias="tunnel-source")
    tunnel_source_interface: str = Field(alias="tunnel-source-interface")
    tunnel_route_via: str = Field(alias="tunnel-route-via")
    tunnel_destination: str = Field(alias="tunnel-destination")
    application: Application = Application.SIG
    # application: Application = Application.SIG
    tunnel_set: TunnelSet = Field(TunnelSet.SECURE_INTERNET_GATEWAY_UMBRELLA, alias="tunnel-set")
    tunnel_dc_preference: TunnelDcPreference = Field(TunnelDcPreference.PRIMARY_DC, alias="tunnel-dc-preference")
    tcp_mss_adjust: Optional[int] = Field(alias="tcp-mss-adjust")
    mtu: int = 1400
    dpd_interval: Optional[int] = Field(10, alias="dpd-interval")
    dpd_retries: Optional[int] = Field(3, alias="dpd-retries")
    ike_version: int = Field(2, alias="ike-version")
    pre_shared_secret: Optional[str] = Field(alias="pre-shared-secret")
    ike_rekey_interval: Optional[int] = Field(14400, alias="ike-rekey-interval")
    ike_ciphersuite: Optional[IkeCiphersuite] = Field(IkeCiphersuite.AES256_CBC_SHA1, alias="ike-ciphersuite")
    ike_group: IkeGroup = Field(IkeGroup.FOURTEEN, alias="ike-group")
    pre_shared_key_dynamic: bool = Field(True, alias="pre-shared-key-dynamic")
    ike_local_id: Optional[str] = Field(alias="ike-local-id")
    ike_remote_id: Optional[str] = Field(alias="ike-remote-id")
    ipsec_rekey_interval: Optional[int] = Field(3600, alias="ipsec-rekey-interval")
    ipsec_replay_window: Optional[int] = Field(512, alias="ipsec-replay-window")
    ipsec_ciphersuite: IpsecCiphersuite = Field(IpsecCiphersuite.AES256_GCM, alias="ipsec-ciphersuite")
    perfect_forward_secrecy: PerfectForwardSecrecy = Field(PerfectForwardSecrecy.NONE, alias="perfect-forward-secrecy")
    tracker: Optional[bool]
    track_enable: Optional[bool] = Field(True, alias="track-enable")

    class Config:
        allow_population_by_field_name = True


class SvcType(str, Enum):
    SIG = "sig"


class InterfacePair(BaseModel):
    active_interface: str = Field(alias="active-interface")
    active_interface_weight: int = Field(1, alias="active-interface-weight")
    backup_interface: Optional[str] = Field("None", alias="backup-interface")
    backup_interface_weight: int = Field(1, alias="backup-interface-weight")

    class Config:
        allow_population_by_field_name = True


class DisplayTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class RefreshTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class Service(BaseModel):
    svc_type: SvcType = Field(SvcType.SIG, alias="svc-type")
    interface_pair: List[InterfacePair] = Field(alias="interface-pair")
    auth_required: Optional[bool] = Field(False, alias="auth-required")
    xff_forward_enabled: Optional[bool] = Field(False, alias="xff-forward-enabled")
    ofw_enabled: Optional[bool] = Field(False, alias="ofw-enabled")
    ips_control: Optional[bool] = Field(False, alias="ips-control")
    caution_enabled: Optional[bool] = Field(False, alias="caution-enabled")
    primary_data_center: Optional[str] = Field("Auto", alias="primary-data-center")
    secondary_data_center: Optional[str] = Field("Auto", alias="secondary-data-center")
    ip: Optional[bool]
    idle_time: Optional[int] = Field(0, alias="idle-time")
    display_time_unit: Optional[DisplayTimeUnit] = Field(DisplayTimeUnit.MINUTE, alias="display-time-unit")
    ip_enforced_for_known_browsers: Optional[bool] = Field(False, alias="ip-enforced-for-known-browsers")
    refresh_time: Optional[int] = Field(0, alias="refresh-time")
    refresh_time_unit: Optional[RefreshTimeUnit] = Field(RefreshTimeUnit.MINUTE, alias="refresh-time-unit")
    enabled: Optional[bool]
    block_internet_until_accepted: Optional[bool] = Field(False, alias="block-internet-until-accepted")
    force_ssl_inspection: Optional[bool] = Field(False, alias="force-ssl-inspection")
    timeout: Optional[int]
    data_center_primary: Optional[str] = Field("Auto", alias="data-center-primary")
    data_center_secondary: Optional[str] = Field("Auto", alias="data-center-secondary")

    class Config:
        allow_population_by_field_name = True


class TrackerType(str, Enum):
    SIG = "SIG"


class Tracker(BaseModel):
    name: str
    endpoint_api_url: str = Field(alias="endpoint-api-url")
    threshold: Optional[int] = 300
    interval: Optional[int] = 60
    multiplier: Optional[int] = 3
    tracker_type: TrackerType = Field(alias="tracker-type")

    class Config:
        allow_population_by_field_name = True


class CiscoSecureInternetGatewayModel(FeatureTemplate, ConvertIPToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    vpn_id: int = Field(0, alias="vpn-id")
    interface: List[Interface]
    service: List[Service]
    tracker_src_ip: ipaddress.IPv4Interface = Field(alias="tracker-src-ip")
    tracker: Optional[List[Tracker]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_secure_internet_gateway"
