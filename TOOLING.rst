Tooling
=======
.. image:: https://img.icons8.com/wired/64/000000/road-worker.png
   :alt: Project under construction, find an actual icon some time
   :align: center

.. header-end


Containerization
~~~~~~~~~~~~~~~~

Docker_ is used to ensure that the development and deployment environments
are as similar as possible.
If you want to run a high level/integration test of this project locally, you
should do so using the docker image. Make sure `docker is installed`_ if it
isn't already.

If you depend on packages that are not `pure python wheels`_, you need to
build the dependencies (after locking them with poetry) for alpine architecture:

.. code-block:: bash

  $ ./scripts/wheelhouse.sh

This should generate a ``wheels/`` folder in the project root, which docker
needs in order to be able to build the image locally:

.. code-block:: bash

  $ docker build -t stenotype .

It's tagged it with the name ``'stenotype'``, just so it
can be referred to it a little easier when running as a container:

.. code-block:: bash

  $ docker run stenotype

This will execute the default entrypoint of the docker image.

If you want to open a shell to the container in order to debug its environment,
you can do so with

.. code-block:: bash

  $ docker run -it --entrypoint /bin/sh stenotype


Packaging
~~~~~~~~~
If you want to package the project without its dependencies, use the following
command:

.. code-block:: bash

  $ poetry build -f wheel

Poetry will drop `a wheel file`_ in ``dist/``.


Unit Tests
~~~~~~~~~~
This project's unit test suite is run with pytest_. Execute it with:

.. code-block:: bash

  $ pytest tests/


Type Checking
~~~~~~~~~~~~~
Since version 3.5, python supports `type hinting`_. You can run a static
type check with mypy_ like so:

.. code-block:: bash

  $ mypy src/


Linting
~~~~~~~
This project's code style is black_. You can run a classic linter-style test
with the ``check`` flag:

.. code-block:: bash

  $ black src/ tests/ --check

But it is recommended to use black's auto-formatter_ in your editor of choice.


Security
~~~~~~~~
Since we can't check every dependency in-depth for security issues, we rely on
safety_ to tell us which ones are known to deserve a closer look. You can run
it on the current python environment, in case it is properly virtualized and
activated:

.. code-block:: bash

  $ safety check

Conversely, you can also use poetry [1]_ to generate a ``requirements.txt`` for
yor production dependencies and check that instead, which is a little safer and
more explicit:

.. code-block:: bash

  $ poetry export -f requirements.txt
  $ safety check -r requirements.txt

But checking third party packages is not enough, we also need to check our own
code. Or rather, we let bandit_ do it:

.. code-block:: bash

  $ bandit -r src/

Once these two tools have run with zero issues, you can be reasonably confident
that your code didn't blow glaring security holes into the project.


Coverage
~~~~~~~~
Testing the coverage is a bit iffy and not always super reliable, but we try our
best. Right now we only use unit tests to test the code, so using the
`coverage.py`_ wrapper pytest-cov_ makes a lot of sense and means that the
configuration is a lot easier.

If at some point other test suite runners are used for
smoke/functional/integration testing, we'll need to combine multiple calibrated
runs with a bare coverage.py instead.

Anyway, right now it's just:

.. code-block:: bash

  $ pytest tests/ --cov

.. _Docker: https://www.docker.com/
.. _docker is installed: https://docs.docker.com/install/
.. _pure python wheels: https://packaging.python.org/guides/distributing-packages-using-setuptools/#pure-python-wheels
.. _a wheel file: https://pythonwheels.com/
.. _pytest: https://docs.pytest.org/en/latest/
.. _type hinting: https://www.python.org/dev/peps/pep-0484/
.. _mypy: http://mypy-lang.org/
.. _black: https://black.readthedocs.io/en/stable/the_black_code_style.html
.. _auto-formatter: https://black.readthedocs.io/en/stable/editor_integration.html
.. _safety: https://pypi.org/project/safety/
.. _bandit: https://pypi.org/project/bandit/
.. _coverage.py: https://coverage.readthedocs.io/en/v4.5.x/
.. _pytest-cov: https://pypi.org/project/pytest-cov/

----

.. [1] At the time of writing, the ``export`` command is only available in pre-releases 1.0.0a0 and up.