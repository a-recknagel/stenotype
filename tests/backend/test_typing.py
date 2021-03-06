"""Test normalization of steno objects to typing-types."""

import pytest

from stenotype.backend import elements as ste
from stenotype.backend.steno import unparse
from stenotype.backend.typing import normalize

# fmt: off
terminals = [
    ("typing.Any", ste.Any()),
    ("typing.Literal[True]", ste.Literal(True)),
    ("typing.Literal[False]", ste.Literal(False)),
    ("typing.Literal[Ellipsis]", ste.Literal(Ellipsis)),
    ("typing.Literal[None]", ste.Literal(None)),
    ("typing.Literal[712412]", ste.Literal(712412)),
    ("typing.Literal[187512]", ste.Literal(187512)),
    ("typing.Literal[-1]", ste.Literal(-1)),
    ('typing.Literal["foo bar"]', ste.Literal('"foo bar"')),
    ('typing.Literal[b"foo bar"]', ste.Literal('b"foo bar"')),
]
typings = [
    ("foo", ste.Identifier("foo")),
    ("foo.bar", ste.Identifier("foo", "bar")),
    ("foo.bar[typing.Any, typing.Any]",
     ste.Generic(ste.Identifier("foo", "bar"), parameters=(ste.Any(), ste.Any()))),
    ("foo.bar[baz[typing.Any, typing.Any], typing.Any]",
     ste.Generic(ste.Identifier("foo", "bar"), parameters=(ste.Generic(ste.Identifier("baz"), parameters=(ste.Any(), ste.Any())), ste.Any()))),
]
specials = [
    ("typing.Optional[foo]", ste.Optional(ste.Identifier("foo"))),
    ("typing.Optional[typing.Any]", ste.Optional(ste.Any())),
    ("typing.Union[typing.Any, foo]", ste.Union(ste.Any(), ste.Identifier("foo"))),
    ("typing.Union[foo, typing.Any, bar]", ste.Union(ste.Identifier("foo"), ste.Any(), ste.Identifier("bar"))),
]
containers = [
    ("typing.Tuple[typing.Any]", ste.Tuple(elements=(ste.Any(),))),
    ("typing.Tuple[typing.Any, ...]", ste.Tuple(elements=(ste.Any(), ste.Dots()))),
    ("typing.Set[typing.Any]", ste.Set(ste.Any())),
    ("typing.Set[foo]", ste.Set(ste.Identifier("foo"))),
    ("typing.List[typing.Any]", ste.List(ste.Any())),
    ("typing.List[foo[typing.Any]]", ste.List(ste.Generic(ste.Identifier("foo"), parameters=(ste.Any(),)))),
    ("typing.Dict[key, value]", ste.Dict(ste.Identifier("key"), ste.Identifier("value"))),
]
shorthands = [
    ("typing.Iterable[foo]", ste.Iterable(ste.Identifier("foo"))),
    ("typing.ContextManager[foo]", ste.Context(ste.Identifier("foo"))),
    ("typing.Awaitable[foo]", ste.Awaitable(ste.Identifier("foo"))),
    ("typing.AsyncIterable[foo]", ste.AsyncIterable(ste.Identifier("foo"))),
    ("typing.AsyncContextManager[foo]", ste.AsyncContext(ste.Identifier("foo"))),
]
callables = [
    ("typing.Callable[..., R]", ste.Callable(ste.Dots(), ste.Identifier('R'))),
    ("typing.Callable[[A], R]", ste.Callable(
        (ste.Identifier('A'),), ste.Identifier('R'),
    )),
    ("typing.Callable[[A, B], R]", ste.Callable(
        (ste.Identifier('A'), ste.Identifier('B')), ste.Identifier('R'),
    )),
]
callable_signatures = [
    ("typing.Callable[..., R]", ste.Signature(
        positional=(), mixed=(), args=ste.Parameter(None, ste.Any()), keywords=(), kwargs=None, returns=ste.Identifier('R'))
     ),
    ("typing.Callable[[A, B, C], R]", ste.Signature(
        positional=(ste.Parameter(None, ste.Identifier('A')), ste.Parameter(None, ste.Identifier('B')), ste.Parameter(None, ste.Identifier('C'))),
        mixed=(),
        args=None, keywords=(), kwargs=None, returns=ste.Identifier('R'))
     ),
    ("typing.Callable[[A, B, C], R]", ste.Signature(
        positional=(),
        mixed=(ste.Parameter(None, ste.Identifier('A')), ste.Parameter(None, ste.Identifier('B')), ste.Parameter(None, ste.Identifier('C'))),
        args=None, keywords=(), kwargs=None, returns=ste.Identifier('R'))
     ),
    ("typing.Callable[[A, B, C], R]", ste.Signature(
        positional=(ste.Parameter(None, ste.Identifier('A')), ste.Parameter(None, ste.Identifier('B'))),
        mixed=(ste.Parameter(None, ste.Identifier('C')),),
        args=None, keywords=(), kwargs=None, returns=ste.Identifier('R'))
     ),
]
protocol_signatures = [
    ste.Signature(
        positional=(ste.Parameter(None, ste.Identifier('A')), ste.Parameter('b', ste.Identifier('B'))),
        mixed=(),
        args=None, keywords=(), kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(ste.Parameter(None, ste.Identifier('A')),),
        mixed=(ste.Parameter('b', ste.Identifier('B')),),
        args=None, keywords=(), kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(ste.Parameter(None, ste.Identifier('A')),),
        mixed=(),
        args=ste.Parameter(None, ste.Any()), keywords=(), kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(),
        mixed=(ste.Parameter(None, ste.Identifier('A')),),
        args=ste.Parameter(None, ste.Any()), keywords=(), kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(),
        mixed=(),
        args=ste.Parameter(None, ste.Identifier('A')), keywords=(), kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(),
        mixed=(),
        args=ste.Parameter(None, ste.Any()),
        keywords=(ste.Parameter('a', ste.Identifier('A')),),
        kwargs=None, returns=ste.Identifier('R'),
    ),
    ste.Signature(
        positional=(),
        mixed=(),
        args=ste.Parameter(None, ste.Any()), keywords=(),
        kwargs=ste.Parameter(None, ste.Any()), returns=ste.Identifier('R'),
    ),
]
# fmt: on


@pytest.mark.parametrize("typing_type, element", terminals)
def test_terminals(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", typings)
def test_typings(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", specials)
def test_specials(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", containers)
def test_containers(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", shorthands)
def test_shorthands(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", callables)
def test_callables(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("typing_type, element", callable_signatures)
def test_callable_signatures(typing_type, element):
    assert typing_type == unparse(normalize(element))


@pytest.mark.parametrize("element", protocol_signatures)
def test_protocol_signatures(element):
    with pytest.raises(ValueError):
        normalize(element)


def test_unknown():
    with pytest.raises(NotImplementedError, match="cannot be represented"):
        normalize(object)
