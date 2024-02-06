import ipaddress
from typing import Any

from pydantic.v1 import BaseModel, root_validator


class ConvertBoolToStringModel(BaseModel):
    @root_validator  # type: ignore
    def convert_bool_to_string_validator(cls, values):
        for key, value in values.items():
            if isinstance(value, bool):
                values[key] = str(value).lower()
        return values


class ConvertIPToStringModel(BaseModel):
    @root_validator  # type: ignore
    def convert_ip_to_string_validator(cls, values):
        for key, value in values.items():
            values[key] = convert_ip_to_string(value)
        return values


def convert_ip_to_string(values: Any):
    if isinstance(values, list):
        for index, ip in enumerate(values):
            values[index] = convert_ip_to_string(ip)
    if isinstance(values, ipaddress._BaseAddress):
        values = str(values)
    return values
