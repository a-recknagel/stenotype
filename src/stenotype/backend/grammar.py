"""
Grammar for parsing :py:mod:`stenotype` strings to :py:mod:`~stenotype.backend.elements`
"""
from keyword import kwlist
from pyparsing import (
    Word,
    alphas,
    Forward,
    delimitedList,
    Literal,
    Keyword,
    nums,
    Group,
    Suppress,
    OneOrMore,
    ParseResults,
    Optional,
    QuotedString,
    Combine,
    MatchFirst,
)

from . import elements as ste


__all__ = ["parse"]


def unpack(results: ParseResults) -> tuple:
    """Unpack the members of a :py:class:`~.ParseResults` to a :py:class:`tuple`"""
    return tuple(item[0] for item in results)


#: Words that are not valid identifiers
KEYWORDS = Forward()
KEYWORDS.setName("KEYWORD")
KEYWORDS << MatchFirst(tuple(map(Keyword, kwlist)))

#: literal `...`, e.g. in `typing.Tuple[int, ...]`, not an `Ellipsis`
DOTS = Literal("...").setParseAction(lambda: ste.Dots())
KEYWORDS << MatchFirst((*KEYWORDS.expr.exprs, DOTS))

#: any valid typing or stenotype expression, such as `List`, `typing.List`, `?List`, ...
TYPE = Forward()
TYPE.setName("TYPE")
TYPE_exclude_UNION = Forward()
TYPE_exclude_UNION.setName("TYPE_exclude_UNION")

# typing expressions
# ==================

#: a direct or nested reference, such as `List` or `typing.List`
IDENTIFIER = (
    delimitedList((~KEYWORDS + Word(alphas)).setName("IDENTIFIER"), delim=".")
    .setName("NAME")
    .setParseAction(lambda s, l, toks: ste.Identifier(*toks))
)

#: a subscribed reference, such as `List[...]`
GENERIC = (
    (IDENTIFIER + Suppress("[") + delimitedList(Group(TYPE)) + Suppress("]"))
    .setName("NAME '[' TYPE {',' TYPE} ']'")
    .setParseAction(lambda s, loc, toks: ste.Generic(toks[0], unpack(toks[1:])))
)

#: any valid typing expression
TYPING = (GENERIC | IDENTIFIER).setName("GENERIC | IDENTIFIER")

# stenotype expressions
# =====================

# Special Forms
# -------------

#: `Any` as `_`
ANY = Keyword("_").setName("'_'").setParseAction(lambda s, loc, toks: ste.Any())

_OPTIONAL_SYMBOL = Literal("?")
#: `Optional[TP]` as `?TP`
OPTIONAL = (
    Suppress(_OPTIONAL_SYMBOL)
    + ~_OPTIONAL_SYMBOL
    + Group(TYPE).setParseAction(lambda s, loc, toks: ste.Optional(toks[0][0]))
).setName("'?' TYPE")

_UNION_SEPARATOR = Keyword("or")
#: `Union[TA, TB]`` as ``TA or TB``
UNION = (
    (TYPE_exclude_UNION + OneOrMore(Suppress(_UNION_SEPARATOR) + TYPE_exclude_UNION))
    .setName("TYPE 'or' TYPE {'or' TYPE}")
    .setParseAction(lambda s, loc, toks: ste.Union(*toks))
)

KEYWORDS << MatchFirst((*KEYWORDS.expr.exprs, _UNION_SEPARATOR))
#: all special forms
SPECIALS = MatchFirst((UNION, ANY, OPTIONAL)).setName("UNION | ANY | OPTIONAL")

# Containers
# ----------

#: `Tuple[TA, TB, ...]` as `(TA, TB, ...)`
TUPLE = (
    (
        Suppress("(")
        + delimitedList(TYPE)
        + Optional(Suppress(",") + DOTS)
        + Suppress(")")
    )
    .setName("'(' TYPE {',' TYPE} [',' '...'] ')'")
    .setParseAction(lambda s, loc, toks: ste.Tuple(tuple(toks)))
)
#: `List[TA]` as `[TA]`
LIST = (
    (Suppress("[") + TYPE + Suppress("]"))
    .setName("'[' TYPE ']'")
    .setParseAction(lambda s, loc, toks: ste.List(toks[0]))
)
#: `Dict[TK, TV]` as `{TK: TV}`
DICT = (
    (Suppress("{") + TYPE + Suppress(":") + TYPE + Suppress("}"))
    .setName("'{' TYPE ':' TYPE '}'")
    .setParseAction(lambda s, loc, toks: ste.Dict(toks[0], toks[1]))
)
#: `Set[TA]` as `{TA}`
SET = (
    (Suppress("{") + TYPE + Suppress("}"))
    .setName("'{' TYPE '}'")
    .setParseAction(lambda s, loc, toks: ste.Set(toks[0]))
)

#: all container literals
CONTAINERS = MatchFirst((TUPLE, LIST, DICT, SET)).setName("TUPLE | LIST | DICT | SET")

# Literals
# --------

#: a literal bool, i.e. `True` or `False`
LITERAL_BOOL = (
    (Keyword("True") | Keyword("False"))
    .setName("'True' | 'False'")
    .setParseAction(
        lambda s, loc, toks: ste.Literal(True)
        if toks[0] == "True"
        else ste.Literal(False)
    )
)
#: a literal `None`
LITERAL_NONE = (
    (Keyword("None"))
    .setName("'None'")
    .setParseAction(lambda s, loc, toks: ste.Literal(None))
)
#: a literal `Ellipsis` or `...`
LITERAL_ELLIPSIS = (
    (Keyword("Ellipsis"))
    .setName("'Ellipsis'")
    .setParseAction(lambda s, loc, toks: ste.Literal(Ellipsis))
)
#: any literal `int`
LITERAL_INT = (
    (Combine(Optional("-") + Word(nums)))
    .setName("INTEGER")
    .setParseAction(lambda s, loc, toks: ste.Literal(int(toks[0])))
)
_string_opts = dict(unquoteResults=False, convertWhitespaceEscapes=False)
#: any literal `str`
LITERAL_STR = (
    (
        QuotedString('"', escChar="\\", **_string_opts)
        | QuotedString("'", escChar="\\", **_string_opts)
    )
    .setName("STRING")
    .setParseAction(lambda s, loc, toks: ste.Literal(toks[0]))
)
#: any literal `bytes`
LITERAL_BYTES = (
    (
        "b"
        + (
            QuotedString('"', escChar="\\", **_string_opts)
            | QuotedString("'", escChar="\\", **_string_opts)
        )
    )
    .setName("BYTES")
    .setParseAction(lambda s, loc, toks: ste.Literal("b" + toks[1]))
)
# TODO: float (does this even make sense? float is notoriously bad for precise values)

KEYWORDS << MatchFirst(
    (*KEYWORDS.expr.exprs, LITERAL_BOOL, LITERAL_NONE, LITERAL_ELLIPSIS)
)
#: all literal values
LITERALS = MatchFirst(
    (
        LITERAL_BOOL,
        LITERAL_NONE,
        LITERAL_ELLIPSIS,
        LITERAL_INT,
        LITERAL_STR,
        LITERAL_BYTES,
    )
).setName(
    " | ".join(
        (
            "LITERAL_BOOL",
            "LITERAL_NONE",
            "LITERAL_ELLIPSIS",
            "LITERAL_INT",
            "LITERAL_STR",
        )
    )
)

# Shorthands
# ----------

#: `Iterable[T]` as `iter T`
ITERABLE = (
    (Keyword("iter") + TYPE)
    .setName("'iter' TYPE")
    .setParseAction(lambda s, loc, toks: ste.Iterable(toks[1]))
)
#: `ContextManager[T]` as `with T`
CONTEXT = (
    (Keyword("with") + TYPE)
    .setName("'with' TYPE")
    .setParseAction(lambda s, loc, toks: ste.Context(toks[1]))
)
#: `Awaitable[T]` as `await T`
AWAITABLE = (
    (Keyword("await") + TYPE)
    .setName("'await' TYPE")
    .setParseAction(lambda s, loc, toks: ste.Awaitable(toks[1]))
)
#: `AsyncIterable[T]` as `async iter T`
ASYNC_ITERABLE = (
    (Keyword("async iter") + TYPE)
    .setName("'async iter' TYPE")
    .setParseAction(lambda s, loc, toks: ste.AsyncIterable(toks[1]))
)
#: `AsyncContextManager[T]` as `async with T`
ASYNC_CONTEXT = (
    (Keyword("async with") + TYPE)
    .setName("'async with' TYPE")
    .setParseAction(lambda s, loc, toks: ste.AsyncContext(toks[1]))
)

KEYWORDS << MatchFirst(
    (
        *KEYWORDS.expr.exprs,
        ITERABLE.exprs[0],
        CONTEXT.exprs[0],
        AWAITABLE.exprs[0],
        ASYNC_ITERABLE.exprs[0],
        ASYNC_CONTEXT.exprs[0],
    )
)
#: all shorthand notations
SHORTHANDS = MatchFirst(
    (ITERABLE, CONTEXT, AWAITABLE, ASYNC_ITERABLE, ASYNC_CONTEXT)
).setName(
    " | ".join(("ITERABLE", "CONTEXT", "AWAITABLE", "ASYNC_ITERABLE", "ASYNC_CONTEXT"))
)

# Callable
# ----------

#: `Callable[[A, B], R]` as `(A, B) -> R`
#: `Protocol.__call__(a: A, b: B, /, c: C, d: D, *args) -> R`

# Parsing the signature is tricky, because delimiters depend on whether
# two complex elements are joined. The parse rules thus are built from
# individual complex elements, arranged in various combinations.

# Individual parameters as `A` or `a: A`
NAME = (~KEYWORDS + Word(alphas)).setName("NAME")
PARAMETER = (
    (Optional(NAME + Suppress(":"), default=None) + TYPE)
    .setName("[NAME ':'] TYPE")
    .setParseAction(lambda s, loc, toks: ste.Parameter(name=toks[0], base=toks[1]))
)
NAMED_PARAMETER = (
    (NAME + Suppress(":") + TYPE)
    .setName("NAME ':' TYPE")
    .setParseAction(lambda s, loc, toks: ste.Parameter(name=toks[0], base=toks[1]))
)

# Individual parts of the signature
SIGNATURE_POSITIONAL = (
    (delimitedList(PARAMETER) + Suppress(",") + Suppress("/"))
    .setName("[NAME ':'] TYPE {',' [NAME ':'] TYPE} ',' '/'")
    .setResultsName("positional")
)
SIGNATURE_MIXED = (
    delimitedList(PARAMETER)
    .setName("[NAME ':'] TYPE {',' [NAME ':'] TYPE}")
    .setResultsName("mixed")
)
SIGNATURE_ARGS = (
    Suppress("*") + (Optional(PARAMETER, default=None).setResultsName("args"))
).setName("'*' [TYPE]")
SIGNATURE_KEYWORDS = (
    delimitedList(NAMED_PARAMETER)
    .setName("NAME ':' TYPE {',' NAME ':' TYPE}")
    .setResultsName("keywords")
)
SIGNATURE_KWARGS = (Suppress("**") + Group(PARAMETER).setResultsName("kwargs")).setName(
    "'**' TYPE"
)
SIGNATURE_RETURN = Suppress("->") + TYPE.setResultsName("returns").setName("-> TYPE")

# Match for the entire parameter list
# This does a recursive ``head + Optional(delimiter + tail) or tail``. This
# creates any combination of optional tails starting from any head.
# Based on the Python 3.8 Function Definitions grammar
PARAMETER_LIST_STARARGS = MatchFirst(
    (
        SIGNATURE_ARGS
        + Optional(Suppress(",") + SIGNATURE_KEYWORDS)
        + Optional(Suppress(",") + SIGNATURE_KWARGS),
        SIGNATURE_KWARGS,
    )
)
PARAMETER_LIST_NO_POSONLY = MatchFirst(
    (
        SIGNATURE_MIXED + Optional(Suppress(",") + PARAMETER_LIST_STARARGS),
        PARAMETER_LIST_STARARGS,
    )
)
PARAMETER_LIST = MatchFirst(
    (
        SIGNATURE_POSITIONAL + Optional(Suppress(",") + PARAMETER_LIST_NO_POSONLY),
        PARAMETER_LIST_NO_POSONLY,
    )
)

# The actual call signature
SIGNATURE = (
    (Suppress("(") + PARAMETER_LIST + Suppress(")") + SIGNATURE_RETURN)
    .setName(
        # This does not exactly replicate leading/trailing
        # comma separators, but is much more readable.
        "'(' "
        "[{[NAME ':'] TYPE ','} '/' ','] "
        "{[NAME ':'] TYPE ','} "
        "[* [[NAME ':' ] TYPE] ','] "
        "{NAME ':' TYPE ','} "
        "[** [[NAME ':'] TYPE]] "
        "')' '->' TYPE"
    )
    .setParseAction(
        lambda s, loc, toks: ste.Signature(
            positional=tuple(toks.positional),
            mixed=tuple(toks.mixed),
            args=toks.args[0] if toks.args else None,
            keywords=tuple(toks.keywords),
            kwargs=toks.kwargs[0] if toks.kwargs else None,
            returns=toks.returns,
        )
    )
)

#: any valid stenotype expression
STENOTYPE = MatchFirst(
    (SIGNATURE, *SPECIALS.exprs, *CONTAINERS.exprs, *LITERALS.exprs, *SHORTHANDS.exprs)
).setName("SPECIALS | CONTAINERS | LITERALS | SHORTHANDS")

TYPE << MatchFirst((*STENOTYPE.exprs, *TYPING.exprs))
TYPE_exclude_UNION << (CONTAINERS | LITERALS | SHORTHANDS | ANY | OPTIONAL | TYPING)


def parse(steno_string: str) -> ste.Steno:
    """Parse a stenotype or typing string to element representation"""
    return TYPE.parseString(steno_string, parseAll=True)[0]  # type: ignore
