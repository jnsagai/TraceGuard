from typer.testing import CliRunner

from traceguard.cli import app


def test_cli_help_runs() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Deterministic requirements" in result.output


def test_cli_check_runs() -> None:
    result = CliRunner().invoke(
        app,
        ["check", "--project", "examples/braking_project/traceguard.yaml"],
    )

    assert result.exit_code == 0
    assert "Wrote evidence" in result.output
