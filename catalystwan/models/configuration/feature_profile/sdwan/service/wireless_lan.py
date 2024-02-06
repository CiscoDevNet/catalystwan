from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable


class CountryCode(str, Enum):
    AE = "AE"
    AR = "AR"
    AT = "AT"
    AU = "AU"
    BA = "BA"
    BB = "BB"
    BE = "BE"
    BG = "BG"
    BH = "BH"
    BN = "BN"
    BO = "BO"
    BR = "BR"
    BY = "BY"
    CA = "BA"
    CA2 = "CA2"
    CH = "CH"
    CL = "CL"
    CM = "CM"
    CN = "CN"
    CO = "CO"
    CR = "CR"
    CY = "CY"
    CZ = "CZ"
    DE = "DE"
    DK = "DK"
    DO = "DO"
    DZ = "DZ"
    EC = "EC"
    EE = "EE"
    EG = "EG"
    ES = "ES"
    FI = "FI"
    FJ = "FJ"
    FR = "FR"
    GB = "GB"
    GH = "GH"
    GI = "GI"
    GR = "GR"
    HK = "HK"
    HR = "HR"
    HU = "HU"
    ID = "ID"
    IE = "IE"
    IL = "IL"
    IO = "IO"
    IN = "IN"
    IQ = "IQ"
    IS = "IS"
    IT = "IT"
    J2 = "J2"
    J4 = "J4"
    JM = "JM"
    JO = "JO"
    KE = "KE"
    KN = "KN"
    KW = "KW"
    KZ = "KZ"
    LB = "LB"
    LI = "LI"
    LK = "LK"
    LT = "LT"
    LU = "LU"
    LV = "LV"
    LY = "LY"
    MA = "MA"
    MC = "MC"
    ME = "ME"
    MK = "MK"
    MN = "MN"
    MO = "MO"
    MT = "MT"
    MX = "MX"
    MY = "MY"
    NL = "NL"
    NO = "NO"
    NZ = "NZ"
    OM = "OM"
    PA = "PA"
    PE = "PE"
    PH = "PH"
    PH2 = "PH2"
    PK = "PK"
    PL = "PL"
    PR = "PR"
    PT = "PT"
    PY = "PY"
    QA = "QA"
    RO = "RO"
    RS = "RS"
    RU = "RU"
    SA = "SA"
    SE = "SE"
    SG = "SG"
    SI = "SI"
    SK = "SK"
    TH = "TH"
    TN = "TN"
    TR = "TR"
    TW = "TW"
    UA = "UA"
    US = "US"
    UY = "UY"
    VE = "VE"
    VN = "VN"
    ZA = "ZA"


class RadioType(str, Enum):
    ALL = "all"
    GHZ_2_4 = "24ghz"
    GHZ_5 = "5ghz"


class QosProfile(str, Enum):
    PLATINUM = "platinum"
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


class SecurityType(str, Enum):
    OPEN = "open"
    PERSONAL = "personal"
    ENTERPRISE = "enterprise"


class MeStaticIpConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    me_ipv4_address: Union[Global[str], Variable]
    netmask: Union[Global[str], Variable]
    default_gateway: Union[Global[str], Variable] = Field(alias="defaultGateway")


class MeIpConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    me_dynamic_ip_enabled: Union[Global[bool], Default[bool]] = Field(
        alias="meDynamicIpEnabled", default=Default[bool](value=True)
    )
    me_static_ip_config: Optional[MeStaticIpConfig] = None


class SecurityConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    security_type: Global[SecurityType] = Field(alias="securityType")
    radius_server_ip: Optional[Union[Global[str], Variable]] = Field(alias="radiusServerIp", default=None)
    radius_server_port: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        alias="radiusServerPort", default=None
    )
    radius_server_secret: Optional[Union[Global[str], Variable]] = Field(alias="radiusServerSecret", default=None)
    passphrase: Optional[Union[Global[str], Variable]] = None


class SSID(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: Global[str]
    admin_state: Union[Global[bool], Variable, Default[bool]] = Field(
        alias="adminState", default=Default[bool](value=True)
    )
    broadcast_ssid: Union[Global[bool], Variable, Default[bool]] = Field(
        alias="broadcastSsid", default=Default[bool](value=True)
    )
    vlan_id: Union[Global[int], Variable] = Field(alias="vlanId")
    radio_type: Union[Global[RadioType], Variable, Default[RadioType]] = Field(
        alias="radioType", default=Default[RadioType](value=RadioType.ALL)
    )
    security_config: SecurityConfig = Field(alias="securityConfig")
    qos_profile: Union[Global[QosProfile], Variable, Default[QosProfile]] = Field(
        alias="qosProfile", default=Default[QosProfile](value=QosProfile.SILVER)
    )


class WirelessLanData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    enable_2_4G: Union[Global[bool], Variable, Default[bool]] = Field(
        alias="enable24G", default=Default[bool](value=True)
    )
    enable_5G: Union[Global[bool], Variable, Default[bool]] = Field(alias="enable5G", default=Default[bool](value=True))
    ssid: List[SSID]
    country: Union[Global[CountryCode], Variable]
    username: Union[Global[str], Variable]
    password: Union[Global[str], Variable]
    me_ip_config: MeIpConfig = Field(alias="meIpConfig", default=MeIpConfig())


class WirelessLanCreationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str
    description: Optional[str] = None
    data: WirelessLanData
    metadata: Optional[dict] = None
