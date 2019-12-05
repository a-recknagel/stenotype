"""Command Line Interface for stenotype.

The backend is exposed here through a simple command line interface. Documentation of
their usage is contained in the docstrings, which are written in a way that they will be
rendered nicely by click's automatic --help text generator.
"""
from logging import getLogger

import click

from stenotype.backend.grammar import parse
from stenotype.backend.steno import unparse
from stenotype.backend.typing import normalize as to_typing
from stenotype import util, __version__

log = getLogger(__name__)


@click.command()
@click.option(
    "-v", "--version", is_flag=True, help="Print stenotype's version number and exit."
)
@click.option(
    "-l",
    "--loglevel",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Set the loglevel.",
)
@click.option(
    "-s",
    "--shorten",
    is_flag=True,
    help="Inverts the parser to instead try to generate stenotype from standard types.",
)
@click.option(
    "-c",
    "--check",
    is_flag=True,
    help="Disables the check-skipping, annotations need to be written as they would "
    "be in source files in this mode.",
)
@click.argument("args", nargs=-1)
def cli(args, version, loglevel, shorten, check):
    """CLI entrypoint to test the stenotype backend.

    Enter any number of stenotype expressions to see which standard annotations they will
    resolve into. There is no need to double quote expression or to assign them to a
    value, the following will just work:

    \b
      $ stenotype 'bool or int'
      typing.Union[bool, int]
      $ stenotype '(int) -> bool'
      typing.Signature[[int], bool]

    You can also enter multiple arguments that will be executed in turn and consider each
    other in the context of, for example, custom type variables:

    \b
      $ stenotype 'T, int' 'bool or T'
      T = TypeVar[int]
      typing.Union[bool, T]
    """
    # early exits
    if version:
        click.echo(f"stenotype {__version__}")
        exit(0)
    if shorten and check:
        click.echo(
            "Flags --shorten and --check can't be used simultaneously.", err=True
        )
        exit(1)
    if not args:
        click.echo("No arguments entered, nothing to do.", err=True)
        exit(0)

    util.setup_logging(loglevel)
    try:
        if shorten:
            expressions = (f"stub inverse function: {arg}" for arg in args)
        else:
            expressions = (unparse(to_typing(parse(arg))) for arg in args)
        for expression in expressions:
            click.echo(expression)
    except util.StenotypeException as e:
        click.echo(e, err=True)
        exit(1)
