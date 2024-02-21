from ipaddress import AddressValueError, IPv4Address, IPv6Address
from typing import List, Union

from pydantic import BeforeValidator
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import Global, Variable
from catalystwan.models.common import TLOCColor


def recast_as_global_bool(global_: Global[str]):
    value = global_.value
    if value == "true":
        return Global[bool](value=True)
    elif value == "false":
        return Global[bool](value=False)


def recast_as_global_list_str(global_: Global[str]):
    value = global_.value
    return Global[List[str]](value=[v for v in value.split(",")])


def recast_as_global_ipv6_ipv4(global_: Global[str]):
    value = global_.value
    try:
        return Global[IPv4Address](value=IPv4Address(value))
    except AddressValueError:
        pass
    try:
        return Global[IPv6Address](value=IPv6Address(value))
    except AddressValueError:
        pass
    return value


def recast_as_global_str(global_: Global[int]):
    value = global_.value
    return Global[str](value=str(value))


def recast_as_variable(global_: Global[str]):
    value = global_.value
    return Variable(value=value)


def recast_as_global_color_literal(global_: Global[str]):
    value = global_.value
    return Global[TLOCColor](value=value)  # type: ignore[arg-type]


DefaultGlobalBool = Annotated[Global[bool], BeforeValidator(recast_as_global_bool)]
DefaultGlobalList = Annotated[Global[List[str]], BeforeValidator(recast_as_global_list_str)]
DefaultGlobalIPAddress = Annotated[
    Union[Global[IPv4Address], Global[IPv6Address]], BeforeValidator(recast_as_global_ipv6_ipv4)
]
DefaultGlobalStr = Annotated[Global[str], BeforeValidator(recast_as_global_str)]
DefaultVariableStr = Annotated[Variable, BeforeValidator(recast_as_variable)]
DefaultGlobalColorLiteral = Annotated[Global[TLOCColor], BeforeValidator(recast_as_global_color_literal)]
