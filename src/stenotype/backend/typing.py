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


@normalize.register(ste.Callable)
def normalize_generic(element: ste.Callable) -> ste.Callable:
    if isinstance(element.positional, ste.Dots):
        return element
    return ste.Callable(
        positional=tuple(map(normalize, element.positional)), returns=element.returns
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


# Callables
# ---------


@normalize.register(ste.Signature)
def normalize_signature(element: ste.Signature):
    # TODO: declare a ``Protocol`` if ``Callable`` is not enough
    return _normalize_callable(element)


def _normalize_callable(element: ste.Signature) -> ste.Callable:
    if element.keywords or element.kwargs:
        raise ValueError("'typing.Callable' does not support keyword arguments")
    if element.args:
        # args may have a name, but it is inconsequential to the call
        if not isinstance(element.args.base, ste.Any):
            raise ValueError(
                "'typing.Callable' does not support typed variadic arguments"
            )
        if element.positional or element.mixed:
            raise ValueError(
                "'typing.Callable' does not support explicit and variadic arguments"
            )
        return ste.Callable(positional=ste.Dots(), returns=element.returns)
    else:
        # names of arguments may be relevant, do not discard
        if any(arg.name is not None for arg in element.positional + element.mixed):
            raise ValueError("'typing.Callable' does not support named arguments")
        return ste.Callable(
            positional=tuple(arg.base for arg in element.positional + element.mixed),
            returns=element.returns,
        )
