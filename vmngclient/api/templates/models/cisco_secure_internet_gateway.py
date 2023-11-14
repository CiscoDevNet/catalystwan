import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic.v1 import BaseModel, Field

from vmngclient.api.templates.feature_template import FeatureTemplate
from vmngclient.utils.pydantic_validators import ConvertIPToStringModel

DEFAULT_TRACKER_THRESHOLD = 300
DEFAULT_TRACKER_INTERVAL = 60
DEFAULT_TRACKER_MULTIPLIER = 3
DEFAULT_INTERFACE_MTU = 1400
DEFAULT_INTERFACE_DPD_INTERVAL = 10
DEFAULT_INTERFACE_DPD_RETRIES = 3
DEFAULT_INTERFACE_IKE_VERSION = 2
DEFAULT_INTERFACE_IKE_REKEY_INTERVAL = 14400
DEFAULT_INTERFACE_IPSEC_REKEY_INTERVAL = 3600
DEFAULT_INTERFACE_IPSEC_REPLAY_WINDOW = 512
DEFAULT_INTERFACE_PAIR_ACTIVE_INTERFACE_WEIGHT = 1
DEFAULT_INTERFACE_PAIR_BACKUP_INTERFACE_WEIGHT = 1
DEFAULT_SIG_VPN_ID = 0
DEFAULT_SERVICE_IDLE_TIME = 0
DEFAULT_SERVICE_REFRESH_TIME = 0


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
    if_name: str = Field(vmanage_key="if-name")
    auto: bool
    shutdown: bool
    description: Optional[str]
    unnumbered: bool = True
    address: Optional[ipaddress.IPv4Interface]
    tunnel_source: ipaddress.IPv4Address = Field(vmanage_key="tunnel-source")
    tunnel_source_interface: str = Field(vmanage_key="tunnel-source-interface")
    tunnel_route_via: str = Field(vmanage_key="tunnel-route-via")
    tunnel_destination: str = Field(vmanage_key="tunnel-destination")
    application: Application = Application.SIG
    tunnel_set: TunnelSet = Field(TunnelSet.SECURE_INTERNET_GATEWAY_UMBRELLA, vmanage_key="tunnel-set")
    tunnel_dc_preference: TunnelDcPreference = Field(TunnelDcPreference.PRIMARY_DC, vmanage_key="tunnel-dc-preference")
    tcp_mss_adjust: Optional[int] = Field(vmanage_key="tcp-mss-adjust")
    mtu: int = DEFAULT_INTERFACE_MTU
    dpd_interval: Optional[int] = Field(DEFAULT_INTERFACE_DPD_INTERVAL, vmanage_key="dpd-interval")
    dpd_retries: Optional[int] = Field(DEFAULT_INTERFACE_DPD_RETRIES, vmanage_key="dpd-retries")
    ike_version: int = Field(DEFAULT_INTERFACE_IKE_VERSION, vmanage_key="ike-version")
    pre_shared_secret: Optional[str] = Field(vmanage_key="pre-shared-secret")
    ike_rekey_interval: Optional[int] = Field(DEFAULT_INTERFACE_IKE_REKEY_INTERVAL, vmanage_key="ike-rekey-interval")
    ike_ciphersuite: Optional[IkeCiphersuite] = Field(IkeCiphersuite.AES256_CBC_SHA1, vmanage_key="ike-ciphersuite")
    ike_group: IkeGroup = Field(IkeGroup.FOURTEEN, vmanage_key="ike-group")
    pre_shared_key_dynamic: bool = Field(True, vmanage_key="pre-shared-key-dynamic")
    ike_local_id: Optional[str] = Field(vmanage_key="ike-local-id")
    ike_remote_id: Optional[str] = Field(vmanage_key="ike-remote-id")
    ipsec_rekey_interval: Optional[int] = Field(
        DEFAULT_INTERFACE_IPSEC_REKEY_INTERVAL, vmanage_key="ipsec-rekey-interval"
    )
    ipsec_replay_window: Optional[int] = Field(DEFAULT_INTERFACE_IPSEC_REPLAY_WINDOW, vmanage_key="ipsec-replay-window")
    ipsec_ciphersuite: IpsecCiphersuite = Field(IpsecCiphersuite.AES256_GCM, vmanage_key="ipsec-ciphersuite")
    perfect_forward_secrecy: PerfectForwardSecrecy = Field(
        PerfectForwardSecrecy.NONE, vmanage_key="perfect-forward-secrecy"
    )
    tracker: Optional[bool]
    track_enable: Optional[bool] = Field(True, vmanage_key="track-enable")

    class Config:
        allow_population_by_field_name = True


class SvcType(str, Enum):
    SIG = "sig"


class InterfacePair(BaseModel):
    active_interface: str = Field(vmanage_key="active-interface")
    active_interface_weight: int = Field(
        DEFAULT_INTERFACE_PAIR_ACTIVE_INTERFACE_WEIGHT, vmanage_key="active-interface-weight"
    )
    backup_interface: Optional[str] = Field("None", vmanage_key="backup-interface")
    backup_interface_weight: int = Field(
        DEFAULT_INTERFACE_PAIR_BACKUP_INTERFACE_WEIGHT, vmanage_key="backup-interface-weight"
    )

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
    svc_type: SvcType = Field(SvcType.SIG, vmanage_key="svc-type")
    interface_pair: List[InterfacePair] = Field(vmanage_key="interface-pair")
    auth_required: Optional[bool] = Field(False, vmanage_key="auth-required")
    xff_forward_enabled: Optional[bool] = Field(False, vmanage_key="xff-forward-enabled")
    ofw_enabled: Optional[bool] = Field(False, vmanage_key="ofw-enabled")
    ips_control: Optional[bool] = Field(False, vmanage_key="ips-control")
    caution_enabled: Optional[bool] = Field(False, vmanage_key="caution-enabled")
    primary_data_center: Optional[str] = Field("Auto", vmanage_key="primary-data-center")
    secondary_data_center: Optional[str] = Field("Auto", vmanage_key="secondary-data-center")
    ip: Optional[bool]
    idle_time: Optional[int] = Field(DEFAULT_SERVICE_IDLE_TIME, vmanage_key="idle-time")
    display_time_unit: Optional[DisplayTimeUnit] = Field(DisplayTimeUnit.MINUTE, vmanage_key="display-time-unit")
    ip_enforced_for_known_browsers: Optional[bool] = Field(False, vmanage_key="ip-enforced-for-known-browsers")
    refresh_time: Optional[int] = Field(DEFAULT_SERVICE_REFRESH_TIME, vmanage_key="refresh-time")
    refresh_time_unit: Optional[RefreshTimeUnit] = Field(RefreshTimeUnit.MINUTE, vmanage_key="refresh-time-unit")
    enabled: Optional[bool]
    block_internet_until_accepted: Optional[bool] = Field(False, vmanage_key="block-internet-until-accepted")
    force_ssl_inspection: Optional[bool] = Field(False, vmanage_key="force-ssl-inspection")
    timeout: Optional[int]
    data_center_primary: Optional[str] = Field("Auto", vmanage_key="data-center-primary")
    data_center_secondary: Optional[str] = Field("Auto", vmanage_key="data-center-secondary")

    class Config:
        allow_population_by_field_name = True


class TrackerType(str, Enum):
    SIG = "SIG"


class Tracker(BaseModel):
    name: str
    endpoint_api_url: str = Field(vmanage_key="endpoint-api-url")
    threshold: Optional[int] = DEFAULT_TRACKER_THRESHOLD
    interval: Optional[int] = DEFAULT_TRACKER_INTERVAL
    multiplier: Optional[int] = DEFAULT_TRACKER_MULTIPLIER
    tracker_type: TrackerType = Field(vmanage_key="tracker-type")

    class Config:
        allow_population_by_field_name = True


class CiscoSecureInternetGatewayModel(FeatureTemplate, ConvertIPToStringModel):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    vpn_id: int = Field(DEFAULT_SIG_VPN_ID, vmanage_key="vpn-id")
    interface: List[Interface]
    service: List[Service]
    tracker_src_ip: ipaddress.IPv4Interface = Field(vmanage_key="tracker-src-ip")
    tracker: Optional[List[Tracker]]

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_secure_internet_gateway"
