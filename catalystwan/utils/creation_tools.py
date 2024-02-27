# Copyright 2022 Cisco Systems, Inc. and its affiliates

import datetime as dt
from typing import Any, ClassVar, Dict, Iterable, List, Protocol, Type, TypeVar, runtime_checkable

import attrs  # type: ignore
from attr import Attribute, fields, fields_dict
from dateutil import parser  # type: ignore

T = TypeVar("T")
FIELD_NAME = "__field_name"


@runtime_checkable
class AttrsInstance(Protocol):
    __attrs_attrs__: ClassVar[Any]


def create_dataclass(cls: Type[T], data: Dict[str, Any]) -> T:
    """Deserializes data to convert it into an object.

    Prepares data to create dataclass from json structure.
    If field has given metadata information about FIELD_NAME,
    the data keys are mapped into an field name from given dataclass.
    Then it filters fields which are not given explicitly.
    Creation is handled by attrs module.

    Args:
        cls (type): Dataclass which should be created
        data (dict): A dict to deserialize from

    Returns:
        A dataclass with implemented fields
    """

    def filter_fields(available_fields: Iterable[str], data: Dict[str, Any]) -> Dict[str, Any]:
        return dict(filter(lambda key_value: key_value[0] in available_fields, data.items()))

    data_copy = data.copy()
    for field in fields(cls):  # type: ignore[misc]
        json_field_name = field.metadata.get(FIELD_NAME, None)
        if json_field_name and json_field_name in data_copy:
            data_copy[field.name] = data_copy.pop(json_field_name)
    filtered_data = filter_fields(fields_dict(cls).keys(), data_copy)
    return cls(**filtered_data)


def convert_attributes(cls: type, fields: List[Attribute]) -> List[Attribute]:
    """Automatically add converters to the attributes based on their types.

    Args:
        cls (type): Class right before being converted into an attrs class
        fields (List[Attribute]): List of all Attribute instances that
            will later be set to the __attrs_attrs__

    Returns:
        A modified list of all attr.Attribute instances with proper converters
    """
    results = []
    for field in fields:
        if field.converter is not None:
            results.append(field)
            continue
        if field.type in {dt.datetime, "datetime"}:
            converter = (
                lambda d: parser.parse(d) if isinstance(d, str) else dt.datetime.fromtimestamp(d / 1000)
            )  # type: ignore # noqa: E731
        elif field.type in {str, "str"}:
            converter = lambda x: str(x)  # type: ignore # noqa: E731
        else:
            converter = None
        results.append(field.evolve(converter=converter))  # type: ignore
    return results


def asdict(dataclass: AttrsInstance) -> dict:
    """Serializes attrs dataclass into a python dictionary.

    While serializing dataclass, FIELD_NAME is taken into account.

    Args:
        dataclass (Type[T]): Valid attrs dataclass

    Returns:
        dict: Serialized dict
    """

    json_fields_excluded = attrs.asdict(dataclass, filter=lambda x, _: FIELD_NAME not in x.metadata)
    json_fields = attrs.asdict(dataclass, filter=lambda x, _: FIELD_NAME in x.metadata)

    for field in fields(dataclass.__class__):  # type: ignore[misc]
        field_value = getattr(dataclass, field.name)

        json_field_name = field.metadata.get(FIELD_NAME, None)
        if json_field_name:
            json_fields[json_field_name] = json_fields.pop(field.name)
            if isinstance(field_value, AttrsInstance):
                json_fields[json_field_name] = asdict(field_value)

            if isinstance(field_value, list):  # tuple, List[AttrsInstance], set, frozenset
                if len(field_value) > 0 and isinstance(field_value[0], AttrsInstance):
                    json_fields[json_field_name] = [asdict(_f) for _f in field_value]
        else:
            if isinstance(field_value, AttrsInstance):
                json_fields_excluded[field.name] = asdict(field_value)

    return {**json_fields, **json_fields_excluded}


def flatten_dict(d: Dict) -> Dict:
    """Flattens the given dictionary.

    If it has nested dicts or lists of dicts, inlines them into
    the original dictionary. Other member types are ignored.
    For nested lists only members of type dict is processed.

    Args:
        d (Dict): Dictionary to flatten

    Returns:
        A flattened dictionary
    """
    if not isinstance(d, dict):
        return {}

    def recurse(key, value):
        if isinstance(value, dict):
            for k, v in value.items():
                yield from recurse(k, v)
        elif isinstance(value, list):
            for v in value:
                yield from recurse(None, v)
        elif key is not None:
            yield key, value

    return dict(recurse(None, d))
