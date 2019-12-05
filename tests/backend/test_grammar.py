import pytest

from stenotype.backend import elements as ste
from stenotype.backend.grammar import parse

# fmt: off
literals = [True, False, Ellipsis, None, 1234, 1337, -1, '"foo bar"', 'b"foo bar"']
typing = [
    ("str", ste.Identifier("str")),
    ("Vector", ste.Identifier("Vector")),
    ("typing.List", ste.Identifier("typing", "List")),
    ("Dict[str, str]", ste.Generic(
        base=ste.Identifier("Dict"),
        parameters=(ste.Identifier("str"), ste.Identifier("str")))),
    ("Tuple[Address, ConnectionOptions]", ste.Generic(
        base=ste.Identifier("Tuple"),
        parameters=(ste.Identifier("Address"), ste.Identifier("ConnectionOptions")))),
]
terminals = [
    ("_", ste.Any()),
    ("foo", ste.Identifier("foo")),
    ("foo.bar", ste.Identifier("foo", "bar")),
]
specials = [
    ("?foo", ste.Optional(base=ste.Identifier("foo"))),
    ("foo or bar", ste.Union(ste.Identifier("foo"), ste.Identifier("bar"))),
    ("?_", ste.Optional(ste.Any())),
    ("_ or bar", ste.Union(ste.Any(), ste.Identifier('bar'))),
    ("?[foo]", ste.Optional(base=ste.List(values=ste.Identifier('foo')))),
    ("[foo] or [bar]", ste.Union(ste.List(values=ste.Identifier('foo')), ste.List(values=ste.Identifier('bar')))),
]
containers = [
    ("(foo)", ste.Tuple),
    ("[foo]", ste.List),
    ("{foo: bar}", ste.Dict),
    ("{foo}", ste.Set),
]
shorthands = [
    ("iter foo", ste.Iterable(base=ste.Literal("foo"))),
    ("with foo", ste.Context(base=ste.Literal("foo"))),
    ("await foo", ste.Awaitable(base=ste.Literal("foo"))),
    ("async iter foo", ste.AsyncIterable(base=ste.Literal("foo"))),
    ("async with foo", ste.AsyncContext(base=ste.Literal("foo"))),
]
# fmt: on


@pytest.mark.parametrize("literal", literals)
def test_literals(literal):
    # testing literals is a little different from other types
    assert parse(str(literal)) == ste.Literal(literal)


@pytest.mark.parametrize("steno, parsed", typing)
def test_typing(steno, parsed):
    assert parse(steno) == parsed


@pytest.mark.parametrize("steno, parsed", terminals)
def test_terminals(steno, parsed):
    assert parse(steno) == parsed


@pytest.mark.parametrize("steno, parsed", specials)
def test_specials(steno, parsed):
    assert parse(steno) == parsed


@pytest.mark.parametrize("steno, parsed", containers)
def test_containers(steno, parsed):
    assert isinstance(parse(steno), parsed)


@pytest.mark.parametrize("steno, parsed", shorthands)
def test_shorthands(steno, parsed):
    assert parse(steno) == parsed


def test_tricky_tuples():
    assert parse("(foo, bar)") == ste.Tuple(
        elements=(ste.Identifier("foo"), ste.Identifier("bar"))
    )
    assert parse("(foo, bar, ...)") == ste.Tuple(
        elements=(ste.Identifier("foo"), ste.Identifier("bar"), ste.Dots())
    )


def test_reprs():
    assert "Dots()" == repr(ste.Dots())
    assert "Any()" == f"{parse('_')}"
    assert "Literal(value=Ellipsis)" == f"{parse('Ellipsis')}"
    assert "Identifier('foo', 'bar')" == f"{parse('foo.bar')}"
    assert "Union(Identifier('foo'), Identifier('bar'))" == f"{parse('foo or bar')}"
