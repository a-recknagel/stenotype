import pytest

from stenotype.backend import elements as ste
from stenotype.backend.grammar import parse, SIGNATURE


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
callables = [
    ("Callable[..., R]", ste.Callable(
        positional=ste.Dots(), returns=ste.Identifier("R")
    )),
    ("typing.Callable[..., R]", ste.Callable(
        positional=ste.Dots(), returns=ste.Identifier("R")
    )),
    ("Callable[[A], R]", ste.Callable(
        positional=(ste.Identifier("A"),),
        returns=ste.Identifier("R")
    )),
    ("typing.Callable[[A, B, C], R]", ste.Callable(
        positional=(
            ste.Identifier("A"), ste.Identifier("B"), ste.Identifier("C"),
        ),
        returns=ste.Identifier("R")
    )),
]
signatures = [
    ("(A, /) -> R", ste.Signature(
        positional=(ste.Parameter(name=None, base=ste.Identifier("A")),),
        mixed=(),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(A, B, /) -> R", ste.Signature(
        positional=(
            ste.Parameter(name=None, base=ste.Identifier("A")),
            ste.Parameter(name=None, base=ste.Identifier("B"))
        ),
        mixed=(),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(A) -> R", ste.Signature(
        positional=(),
        mixed=(ste.Parameter(name=None, base=ste.Identifier("A")),),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(A, B) -> R", ste.Signature(
        positional=(),
        mixed=(
            ste.Parameter(name=None, base=ste.Identifier("A")),
            ste.Parameter(name=None, base=ste.Identifier("B")),
        ),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(a: A) -> R", ste.Signature(
        positional=(),
        mixed=(ste.Parameter(name="a", base=ste.Identifier("A")),),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(a: A, b: B) -> R", ste.Signature(
        positional=(),
        mixed=(
            ste.Parameter(name="a", base=ste.Identifier("A")),
            ste.Parameter(name="b", base=ste.Identifier("B")),
        ),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(A, b: B) -> R", ste.Signature(
        positional=(),
        mixed=(
            ste.Parameter(name=None, base=ste.Identifier("A")),
            ste.Parameter(name="b", base=ste.Identifier("B")),
        ),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(A, b: B, *) -> R", ste.Signature(
        positional=(),
        mixed=(
            ste.Parameter(name=None, base=ste.Identifier("A")),
            ste.Parameter(name="b", base=ste.Identifier("B")),
        ),
        args=None,
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(*a: A) -> R", ste.Signature(
        positional=(),
        mixed=(),
        args=ste.Parameter(name="a", base=ste.Identifier("A")),
        keywords=(),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(*, a: A) -> R", ste.Signature(
        positional=(),
        mixed=(),
        args=None,
        keywords=(ste.Parameter(name="a", base=ste.Identifier("A")),),
        kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(*, **a: A) -> R", ste.Signature(
        positional=(),
        mixed=(),
        args=None,
        keywords=(),
        kwargs=ste.Parameter(name="a", base=ste.Identifier("A")),
        returns=ste.Identifier("R"),
    )),
    ("(a: A, B, /, C, d: D, *e: E, f: F, **g: G) -> R", ste.Signature(
        positional=(
            ste.Parameter(name="a", base=ste.Identifier("A")),
            ste.Parameter(name=None, base=ste.Identifier("B")),
        ),
        mixed=(
            ste.Parameter(name=None, base=ste.Identifier("C")),
            ste.Parameter(name="d", base=ste.Identifier("D")),
        ),
        args=ste.Parameter(name="e", base=ste.Identifier("E")),
        keywords=(
            ste.Parameter(name="f", base=ste.Identifier("F")),
        ),
        kwargs=ste.Parameter(name="g", base=ste.Identifier("G")),
        returns=ste.Identifier("R"),
    )),
    ("(*_) -> R", ste.Signature(
        positional=(), mixed=(),
        args=ste.Parameter(name=None, base=ste.Any()),
        keywords=(), kwargs=None,
        returns=ste.Identifier("R"),
    )),
    ("(...) -> R", ste.Signature(
        positional=(), mixed=(),
        args=ste.Parameter(name=None, base=ste.Any()),
        keywords=(), kwargs=None,
        returns=ste.Identifier("R"),
    )),
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


@pytest.mark.parametrize("steno, parsed", callables)
def test_callables(steno, parsed):
    assert parse(steno) == parsed


@pytest.mark.parametrize("steno, parsed", signatures)
def test_signatures(steno, parsed):
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
