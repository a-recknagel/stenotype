"""
Steno Type Elements

Representations of the fundamental :py:mod:`stenotype` building blocks.
Each element holds the relevant information for both a :py:mod:`stenotype` and
:py:mod:`typing` conversion.

Note that all elements are represented as values, not types:
A :py:class:`Steno` encodes :py:mod:`stenotype` syntax/code,
not any concrete types.
For example, ``Identifier('typing', 'List')`` is not the type :py:class:`typing.List`
but represents the name ``typing.List``.
"""
from typing import NamedTuple, Tuple as TupleT, Union as UnionT


class Dots:
    """A literal ``...`` placeholder"""

    __slots__ = ()

    def __eq__(self, other):
        return True if type(other) is Dots else NotImplemented

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class Identifier(TupleT[str, ...]):
    """A qualified name, such as ``typing.Tuple``"""

    def __new__(cls, *elements: str):
        return super().__new__(cls, elements)

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self))})'


class Generic(NamedTuple):
    """A generic type, such as ``typing.List[int]``"""

    base: Identifier
    parameters: TupleT[UnionT["Steno", Dots], ...]


class Any:
    """Any type as ``_``, same as :py:class:`typing.Any`"""

    __slots__ = ()

    def __eq__(self, other):
        return True if type(other) is Any else NotImplemented

    def __repr__(self):
        return f"Any()"


class Optional(NamedTuple):
    """Optional type as ``?base``, equivalent to ``typing.Optional[base]``"""

    base: "Steno"


class Union(TupleT["Steno"]):
    """Union of types as ``A or B``, equivalent to ``typing.Union[A, B]``"""

    def __new__(cls, *elements: "Steno"):
        return super().__new__(cls, elements)

    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self))})'


class Tuple(NamedTuple):
    """Typed tuple as ``(A, B, ...)``, equivalent to ``typing.Tuple[A, B, ...]``"""

    elements: TupleT[UnionT["Steno", Dots], ...]


class List(NamedTuple):
    """Typed list as ``[values]``, equivalent to ``typing.List[values]``"""

    values: "Steno"


class Dict(NamedTuple):
    """Typed dict as ``{keys: values}``, equivalent to ``typing.Dict[keys, values]``"""

    keys: "Steno"
    values: "Steno"


class Set(NamedTuple):
    """Typed dict as ``{values}``, equivalent to ``typing.Set[values]``"""

    values: "Steno"


class Literal(NamedTuple):
    """Literal value, not a type"""

    value: UnionT[None, bool, int, str, bytes, "ellipsis"]


class Iterable(NamedTuple):
    """Typed iterable as ``iter base``, equivalent to ``typing.Iterable[base]``"""

    base: "Steno"


class Context(NamedTuple):
    """Typed context manager as ``with base``"""

    base: "Steno"


class Awaitable(NamedTuple):
    """Typed awaitable as ``await base``, equivalent to ``typing.Awaitable[base]``"""

    base: "Steno"


class AsyncIterable(NamedTuple):
    """Typed async iterable as ``async iter base``"""

    base: "Steno"


class AsyncContext(NamedTuple):
    """Typed async context manager as ``async with base``"""

    base: "Steno"


Steno = UnionT[
    Identifier,
    Generic,
    Any,
    Optional,
    List,
    Dict,
    Set,
    Literal,
    Iterable,
    Context,
    Awaitable,
    AsyncIterable,
    AsyncContext,
]
