from enum import Enum


class SecurityPolicyObjectListType(str, Enum):
    DATA_IP_PREFIX = "security-data-ip-prefix"
    FQDN = "security-fqdn"
    PORT = "security-port"
    LOCAL_APP = "security-localapp"
    LOCAL_DOMAIN = "security-localdomain"
    IPS_SIGNATURE = "security-ipssignature"
    URL_LIST = "security-urllist"
    PROTOCOL_NAME = "security-protocolname"
    GEOLOCATION = "security-geolocation"
    IDENTITY = "security-identity"
    SCALABLE_GROUP_TAG = "security-scalablegrouptag"
    ZONE = "security-zone"


class PolicyObjectListType(str, Enum):
    APP_LIST = "app-list"
    SLA_CLASS = "sla-class"
    AS_PATH = "as-path"
    CLASS = "class"
    DATA_IPV6_PREFIX = "data-ipv6-prefix"
    DATA_PREFIX = "data-prefix"
    EXPANDED_COMMUNITY = "expanded-community"
    EXT_COMMUNITY = "ext-community"
    IPV6_PREFIX = "ipv6-prefix"
    MIRROR = "mirror"
    POLICER = "policer"
    PREFIX = "prefix"
    STANDARD_COMMUNITY = "standard-community"
    VPN_GROUP = "vpn-group"
    APP_PROBE = "app-probe"
    TLOC = "tloc"
    COLOR = "color"
    PREFERRED_COLOR_GROUP = "preferred-color-group"
