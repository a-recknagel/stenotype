import pytest
from click.testing import CliRunner

from stenotype import cli


@pytest.fixture
def test_cli(monkeypatch):
    # patch out logger setup
    monkeypatch.setattr(cli.util, "setup_logging", lambda x: None)
    return lambda *args: CliRunner(mix_stderr=False).invoke(cli.cli, args=args)


def pytest_addoption(parser):
    """Add a custom option to pytest."""
    parser.addoption(
        "--mypy",
        action="store_true",
        dest="mypy",
        default=False,
        help="Enable tests that ensure mypy and stenotype interoperability.",
    )


def pytest_configure(config):
    """Ensure that tests that rely on mypy run iff the --mypy flag is present.

    Running ``pytest`` by itself does not invoke the mypy tests. Similarly,
    running ``pytest --mypy`` does not invoke the unit tests. This way, we
    can let them run as separate stages in the CI.
    """
    if config.option.mypy:
        setattr(config.option, "markexpr", "mypy")
    else:
        setattr(config.option, "markexpr", "not mypy")
