"""Assert sane behavior of the unparse function.

For the most part, this is tested by running round-trips on a number of
possible stenotypes by first running parse and then unparse on them."""

import pytest

from stenotype.backend import elements as ste
from stenotype.backend.grammar import parse
from stenotype.backend.steno import unparse

# fmt: off
terminals = [
    ste.Any(),
    ste.Literal(True),
    ste.Literal(False),
    ste.Literal(Ellipsis),
    ste.Literal(None),
    ste.Literal(712412),
    ste.Literal(187512),
    ste.Literal(-1),
    ste.Literal('"foo bar"'),
    ste.Literal('b"foo bar"'),
]
typing = [
    ste.Identifier("foo"),
    ste.Identifier("foo", "bar"),
    ste.Generic(ste.Identifier("foo", "bar"), parameters=(ste.Any(), ste.Any())),
    ste.Generic(ste.Identifier("foo", "bar"), parameters=(ste.Generic(ste.Identifier("baz"), parameters=(ste.Any(), ste.Any())), ste.Any())),
]
specials = [
    ste.Optional(ste.Identifier("foo")),
    ste.Optional(ste.Any()),
    ste.Union(ste.Any(), ste.Identifier("foo")),
    ste.Union(ste.Identifier("foo"), ste.Any(), ste.Identifier("bar")),
]
containers = [
    ste.Tuple(elements=(ste.Any(),)),
    ste.Tuple(elements=(ste.Any(), ste.Dots())),
    ste.Set(ste.Any()),
    ste.Set(ste.Identifier("foo")),
    ste.List(ste.Any()),
    ste.List(ste.Generic(ste.Identifier("foo"), parameters=(ste.Any(),))),
    ste.Dict(ste.Identifier("key"), ste.Identifier("value")),
]

shorthands = [
    ste.Iterable(ste.Identifier("foo")),
    ste.Context(ste.Identifier("foo")),
    ste.Awaitable(ste.Identifier("foo")),
    ste.AsyncIterable(ste.Identifier("foo")),
    ste.AsyncContext(ste.Identifier("foo")),
]
# fmt: on


@pytest.mark.parametrize("element", terminals)
def test_terminals(element):
    assert parse(unparse(element)) == element


@pytest.mark.parametrize("element", typing)
def test_typing(element):
    assert parse(unparse(element)) == element


@pytest.mark.parametrize("element", specials)
def test_specials(element):
    assert parse(unparse(element)) == element


@pytest.mark.parametrize("element", containers)
def test_containers(element):
    assert parse(unparse(element)) == element


@pytest.mark.parametrize("element", shorthands)
def test_shorthands(element):
    assert parse(unparse(element)) == element


def test_unknown():
    with pytest.raises(NotImplementedError, match="cannot be represented") as e:
        unparse(object())
