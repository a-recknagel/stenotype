from functools import singledispatch
from typing import Union, TypeVar

from . import elements as ste


@singledispatch
def normalize(element: ste.Steno) -> Union[ste.Dots, ste.Identifier, ste.Generic]:
    """Normalize any element representation to the subset supported by typing"""
    raise NotImplementedError(
        f"{element.__class__.__name__!r} cannot be represented via typing yet"
    )


ID = TypeVar("ID", ste.Dots, ste.Identifier)


@normalize.register(ste.Dots)
@normalize.register(ste.Identifier)
def normalize_identity(element: ID) -> ID:
    return element


# typing expressions
# ==================


@normalize.register(ste.Generic)
def normalize_generic(element: ste.Generic) -> ste.Generic:
    return ste.Generic(
        base=element.base, parameters=tuple(map(normalize, element.parameters))
    )


# stenotype expressions
# =====================

# Special Forms
# -------------


@normalize.register(ste.Any)
def normalize_any(element: ste.Any) -> ste.Identifier:
    return ste.Identifier("typing", "Any")


@normalize.register(ste.Optional)
def normalize_optional(element: ste.Optional) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "Optional"), parameters=(normalize(element.base),)
    )


@normalize.register(ste.Union)
def normalize_union(element: ste.Union) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "Union"),
        parameters=tuple(map(normalize, element)),
    )


# Containers
# ----------


@normalize.register(ste.Tuple)
def normalize_tuple(element: ste.Tuple) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "Tuple"),
        parameters=tuple(map(normalize, element.elements)),
    )


@normalize.register(ste.List)
def normalize_list(element: ste.List) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "List"), parameters=(normalize(element.values),)
    )


@normalize.register(ste.Dict)
def normalize_dict(element: ste.Dict) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "Dict"),
        parameters=(normalize(element.keys), normalize(element.values)),
    )


@normalize.register(ste.Set)
def normalize_set(element: ste.Set) -> ste.Generic:
    return ste.Generic(
        base=ste.Identifier("typing", "Set"), parameters=(normalize(element.values),)
    )


# Literals
# --------


@normalize.register(ste.Literal)
def normalize_literal(element: ste.Literal) -> ste.Generic:
    return ste.Generic(base=ste.Identifier("typing", "Literal"), parameters=(element,))


# Shorthands
# ----------


SHORTHAND = {
    ste.Iterable: ste.Identifier("typing", "Iterable"),
    ste.Context: ste.Identifier("typing", "ContextManager"),
    ste.Awaitable: ste.Identifier("typing", "Awaitable"),
    ste.AsyncIterable: ste.Identifier("typing", "AsyncIterable"),
    ste.AsyncContext: ste.Identifier("typing", "AsyncContextManager"),
}


@normalize.register(ste.Iterable)
@normalize.register(ste.Context)
@normalize.register(ste.Awaitable)
@normalize.register(ste.AsyncIterable)
@normalize.register(ste.AsyncContext)
def normalize_shorthand(
    element: Union[
        ste.Iterable, ste.Context, ste.Awaitable, ste.AsyncIterable, ste.AsyncContext
    ]
) -> ste.Generic:
    return ste.Generic(
        base=SHORTHAND[type(element)], parameters=(normalize(element.base),)
    )
