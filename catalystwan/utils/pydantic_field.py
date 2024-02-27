# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Any, Optional

from pydantic.fields import FieldInfo


def get_extra_field(field_info: FieldInfo, key: str, default: Optional[Any] = None) -> Any:
    try:
        return field_info.json_schema_extra.get(key, default)  # type: ignore
    except AttributeError:
        return default
