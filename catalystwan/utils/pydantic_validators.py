import ipaddress
from typing import Any

from pydantic import BaseModel, model_validator


class ConvertBoolToStringModel(BaseModel):
    @model_validator(mode="after")
    def convert_bool_to_string_validator(self):
        for key in self.model_fields.keys():
            value = getattr(self, key)
            if isinstance(value, bool):
                setattr(self, key, str(value).lower())
        return self


class ConvertIPToStringModel(BaseModel):
    @model_validator(mode="after")
    def convert_ip_to_string_validator(self):
        for key in self.model_fields.keys():
            value = getattr(self, key)
            setattr(self, key, convert_ip_to_string(value))
        return self


def convert_ip_to_string(values: Any):
    if isinstance(values, list):
        for index, ip in enumerate(values):
            values[index] = convert_ip_to_string(ip)
    if isinstance(values, ipaddress._BaseAddress):
        values = str(values)
    return values
