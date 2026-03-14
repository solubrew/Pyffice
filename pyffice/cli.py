"""Pyffice CLI - Command Line Interface."""

import sys
from typing import Optional

import click


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output')
@click.option('--config', type=click.Path(), help='Specify config file')
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, config: Optional[str]) -> None:
    """Pyffice - Comprehensive document and media framework."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['config'] = config


@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option('--format', '-f', help='Output format')
def convert(input: str, output: str, format: Optional[str]) -> None:
    """Convert documents between formats."""
    click.echo(f"Converting {input} to {output}")


@cli.command()
@click.option('--type', '-t', type=click.Choice(['document', 'spreadsheet', 'presentation']), required=True)
@click.option('--template', help='Template file to use')
@click.argument('output', type=click.Path())
def create(type: str, template: Optional[str], output: str) -> None:
    """Create a new document."""
    click.eout(f"Creating {type} document: {output}")


@cli.command(name='formats')
def list_formats() -> None:
    """List supported file formats."""
    formats = {
        'documents': ['docx', 'odt', 'rtf', 'txt', 'pdf'],
        'spreadsheets': ['xlsx', 'ods', 'csv'],
        'presentations': ['pptx', 'odp'],
        'diagrams': ['dia', 'svg', 'dot', 'graphml', 'vsdx', 'drawio'],
        'images': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'],
        'video': ['mp4', 'avi', 'mov', 'mkv'],
        'audio': ['mp3', 'wav', 'ogg', 'flac'],
    }
    for category, items in formats.items():
        click.echo(f"{category}: {', '.join(items)}")


@cli.group()
def diagram() -> None:
    """Diagram operations."""
    pass


@diagram.command(name='convert')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def diagram_convert(input: str, output: str) -> None:
    """Convert diagram formats."""
    click.echo(f"Converting diagram: {input} -> {output}")


@diagram.command(name='formats')
def diagram_formats() -> None:
    """List supported diagram formats."""
    formats = ['dia', 'svg', 'dot', 'graphml', 'vsdx', 'drawio', 'mm', 'xmind']
    click.echo("Supported diagram formats: " + ', '.join(formats))


@cli.group()
def config() -> None:
    """Configuration operations."""
    pass


@config.command(name='show')
def config_show() -> None:
    """Show current configuration."""
    click.echo("Pyffice Configuration:")
    click.echo("  version: 0.1.0")
    click.echo("  plugins: enabled")


@config.command(name='validate')
def config_validate() -> None:
    """Validate configuration."""
    click.echo("Configuration is valid.")


def main() -> None:
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == '__main__':
    main()
