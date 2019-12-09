import logging

import pytest

from stenotype.util import setup_logging


def test_setup_logging():

    # default settings
    assert logging.root.level == 30

    # custom settings
    setup_logging("DEBUG")
    assert logging.root.level == 10


@pytest.mark.mypy
def test_if_mypy():
    try:
        import mypy
    except ImportError:
        assert False
    else:
        assert True
