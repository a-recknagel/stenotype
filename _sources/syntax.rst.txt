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

Any_:
Is used in cases where you have to specify a type but do not want to place
restrictions on it.

.. code-block:: python

  # regular
  foo: typing.Any

  # stenotype
  foo: "_"
  foo: "object"

----

Union_:
If a number of types are admissible for a single variable, just list them all
with an ``or`` between them.

.. code-block:: python

  # regular
  foo: typing.Union[int, float]

  # stenotype
  foo: "int or float"

----

Optional_:
A special case of ``Union``, where the only other option besides the specified
type for a variable is ``None``. ``stenotype`` prepends a question mark, which
is what a few other languages allow as well.

.. code-block:: python

  # regular
  foo: typing.Optional[int]

  # stenotype
  foo: "?int"

----

Tuple_:
Fixed size container where for every element present in it the correct type
should be supplied. Tuples may also be defined with flexible length, which is
useful for variadic functions. All containers should be specified by using
their literal python notation equivalent.

.. code-block:: python

  # regular
  foo: typing.Tuple[int, str, float]
  bar: typing.Tuple[int, ...]

  # stenotype
  foo: "(int, str, float)"
  bar: "(int, ...)"

----

List_:
A typed list should only contain a single type. Use literal notation in
``stenotype`` mode.

.. code-block:: python

  # regular
  foo: typing.List[int]

  # stenotype
  foo: "[int]"

----

Dict_:
A dictionary contains two arguments, one for the key types and one for the
value types. Use literal notation in ``stenotype`` mode.

.. code-block:: python

  # regular
  foo: typing.Dict[str, int]

  # stenotype
  foo: "{str: int}"

----

Set_:
Set notation is identical to list notation, the difference between them is not
relevant for annotation. Use literal notation in ``stenotype`` mode.

.. code-block:: python

  # regular
  foo: typing.Set[int]

  # stenotype
  foo: "{int}"

----

Callable_:
In situations where it's not possible to annotate a function in its signature,
its name can be accessed at a later point in time to add type info.

.. code-block:: python

  # regular
  foo: typing.Callable[[str], int]

  # stenotype
  foo: "(str) -> int"

----

Iterable_:
The Iterable interface is primarily used for containers that you only plan to
use in loops and for return types of generators. Use the `*` in either context
when using ``stenoype``.

.. code-block:: python

  # regular
  foo: typing.Iterable[int]
  bar: typing.Callable[[], typing.Iterable[bool]]

  # stenotype
  foo: "*int"
  bar: "() -> *bool"

----

Literal_:
Literal values are not really types, but they still can be meaningfully used
in annotations. Most often, they will be part of a union, since they'd
otherwise just be constants.

Types can't be expressed as literals in ``stenotype`` mode, since they'd be
interpreted as instances of that type, and not the actual type object.

.. code-block:: python

  # regular
  foo: typing.Union['foo', 'bar', 'baz', 1]

  # stenotype
  foo: "'foo' or 'bar' or 'baz' or 1"

----

TypeVar_

.. code-block:: python

  # regular

  # stenotype

----

Generic_

.. code-block:: python

  # regular

  # stenotype

----

ForwardRef_

.. code-block:: python

  # regular

  # stenotype

----


Special Function Qualifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use a limited set of keywords to describe a number of special functions
in ``stenotype`` when annotating a function object as a variable.

**Asynchronous function**

.. code-block:: python

  # regular
  typing.Callable[[A, B], typing.Awaitable[R]

  # stenotype
  "(A, B) -> await R"

**Asynchronous generator**

.. code-block:: python

  # regular
  typing.Callable[[A, B], typing.AsyncIterable[R]

  # stenotype
  "(A, B) -> await *R"

**Context managing functions**

.. code-block:: python

  # regular
  typing.Callable[[A, B], typing.ContextManager[R]

  # stenotype
  "(A, B) -> with R"


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