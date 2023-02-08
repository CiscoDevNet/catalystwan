from __future__ import annotations

from typing import Any, Generic, Iterable, MutableSequence, TypeVar, overload

T = TypeVar("T")
D = TypeVar("D")


class TypedList(MutableSequence[T], Generic[T]):
    """A list where all elements are of the same data type.

    A homogeneous list provides an efficient and organized way to store data,
    as all elements can be assumed to have the same properties and behaviors.
    Built-in mutable sequence.

    If no argument is given, the constructor creates a new empty list.
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

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    # def single_or_default(self, default: D = None) -> Union[T, D]:  # _type
    #     """

    #     Returns the only element of a sequence, or a default value
    #     if the sequence is empty; this method throws an exception
    #     if there is more than one element in the sequence.
    #     """
    #     if not self.data:
    #         return default

    #     if len(self.data) > 1:
    #         raise InvalidOperationError("The input sequence contains more than one element.")

    #     return self.data[0]

    # def filter(self, **kwargs) -> "TypedList":
    #     annotations = set(kwargs.keys()) & set(self._type.__annotations__.keys())
    #     # annotations = set(kwargs.keys())

    #     return TypedList(list(filter(lambda x: all(getattr(x, a) == kwargs[a] for a in annotations), self.data)))
