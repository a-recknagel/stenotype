from stenotype.util import StenotypeException


def test_usage(test_cli):
    result = test_cli("?int")
    assert result.exit_code == 0
    assert result.stdout == "typing.Optional[int]\n"


def test_multi_usage(test_cli):
    result = test_cli("?int", "?bool")
    assert result.exit_code == 0
    assert result.stdout == "typing.Optional[int]\n" "typing.Optional[bool]\n"


def test_version(test_cli):
    from stenotype import __version__

    result = test_cli("-v")
    assert result.exit_code == 0
    assert result.stdout == f"stenotype {__version__}\n"


def test_no_args(test_cli):
    result = test_cli()
    assert result.exit_code == 0
    assert result.stderr == "No arguments entered, nothing to do.\n"


def test_shorten_and_check(test_cli):
    result = test_cli("-s", "-c")
    assert result.exit_code == 1
    assert result.stderr == (
        "Flags --shorten and --check can't be used simultaneously.\n"
    )


def test_shorten(test_cli):
    result = test_cli("-s", "typing.Optional[int]")
    assert result.exit_code == 0
    assert result.stdout == "stub inverse function: typing.Optional[int]\n"
    # should be "?int"


def test_parser_exception(test_cli, monkeypatch):
    from stenotype import cli

    def parse_that_fails(*_, **__):
        raise StenotypeException("test message")

    monkeypatch.setattr(cli, "parse", parse_that_fails)

    result = test_cli("?int")
    assert result.exit_code == 1
    assert result.stderr == "test message\n"
