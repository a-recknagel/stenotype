import logging

from stenotype.util import setup_logging


def test_setup_logging():

    # default settings
    assert logging.root.level == 30

    # custom settings
    setup_logging("DEBUG")
    assert logging.root.level == 10
