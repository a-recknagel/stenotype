from functools import singledispatch
from typing import Union

from . import elements as ste


@singledispatch
def unparse(element: ste.Steno) -> str:
    """Unparse element representation to a stenotype string"""
    raise NotImplementedError(
        f"{element.__class__.__name__!r} cannot be represented as a stenotype yet"
    )


@unparse.register(ste.Dots)
def unparse_dots(element: ste.Dots) -> str:
    return "..."


# typing expressions
# ==================


@unparse.register(ste.Identifier)
def unparse_identifier(element: ste.Identifier) -> str:
    return ".".join(element)


@unparse.register(ste.Generic)
def unparse_generic(element: ste.Generic) -> str:
    return f'{unparse(element.base)}[{", ".join(map(unparse, element.parameters))}]'


# stenotype expressions
# =====================

# Special Forms
# -------------


@unparse.register(ste.Any)
def unparse_any(element: ste.Any) -> str:
    return "_"


@unparse.register(ste.Optional)
def unparse_optional(element: ste.Optional) -> str:
    return "?" + unparse(element.base)


@unparse.register(ste.Union)
def unparse_union(element: ste.Union) -> str:
    return " or ".join(map(unparse, element))


# Containers
# ----------


@unparse.register(ste.Tuple)
def unparse_tuple(element: ste.Tuple) -> str:
    return f'({", ".join(map(unparse, element.elements))})'


@unparse.register(ste.List)
def unparse_list(element: ste.List) -> str:
    return f"[{unparse(element.values)}]"


@unparse.register(ste.Dict)
def unparse_dict(element: ste.Dict) -> str:
    return f"{{{unparse(element.keys)}: {unparse(element.values)}}}"


@unparse.register(ste.Set)
def unparse_set(element: ste.Set) -> str:
    return f"{{{unparse(element.values)}}}"


# Literals
# --------


@unparse.register(ste.Literal)
def unparse_literal(element: ste.Literal) -> str:
    return str(element.value)


# Shorthands
# ----------


SHORTHAND = {
    ste.Iterable: "iter",
    ste.Context: "with",
    ste.Awaitable: "await",
    ste.AsyncIterable: "async iter",
    ste.AsyncContext: "async with",
}


@unparse.register(ste.Iterable)
@unparse.register(ste.Context)
@unparse.register(ste.Awaitable)
@unparse.register(ste.AsyncIterable)
@unparse.register(ste.AsyncContext)
def unparse_shorthand(
    element: Union[
        ste.Iterable, ste.Context, ste.Awaitable, ste.AsyncIterable, ste.AsyncContext
    ]
) -> str:
    return f"{SHORTHAND[type(element)]} {unparse(element.base)}"
