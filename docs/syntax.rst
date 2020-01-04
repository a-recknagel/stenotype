Syntax Definition
-----------------

Valid ``stenotype`` annotations will always cleanly map to regular type
annotations. The conversion rules are collected in this document.

How to Annotate Functions and Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Function signature annotation was added with `PEP 3017`_ and properly defined
in `PEP 484`_. This annotation is made up of two parts: The argument annotation
and the return value annotation:

.. code-block:: python

  def foo(a: A, b: B) -> R:
      ...

Variable annotation was added a little later with `PEP 526`_, and written as
follows:

.. code-block:: python

  foo: Var_Type

Since a function is just another object, it can also be annotation in this way.
For example, the function from above could also have been annotated as follows:

.. code-block:: python

  from typing import Callable
  foo: Callable[[A, B], R]

----

This structure will remain as is. ``stenotype`` only influences the way types
are expressed, not where they can be meaningfully used.

All but the variable notation of function types will also stay structurally
similar. Given the examples, they would change in the following ways:

.. code-block:: python

  # function signature notation
  def foo(a: "A", b: "B") -> "R":
      ...

  # variable notation of plain variables
  foo: "Var_Type"

  # variable notation of functions
  foo: "(A, B) -> R"


``typing``-Types Equivalent Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Special Forms
'''''''''''''

Special forms use reserved symbols to represent special types.

Any_:
Is used in cases where you have to specify a type but do not want to place
restrictions on it.

.. content-tabs::

    .. tab-container:: any_regular
        :title: regular

        .. code-block:: python

          foo: typing.Any

    .. tab-container:: any_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "_"
          foo: "object"

----

Union_:
If a number of types are admissible for a single variable, just list them all
with an ``or`` between them.

.. content-tabs::

    .. tab-container:: union_regular
        :title: regular

        .. code-block:: python

          foo: typing.Union[int, float]

    .. tab-container:: union_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "int or float"

----

Optional_:
A special case of ``Union``, where the only other option besides the specified
type for a variable is ``None``. ``stenotype`` prepends a question mark, which
is what a few other languages allow as well.

.. content-tabs::

    .. tab-container:: optional_regular
        :title: regular

        .. code-block:: python

          foo: typing.Optional[int]

    .. tab-container:: optional_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "?int"

Containers
''''''''''

All containers are specified by their literal notation.

Tuple_:
Fixed size ``()`` literal with element types specified for each position.
Tuples may also be defined with flexible length using ``...`` to arbitrarily repeat the
preceding type.

.. content-tabs::

    .. tab-container:: tuple_value
        :title: value

        .. code-block:: python

          foo = (1, 'two', 3.0)
          bar = (1, 2, 3, 4, 5, 6)

    .. tab-container:: tuple_regular
        :title: regular

        .. code-block:: python

          foo: typing.Tuple[int, str, float]
          bar: typing.Tuple[int, ...]

    .. tab-container:: tuple_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "(int, str, float)"
          bar: "(int, ...)"

----

List_:
Variable size ``[]`` literal with all elements of the same type.
For mixed element types, use a union.

.. content-tabs::

    .. tab-container:: list_value
        :title: value

        .. code-block:: python

          foo = [1, 2, 3, 4, 5, 6]
          bar = [1, 'two', 3, 4, 'five', 6]

    .. tab-container:: list_regular
        :title: regular

        .. code-block:: python

          foo: typing.List[int]
          foo: typing.List[Union[int, str]]

    .. tab-container:: list_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "[int]"
          foo: "[int or str]"

----

Dict_:
Variable size ``{}`` literal with all keys and value of the same type, respectively.
For mixed element types, use a union.

.. content-tabs::

    .. tab-container:: dict_value
        :title: value

        .. code-block:: python

          foo = {'one': 1, 'three': 3, 'two': 2}

    .. tab-container:: dict_regular
        :title: regular

        .. code-block:: python

          foo: typing.Dict[str, int]

    .. tab-container:: dict_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "{str: int}"

----

Set_:
Set notation is identical to list notation, the difference between them is not
relevant for the annotation.

.. content-tabs::

    .. tab-container:: set_value
        :title: value

        .. code-block:: python

          foo = {1, 2, 3, 5, 6, 4}

    .. tab-container:: set_regular
        :title: regular

        .. code-block:: python

          foo: typing.Set[int]

    .. tab-container:: set_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "{int}"

Signatures
''''''''''

Specifying the signature of functions is important for wrappers (e.g. decorators),
callbacks and higher-order functions. It also allows annotating functions from
third-party libraries which lack annotations.

Callable_:
In situations where it's not possible to annotate a function in its signature,
its name can be accessed at a later point in time to add type info.
This can also be used to specify the type of callbacks or higher-order functions.

.. content-tabs::

    .. tab-container:: callable_value
        :title: value

        .. code-block:: python

          def foo(a: str, b: int) -> int:
              ...

    .. tab-container:: callable_regular
        :title: regular

        .. code-block:: python

          foo: typing.Callable[[str, int], int]

    .. tab-container:: callable_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "(str, int) -> int"

If the parameters of the signature are unknown or not relevant,
use ``...`` for the arguments -- e.g. ``(...) -> int``.

.. note::

    Variadic and Named Arguments:

    When the number of arguments is arbitrary, the ``*`` and ``**`` symbols are used.
    Similar to list and dict, the type of *all* variadic arguments is the same; use a
    union if multiple are accepted.

    If names of arguments are part of the signature, these can be annotated similar to
    dictionary keys. Use ``name: Type`` instead of just ``Type``. Keyword-only
    arguments are implied by following a ``*`` argument, positional-only arguments
    by preceding an empty ``/`` argument.

    .. content-tabs::

        .. tab-container:: variadic_value
            :title: value

            .. code-block:: python

              def foo(a: str, /, b: int, *c: bool, d: bytes, **e: float) -> int:
                  ...

        .. tab-container:: variadic_regular
            :title: regular

            .. code-block:: python

              class Signature(Protocol):
                  def __call__(a: str, /, b: int, *c: bool, d: bytes, **c: float) -> int:
                    ...

              foo: Signature

        .. tab-container:: variadic_stenotype
            :title: stenotype

            .. code-block:: python

              foo: "(str, /, b: int, *c: bool, d: bytes, **float) -> int"

    Names of positional and variadic arguments can be omitted;
    keyword-only arguments must always have a name.

Common Types
''''''''''''

Iterable_:
The Iterable interface is primarily used for containers that you only plan to
use in loops and for return types of generators. Use the `*` in either context
when using ``stenotype``.

.. content-tabs::

    .. tab-container:: iterable_regular
        :title: regular

        .. code-block:: python

          foo: typing.Iterable[int]
          bar: typing.Callable[[], typing.Iterable[bool]]

    .. tab-container:: iterable_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "iter int"
          bar: "() -> iter bool"

Literal_:
Literal values are not really types, but they still can be meaningfully used
in annotations. Most often, they will be part of a union, since they'd
otherwise just be constants.

Types can't be expressed as literals in ``stenotype`` mode, since they'd be
interpreted as instances of that type, and not the actual type object.
Only constants (``True``, ``False``, ``None``, ``Ellipsis``) and primitive literals
(``str``, ``int``, ``float``) are valid for literal types.

.. content-tabs::

    .. tab-container:: literal_regular
        :title: regular

        .. code-block:: python

          foo: typing.Union['foo', 'bar', 'baz', 1]

    .. tab-container:: literal_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "'foo' or 'bar' or 'baz' or 1"

Meta Types
''''''''''

TypeVar_

.. content-tabs::

    .. tab-container:: typevar_regular
        :title: regular

        .. code-block:: python

          # code

    .. tab-container:: typevar_stenotype
        :title: stenotype

        .. code-block:: python

          # code

----

Generic_

.. content-tabs::

    .. tab-container:: generic_regular
        :title: regular

        .. code-block:: python

          # code

    .. tab-container:: generic_stenotype
        :title: stenotype

        .. code-block:: python

          # code

----

ForwardRef_

.. content-tabs::

    .. tab-container:: forwardref_regular
        :title: regular

        .. code-block:: python

          # code

    .. tab-container:: forwardref_stenotype
        :title: stenotype

        .. code-block:: python

          # code

Special Function Qualifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use a limited set of keywords to describe a number of common types.
These are especially useful when annotating the return types of functions.
Keywords correspond to how the type is used to get a value of a specifi type.

**Asynchronous function**

.. content-tabs::

    .. tab-container:: async_value
        :title: value

        .. code-block:: python

          async def foo(a: A, b: B) -> R:
              return r

          bar = foo(a, b)

    .. tab-container:: async_regular
        :title: regular

        .. code-block:: python

          foo: typing.Callable[[A, B], typing.Awaitable[R]]
          bar: typing.Awaitable[R]

    .. tab-container:: async_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "(A, B) -> await R"
          bar: "await R"

**Asynchronous generator**

.. content-tabs::

    .. tab-container:: asyncgen_value
        :title: value

        .. code-block:: python

          async def foo(a: A, b: B) -> AsyncIterable[R]:
              yield r

          bar = foo(a, b)

    .. tab-container:: asyncgen_regular
        :title: regular

        .. code-block:: python

          foo: typing.Callable[[A, B], typing.AsyncIterable[R]]
          bar: typing.AsyncIterable[R]

    .. tab-container:: asyncgen_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "(A, B) -> await iter R"
          bar: "await iter R"

**Context managing functions**

.. content-tabs::

    .. tab-container:: contextmanager_value
        :title: value

        .. code-block:: python

            @contextmanager
            def foo(a: A, b: B):
                yield r


    .. tab-container:: contextmanager_regular
        :title: regular

        .. code-block:: python

          foo: typing.Callable[[A, B], typing.ContextManager[R]

    .. tab-container:: contextmanager_stenotype
        :title: stenotype

        .. code-block:: python

          foo: "(A, B) -> with R"

.. _PEP 3017: https://www.python.org/dev/peps/pep-3107/
.. _PEP 484: https://www.python.org/dev/peps/pep-0484/
.. _PEP 526: https://www.python.org/dev/peps/pep-0526/

.. _Any: https://docs.python.org/3/library/typing.html#the-any-type
.. _Union: https://docs.python.org/3/library/typing.html#typing.Union
.. _Optional: https://docs.python.org/3/library/typing.html#typing.Optional
.. _Tuple: https://docs.python.org/3/library/typing.html#typing.Tuple
.. _List: https://docs.python.org/3/library/typing.html#typing.List
.. _Dict: https://docs.python.org/3/library/typing.html#typing.Dict
.. _Set: https://docs.python.org/3/library/typing.html#typing.Set
.. _Iterable:  https://docs.python.org/3/library/typing.html#typing.Iterable
.. _Callable: https://docs.python.org/3/library/typing.html#typing.Callable
.. _TypeVar: https://docs.python.org/3/library/typing.html#typing.TypeVar
.. _Generic: https://docs.python.org/3/library/typing.html#typing.Generic
.. _Literal: https://www.python.org/dev/peps/pep-0586/#id17
.. _ForwardRef: https://docs.python.org/3/library/typing.html#typing.ForwardRef
