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

Containers
''''''''''

All containers are specified by their literal notation.

Tuple_:
Fixed size ``()`` literal with element types specified for each position.
Tuples may also be defined with flexible length using ``...`` to arbitrarily repeat the preceding type.

.. code-block:: python
  
  # value
  foo = (1, 'two', 3.0)
  bar = (1, 2, 3, 4, 5, 6)

  # regular
  foo: typing.Tuple[int, str, float]
  bar: typing.Tuple[int, ...]

  # stenotype
  foo: "(int, str, float)"
  bar: "(int, ...)"

----

List_:
Variable size ``[]`` literal with all elements of the same type.
For mixed element types, use a union.

.. code-block:: python

  # value
  foo = [1, 2, 3, 4, 5, 6]
  bar = [1, 'two', 3, 4, 'five', 6]

  # regular
  foo: typing.List[int]
  foo: typing.List[Union[int, str]]

  # stenotype
  foo: "[int]"
  foo: "[int or str]"

----

Dict_:
Variable size ``{}`` literal with all keys and value of the same type, respectively.
For mixed element types, use a union.

.. code-block:: python

  # value
  foo = {'one': 1, 'three': 3, 'two': 2}  

  # regular
  foo: typing.Dict[str, int]

  # stenotype
  foo: "{str: int}"

----

Set_:
Set notation is identical to list notation, the difference between them is not
relevant for the annotation.

.. code-block:: python

  # value
  foo = {1, 2, 3, 5, 6, 4}

  # regular
  foo: typing.Set[int]

  # stenotype
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

.. code-block:: python

  # value
  def foo(a: str, b: int) -> int:
      ...

  # regular
  foo: typing.Callable[[str, int], int]

  # stenotype
  foo: "(str, int) -> int"

.. note::

    Variadic Arguments:

    When the number of arguments is arbitrary, the ``*`` and ``**`` symbols are used.
    Similar to list and dict, the type of *all* variadic arguments is the same; use a union if multiple are accepted.

    .. code-block:: python

       # value
       def foo(a: str, *b: int, **c: float) -> int:
           ...

       # stenotype
       foo: "(str, *int, **float) -> int"

    Named Arguments:
    
    If names of arguments are part of the signature, these can be annotated similar to dictionary keys.
    Use ``name: Type`` instead of just ``Type``; keyword-only arguments are implied by following a ``*`` argument.
    
    .. code-block:: python

       # value
       def foo(a: str, *b: int, c: bool, **d: float) -> int:
           ...

       # stenotype
       foo: "(a: str, *int, c: bool, **float) -> int"

    Names of positional can be ommited; keyword-only arguments must always have a name.
    Note that variadic arguments never have a name.

Common Types
''''''''''''

Iterable_:
The Iterable interface is primarily used for containers that you only plan to
use in loops and for return types of generators. Use the `*` in either context
when using ``stenotype``.

.. code-block:: python

  # regular
  foo: typing.Iterable[int]
  bar: typing.Callable[[], typing.Iterable[bool]]

  # stenotype
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

.. code-block:: python

  # regular
  foo: typing.Union['foo', 'bar', 'baz', 1]

  # stenotype
  foo: "'foo' or 'bar' or 'baz' or 1"

Meta Types
''''''''''

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

Special Function Qualifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use a limited set of keywords to describe a number of common types.
These are especially useful when annotating the return types of functions.
Keywords correspond to how the type is used to get a value of a specifi type.

**Asynchronous function**

.. code-block:: python

  # value
  async def foo(a: A, b: B) -> R:
    return r

  bar = foo(a, b)

  # regular
  foo: typing.Callable[[A, B], typing.Awaitable[R]]
  bar: typing.Awaitable[R]

  # stenotype
  foo: "(A, B) -> await R"
  bar: "await R"

**Asynchronous generator**

.. code-block:: python

  # value
  async def foo(a: A, b: B) -> AsyncIterable[R]:
     yield r
  
  bar = foo(a, b)

  # regular
  foo: typing.Callable[[A, B], typing.AsyncIterable[R]]
  bar: typing.AsyncIterable[R]

  # stenotype
  foo: "(A, B) -> await iter R"
  bar: "await iter R"

**Context managing functions**

.. code-block:: python

  @contextmanager
  def foo(a: A, b: B):
      yield r

  # regular
  foo: typing.Callable[[A, B], typing.ContextManager[R]

  # stenotype
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
