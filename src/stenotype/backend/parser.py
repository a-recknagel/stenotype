"""Stand-in until we have an actual implementation.

Feel free to suggest a better interface, this one is not binding at all and was just a
wild guess on my part on what a respective parse function might need.
"""

from typing import Iterable


def parse(args: Iterable[str], invert):
    if invert:
        for arg in args:
            yield f"stub inverse function: {arg}"
    else:
        for arg in args:
            yield f"stub parse function: {arg}"
