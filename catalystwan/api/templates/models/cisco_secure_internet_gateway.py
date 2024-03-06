# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

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


class Interface(FeatureTemplateValidator):
    if_name: str = Field(json_schema_extra={"vmanage_key": "if-name"})
    auto: bool
    shutdown: bool
    description: Optional[str] = None
    unnumbered: bool = True
    address: Optional[ipaddress.IPv4Interface] = None
    tunnel_source: Optional[ipaddress.IPv4Address] = Field(
        default=None, json_schema_extra={"vmanage_key": "tunnel-source"}
    )
    tunnel_source_interface: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "tunnel-source-interface"}
    )
    tunnel_route_via: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "tunnel-route-via"})
    tunnel_destination: str = Field(json_schema_extra={"vmanage_key": "tunnel-destination"})
    application: Application = Application.SIG
    tunnel_set: TunnelSet = Field(
        TunnelSet.SECURE_INTERNET_GATEWAY_UMBRELLA, json_schema_extra={"vmanage_key": "tunnel-set"}
    )
    tunnel_dc_preference: TunnelDcPreference = Field(
        TunnelDcPreference.PRIMARY_DC, json_schema_extra={"vmanage_key": "tunnel-dc-preference"}
    )
    tcp_mss_adjust: Optional[int] = Field(default=None, json_schema_extra={"vmanage_key": "tcp-mss-adjust"})
    mtu: int = DEFAULT_INTERFACE_MTU
    dpd_interval: Optional[int] = Field(
        DEFAULT_INTERFACE_DPD_INTERVAL, json_schema_extra={"vmanage_key": "dpd-interval"}
    )
    dpd_retries: Optional[int] = Field(DEFAULT_INTERFACE_DPD_RETRIES, json_schema_extra={"vmanage_key": "dpd-retries"})
    ike_version: int = Field(DEFAULT_INTERFACE_IKE_VERSION, json_schema_extra={"vmanage_key": "ike-version"})
    pre_shared_secret: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "pre-shared-secret"})
    ike_rekey_interval: Optional[int] = Field(
        DEFAULT_INTERFACE_IKE_REKEY_INTERVAL, json_schema_extra={"vmanage_key": "ike-rekey-interval"}
    )
    ike_ciphersuite: Optional[IkeCiphersuite] = Field(
        IkeCiphersuite.AES256_CBC_SHA1, json_schema_extra={"vmanage_key": "ike-ciphersuite"}
    )
    ike_group: IkeGroup = Field(IkeGroup.FOURTEEN, json_schema_extra={"vmanage_key": "ike-group"})
    pre_shared_key_dynamic: bool = Field(True, json_schema_extra={"vmanage_key": "pre-shared-key-dynamic"})
    ike_local_id: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "ike-local-id"})
    ike_remote_id: Optional[str] = Field(default=None, json_schema_extra={"vmanage_key": "ike-remote-id"})
    ipsec_rekey_interval: Optional[int] = Field(
        DEFAULT_INTERFACE_IPSEC_REKEY_INTERVAL, json_schema_extra={"vmanage_key": "ipsec-rekey-interval"}
    )
    ipsec_replay_window: Optional[int] = Field(
        DEFAULT_INTERFACE_IPSEC_REPLAY_WINDOW, json_schema_extra={"vmanage_key": "ipsec-replay-window"}
    )
    ipsec_ciphersuite: IpsecCiphersuite = Field(
        IpsecCiphersuite.AES256_GCM, json_schema_extra={"vmanage_key": "ipsec-ciphersuite"}
    )
    perfect_forward_secrecy: PerfectForwardSecrecy = Field(
        PerfectForwardSecrecy.NONE, json_schema_extra={"vmanage_key": "perfect-forward-secrecy"}
    )
    tracker: Optional[bool] = None
    track_enable: Optional[bool] = Field(True, json_schema_extra={"vmanage_key": "track-enable"})
    model_config = ConfigDict(populate_by_name=True)


class SvcType(str, Enum):
    SIG = "sig"


class InterfacePair(FeatureTemplateValidator):
    active_interface: str = Field(json_schema_extra={"vmanage_key": "active-interface"})
    active_interface_weight: int = Field(
        DEFAULT_INTERFACE_PAIR_ACTIVE_INTERFACE_WEIGHT, json_schema_extra={"vmanage_key": "active-interface-weight"}
    )
    backup_interface: Optional[str] = Field("None", json_schema_extra={"vmanage_key": "backup-interface"})
    backup_interface_weight: int = Field(
        DEFAULT_INTERFACE_PAIR_BACKUP_INTERFACE_WEIGHT, json_schema_extra={"vmanage_key": "backup-interface-weight"}
    )
    model_config = ConfigDict(populate_by_name=True)


class DisplayTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class RefreshTimeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"


class Service(FeatureTemplateValidator):
    svc_type: SvcType = Field(SvcType.SIG, json_schema_extra={"vmanage_key": "svc-type"})
    interface_pair: List[InterfacePair] = Field(
        json_schema_extra={"data_path": ["ha-pairs"], "vmanage_key": "interface-pair"}
    )
    auth_required: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "auth-required"})
    xff_forward_enabled: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "xff-forward-enabled"})
    ofw_enabled: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "ofw-enabled"})
    ips_control: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "ips-control"})
    caution_enabled: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "caution-enabled"})
    primary_data_center: Optional[str] = Field("Auto", json_schema_extra={"vmanage_key": "primary-data-center"})
    secondary_data_center: Optional[str] = Field("Auto", json_schema_extra={"vmanage_key": "secondary-data-center"})
    ip: Optional[bool] = None
    idle_time: Optional[int] = Field(DEFAULT_SERVICE_IDLE_TIME, json_schema_extra={"vmanage_key": "idle-time"})
    display_time_unit: Optional[DisplayTimeUnit] = Field(
        DisplayTimeUnit.MINUTE, json_schema_extra={"vmanage_key": "display-time-unit"}
    )
    ip_enforced_for_known_browsers: Optional[bool] = Field(
        False, json_schema_extra={"vmanage_key": "ip-enforced-for-known-browsers"}
    )
    refresh_time: Optional[int] = Field(DEFAULT_SERVICE_REFRESH_TIME, json_schema_extra={"vmanage_key": "refresh-time"})
    refresh_time_unit: Optional[RefreshTimeUnit] = Field(
        RefreshTimeUnit.MINUTE, json_schema_extra={"vmanage_key": "refresh-time-unit"}
    )
    enabled: Optional[bool] = None
    block_internet_until_accepted: Optional[bool] = Field(
        False, json_schema_extra={"vmanage_key": "block-internet-until-accepted"}
    )
    force_ssl_inspection: Optional[bool] = Field(False, json_schema_extra={"vmanage_key": "force-ssl-inspection"})
    timeout: Optional[int] = None
    data_center_primary: Optional[str] = Field("Auto", json_schema_extra={"vmanage_key": "data-center-primary"})
    data_center_secondary: Optional[str] = Field("Auto", json_schema_extra={"vmanage_key": "data-center-secondary"})
    model_config = ConfigDict(populate_by_name=True)


class TrackerType(str, Enum):
    SIG = "SIG"


class Tracker(FeatureTemplateValidator):
    name: str
    endpoint_api_url: str = Field(json_schema_extra={"vmanage_key": "endpoint-api-url"})
    threshold: Optional[int] = DEFAULT_TRACKER_THRESHOLD
    interval: Optional[int] = DEFAULT_TRACKER_INTERVAL
    multiplier: Optional[int] = DEFAULT_TRACKER_MULTIPLIER
    tracker_type: TrackerType = Field(json_schema_extra={"vmanage_key": "tracker-type"})
    model_config = ConfigDict(populate_by_name=True)


class CiscoSecureInternetGatewayModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    vpn_id: int = Field(DEFAULT_SIG_VPN_ID, json_schema_extra={"vmanage_key": "vpn-id"})
    interface: List[Interface]
    service: List[Service]
    tracker_src_ip: Optional[ipaddress.IPv4Interface] = Field(
        default=None, json_schema_extra={"vmanage_key": "tracker-src-ip"}
    )
    tracker: Optional[List[Tracker]] = None

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_secure_internet_gateway"
