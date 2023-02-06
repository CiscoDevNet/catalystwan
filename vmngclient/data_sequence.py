from collections import UserList
from typing import Generic, Iterable, MutableSequence, Optional, TypeVar, Union, overload

from vmngclient.exceptions import InvalidOperationError

T = TypeVar("T")
D = TypeVar("D")


class TypedList(MutableSequence[T], Generic[T]):
    """A list where all elements are of the same data type.

    A homogeneous list provides an efficient and organized way to store data,
    as all elements can be assumed to have the same properties and behaviors.
    Built-in mutable sequence.

    If no argument is given, the constructor creates a new empty list.
    The argument must be an iterable if specified.
    """

    @overload
    def __init__(self, _type: T) -> None:
        ...

    @overload
    def __init__(self, _type: T, iterable: Iterable[T], /) -> None:
        ...

    def __init__(self, _type: T, iterable: Optional[Iterable[T]] = None, /) -> None:  # type: ignore
        self.data = []
        self._type = _type

        if iterable is not None:
            for item in iterable:
                if not isinstance(item, self._type):  # type: ignore
                    raise TypeError(f"Expected {self._type.__name__} item type, " \
                        f"got {type(item).__name__}.") # type : ignore
                self.data.append(item)

    # TODO
    def __repr__(self):
        return repr(self.data)

    def __lt__(self, other):
        return self.data < self.__cast(other)

    def __le__(self, other):
        return self.data <= self.__cast(other)

    def __eq__(self, other):
        return self.data == self.__cast(other)

    def __gt__(self, other):
        return self.data > self.__cast(other)

    def __ge__(self, other):
        return self.data >= self.__cast(other)

    def __cast(self, other):
        return other.data if isinstance(other, UserList) else other

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other):
        if isinstance(other, UserList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    def __radd__(self, other):
        if isinstance(other, UserList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        return self.__class__(list(other) + self.data)

    def __iadd__(self, other):
        if isinstance(other, UserList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        return self

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    def append(self, item):
        self.data.append(item)

    def insert(self, i, item):
        self.data.insert(i, item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)

    def single_or_default(self, default: D = None) -> Union[T, D]:  # _type
        """

        Returns the only element of a sequence, or a default value
        if the sequence is empty; this method throws an exception
        if there is more than one element in the sequence.
        """
        if not self.data:
            return default

        if len(self.data) > 1:
            raise InvalidOperationError("The input sequence contains more than one element.")

        return self.data[0]

    def filter(self, **kwargs) -> "TypedList":
        annotations = set(kwargs.keys()) & set(self._type.__annotations__.keys())
        # annotations = set(kwargs.keys())

        return TypedList(list(filter(lambda x: all(getattr(x, a) == kwargs[a] for a in annotations), self.data)))
