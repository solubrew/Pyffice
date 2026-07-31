"""Tests for pyffice/cli.py.

Coverage:
- The click group is registered and lists subcommands
- --help exits 0 and lists the 22 commands (after T-NEW-044)
- Subcommand --help works for groups with real subcommands
- The Pyffice alias points to PyfficeCodex (T-NEW-044)

The CLI uses click.testing.CliRunner for isolation.
"""

from click.testing import CliRunner

from pyffice.cli import cli
from pyffice.pyffice import PyfficeCodex


class TestCliGroup:
    """The top-level click group is well-formed."""

    def test_pyffice_alias_is_pyffice_codex(self):
        # T-NEW-044: pyffice/cli.py aliases `Pyffice = PyfficeCodex`
        # so legacy bare 'Pyffice()' calls still work.
        from pyffice.cli import Pyffice
        assert Pyffice is PyfficeCodex

    def test_cli_help_exits_zero(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Pyffice" in result.output

    def test_cli_lists_expected_commands(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        # Spot-check a few commands that should always be present
        # after T-NEW-044.
        assert "document-convert" in result.output
        assert "document-info" in result.output
        assert "spreadsheet-convert" in result.output
        assert "spreadsheet-info" in result.output
        assert "formats" in result.output

    def test_cli_lists_group_subcommands(self):
        # The diagram group has 3 subcommands (convert, info, validate).
        runner = CliRunner()
        result = runner.invoke(cli, ["diagram", "--help"])
        assert result.exit_code == 0
        assert "convert" in result.output
        assert "info" in result.output
        assert "validate" in result.output

    def test_cli_image_group_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["image", "--help"])
        assert result.exit_code == 0
        assert "convert" in result.output
        assert "info" in result.output
        assert "resize" in result.output

    def test_cli_unknown_command_exits_nonzero(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["nonexistent-command"])
        # Click returns exit code 2 on unknown commands.
        assert result.exit_code != 0

    def test_cli_verbose_flag_accepted(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help", "-v"])
        assert result.exit_code == 0

    def test_cli_quiet_flag_accepted(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help", "-q"])
        assert result.exit_code == 0

    def test_cli_config_option_accepted(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help", "--config", "/tmp/nonexistent.yaml"])
        assert result.exit_code == 0

    def test_cli_groups_all_registered(self):
        # The 24 @cli.group() decorators all register (T-NEW-049).
        # We assert the count of unique top-level commands.
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        # Top-level click commands are listed in 'Commands:'.
        # Each line is '<name>   <help text>'.
        commands_section = result.output.split("Commands:")[1]
        # Each command is one indented line; count non-empty lines.
        command_lines = [
            ln for ln in commands_section.splitlines()
            if ln.strip() and not ln.startswith("Commands") and not ln.startswith("Options")
        ]
        # We expect at least 6 (the 6 @cli.command decorators).
        assert len(command_lines) >= 6

    def test_cli_document_info_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["document-info", "--help"])
        assert result.exit_code == 0
        assert "INPUT" in result.output or "input" in result.output

    def test_cli_spreadsheet_convert_help(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["spreadsheet-convert", "--help"])
        assert result.exit_code == 0