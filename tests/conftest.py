import pytest
from click.testing import CliRunner

from stenotype import cli


@pytest.fixture
def test_cli(monkeypatch):
    # don't run logger setup
    monkeypatch.setattr(cli.util, "setup_logging", lambda x: None)
    return lambda *args: CliRunner(mix_stderr=False).invoke(cli.cli, args=args)
