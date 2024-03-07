# Copyright 2023 Cisco Systems, Inc. and its affiliates

from __future__ import annotations

from typing import Any, Generic, Iterable, MutableSequence, Type, TypeVar, overload

from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel as BaseModelV1

from catalystwan.exceptions import InvalidOperationError
from catalystwan.utils.creation_tools import AttrsInstance, asdict

T = TypeVar("T")
D = TypeVar("D")


class TypedList(MutableSequence[T], Generic[T]):
    """A list where all elements are of the same data type.

    A homogeneous list provides an efficient and organized way to store data,
    as all elements can be assumed to have the same properties and behaviors.
    Built-in mutable sequence.

    If no argument is provided, the constructor creates a new empty list.
    The argument must be an iterable if specified.

    An implementation is based of pythonic list, instead of creating a new
    Linked List from scratch.
    """

    @overload
    def __init__(self, _type: T) -> None:
        ...

    @overload
    def __init__(self, _type: T, _iterable: Iterable[T], /) -> None:
        ...

    def __init__(self, _type, _iterable=None, /):
        self.data = []
        self._type = _type

        if _iterable is not None:
            for item in _iterable:
                if not isinstance(item, self._type):
                    raise TypeError(f"Expected {self._type.__name__} item type, " f"got {type(item).__name__}.")
                self.data.append(item)

    def __repr__(self) -> str:
        return f"TypedList({self._type.__name__}, {repr(self.data)})"

    def __contains__(self, item: Any) -> bool:
        return item in self.data

    def __len__(self) -> int:
        return len(self.data)

    @overload
    def __getitem__(self, i: int) -> T:
        ...

    @overload
    def __getitem__(self, i: slice) -> TypedList[T]:
        ...

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._type, self.data[i])
        else:
            return self.data[i]

    @overload
    def __setitem__(self, i: int, item: T, /) -> None:
        ...

    @overload
    def __setitem__(self, i: slice, item: Iterable[T], /) -> None:
        ...

    def __setitem__(self, i, item):
        if not isinstance(item, self._type):
            raise TypeError(f"Expected {self._type.__name__} item type, " f"got {type(item).__name__}.")
        self.data[i] = item

    @overload
    def __delitem__(self, i: int, /) -> None:
        ...

    @overload
    def __delitem__(self, i: slice, /) -> None:
        ...

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, __value: Iterable[T]) -> TypedList[T]:
        return TypedList(self._type, self.data + [*__value.__iter__()])

    def __iadd__(self, __value: Iterable[T]) -> TypedList[T]:
        self.data = TypedList(self._type, self.data + [*__value.__iter__()]).data
        return self

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, TypedList):
            if len(self) != len(__o):
                return False
            return all([self.data[i] == __o.data[i] for i in range(len(self))])
        return False

    def append(self, item: T) -> None:
        if not isinstance(item, self._type):
            raise TypeError(f"Expected {self._type.__name__} item type, " f"got {type(item).__name__}.")
        self.data.append(item)

    def insert(self, i: int, item: T) -> None:
        if not isinstance(item, self._type):
            raise TypeError(f"Expected {self._type.__name__} item type, " f"got {type(item).__name__}.")
        self.data.insert(i, item)

    def pop(self, i: int = -1) -> T:
        return self.data.pop(i)

    def remove(self, item: T) -> None:
        self.data.remove(item)

    def clear(self) -> None:
        self.data.clear()

    def count(self, item: T) -> int:
        return self.data.count(item)

    def reverse(self) -> None:
        self.data.reverse()


class DataSequence(TypedList[T], Generic[T]):
    """
    ## Example:

    >>> DataSequence(User, [User(username="User1")])
        DataSequence(User, [
            User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None)
    ])
    """

    @overload
    def __init__(self, _type: Type[T]) -> None:
        ...

    @overload
    def __init__(self, _type: Type[T], _iterable: Iterable[T], /) -> None:
        ...

    def __init__(self, _type, _iterable=None, /):
        if (
            not isinstance(_type, AttrsInstance)
            and not issubclass(_type, BaseModelV1)
            and not issubclass(_type, BaseModelV2)
        ):
            raise TypeError(
                f"Expected {AttrsInstance.__name__} or {BaseModelV1.__name__} item type, got {_type.__name__}."
            )

        super().__init__(_type, _iterable)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, DataSequence):
            if len(self) != len(__o):
                return False
            return all([self.data[i] == __o.data[i] for i in range(len(self))])
        return False

    def __repr__(self) -> str:
        return f"DataSequence({self._type.__name__}, {repr(self.data)})"

    def __str__(self) -> str:
        pretty_message = ""
        for element in self:
            if issubclass(element.__class__, (BaseModelV1, BaseModelV2)):
                pprint = "\n".join(f"    {attr[0]}: {attr[1]}, " for attr in element.dict().items())  # type: ignore
            else:
                pprint = "\n".join(f"    {attr[0]}: {attr[1]}, " for attr in asdict(element).items())  # type: ignore

            pretty_message += f"\n{element.__class__.__name__}(\n" + pprint + "\n)"  # type: ignore
        return pretty_message

    def __add__(self, __value: Iterable[T]) -> DataSequence[T]:
        return DataSequence(self._type, self.data + [*__value.__iter__()])

    def __iadd__(self, __value: Iterable[T]) -> DataSequence[T]:
        self.data = DataSequence(self._type, self.data + [*__value.__iter__()]).data
        return self

    @overload
    def single_or_default(self) -> T:
        ...

    @overload
    def single_or_default(self, default: D) -> D:
        ...

    def single_or_default(self, default=None):
        """Returns the only element of a sequence, or a default value if the sequence is empty.

        ## Example:
        >>> seq = DataSequence(User, [User(username="User1")])
        >>> seq.single_or_default()
        User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None)
        >>> seq = DataSequence(User, [User(username="User1"), User(username="User2")])
        >>> seq.filter(username="User1").single_or_default()
        User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None)

        Args:
            default : The default value to return if the sequence is empty. Defaults to None.

        Raises:
            InvalidOperationError: Raises when there is more than one element in the sequence.

        Returns:
            Union[D, T]: The single element of the input sequence, or default.
        """
        if not self.data:
            return default

        if len(self.data) > 1:
            raise InvalidOperationError("The input sequence contains more than one element.")

        return self.data[0]

    def filter(self, **kwargs) -> DataSequence[T]:
        """Filters a sequence of values based on attributes.

        >>> seq = DataSequence(User, [User(username="User1"), User(username="User2")])
        >>> seq.filter(username="User1")
        DataSequence(User, [
            User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None)
        ])

        Returns:
            DataSequence: Filtered DataSequence.
        """
        annotations = set(kwargs.keys())

        return DataSequence(
            self._type, filter(lambda x: all(getattr(x, a) == kwargs[a] for a in annotations), self.data)
        )

    def first(self) -> T:
        """Returns the first element of a sequence.

        ## Example:
        >>> seq = DataSequence(Device, [Device(hostname="dev-1"), Device(hostname="dev-2"), Device(hostname="dev-3")])
        >>> seq.first()
        Device(hostname="dev-1", personality=Personality.EDGE, ...)

        Raises:
            InvalidOperationError: Raises when there is no elements in the sequence.

        Returns:
            [T]: The single element of the input sequence.
        """

        if len(self.data) < 1:
            raise InvalidOperationError("The input sequence contains no elements.")

        return self.data[0]
