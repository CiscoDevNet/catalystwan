# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception(f"Conflict at {'.'.join(path + [str(key)])}")
        else:
            a[key] = b[key]
    return a


class FlattenedDictValue(BaseModel):
    value: Any
    data_path: List[str]


def flatten_dict(original_dict: Dict[str, Any]) -> Dict[str, List[FlattenedDictValue]]:
    """
    Flattens a dictionary.
    Each key corresponds to a list of FlattenedDictValue, allowing us to handle repeated keys in nesting.
    """

    def get_flattened_dict(
        original_dict: Dict[str, Any],
        flattened_dict: Optional[Dict[str, List[FlattenedDictValue]]] = None,
        path: Optional[List[str]] = None,
    ):
        if flattened_dict is None:
            flattened_dict = {}
        if path is None:
            path = []
        for key, value in original_dict.items():
            if isinstance(value, dict):
                get_flattened_dict(value, flattened_dict, path=path + [key])
            else:
                if key not in flattened_dict:
                    flattened_dict[key] = []
                if isinstance(value, list) and all([isinstance(v, dict) for v in value]):
                    flattened_value = FlattenedDictValue(
                        value=[get_flattened_dict(v, {}) for v in value], data_path=path
                    )
                    flattened_dict[key].append(flattened_value)
                else:
                    flattened_dict[key].append(FlattenedDictValue(value=value, data_path=path))
        return flattened_dict

    flattened_dict: Dict[str, List[FlattenedDictValue]] = {}
    get_flattened_dict(original_dict, flattened_dict)
    return flattened_dict
