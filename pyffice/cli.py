"""Pyffice CLI - Command Line Interface."""

import sys
import os
from pathlib import Path
from typing import Optional

import click


# Import all modules for CLI coverage.
# T-NEW-044: previously this was `from pyffice import (...)` with 25
# subpackage names that pyffice/__init__.py never re-exported (the
# only thing it exports is __version__/__version_info__ — T-NEW-051
# covers the rest). Switched to explicit submodule imports so the
# CLI can at least start. Many of these modules have broken
# transitive imports (e.g. pyffice.email.email references a
# non-existent pyffice.text.messages module; pyffice.reports.reports
# references a non-existent pyffice.text.text module). Each is
# wrapped in try/except so one broken submodule doesn't crash the
# whole CLI; this matches the spirit of the original `import ...`
# block (which only imported names for the side effect of making
# modules available) but reports what failed so it's visible.
def _safe_import(module_name: str, attr: str) -> object:
    """Import a submodule; return None if it or its deps fail."""
    try:
        mod = __import__(module_name, fromlist=[attr])
        return getattr(mod, attr, None)
    except (ImportError, AttributeError, ModuleNotFoundError) as exc:  # noqa: BLE001 - reported, not raised
        print(f"[pyffice.cli] skipping {module_name}.{attr}: {exc}", file=sys.stderr)
        return None


analytics = _safe_import("pyffice.analytics", "sources")
audio_module = _safe_import("pyffice.audio", "audio_export")
calendars_module = _safe_import("pyffice.calendars", "calendars")
cam_module = _safe_import("pyffice.cam", "cam")
charts_module = _safe_import("pyffice.charts", "charts")
contacts_module = _safe_import("pyffice.contacts", "contacts")
databases_module = _safe_import("pyffice.databases", "databases")
diagrams_module = _safe_import("pyffice.diagrams", "diagrams")
email_module = _safe_import("pyffice.email", "email")
filesystems_module = _safe_import("pyffice.filesystems", "filesystems")
forms_module = _safe_import("pyffice.forms", "forms")
images_module = _safe_import("pyffice.images", "images")
items_module = _safe_import("pyffice.items", "items")
matrix_module = _safe_import("pyffice.matrix", "matrix")
notebooks_module = _safe_import("pyffice.notebooks", "notebooks")
ports_module = _safe_import("pyffice.ports", "ports")
presentation_module = _safe_import("pyffice.presentation", "presentation")
projects_module = _safe_import("pyffice.projects", "projects")
reports_module = _safe_import("pyffice.reports", "reports")
script_module = _safe_import("pyffice.script", "script")
socials_module = _safe_import("pyffice.socials", "socials")
tags_module = _safe_import("pyffice.tags", "tags")
text_module = _safe_import("pyffice.text", "textdoc")
updates_module = _safe_import("pyffice.updates", "updates")
video_module = _safe_import("pyffice.video", "video_export")
web_module = _safe_import("pyffice.web", "web")
workflows_module = _safe_import("pyffice.workflows", "workflows")

from pyffice import PyfficeCodex
from pyffice.document import PyfficeDocument

# T-NEW-044: keep the legacy alias so the rest of this file
# (which references `Pyffice`) keeps compiling. The real class
# is PyfficeCodex.
Pyffice = PyfficeCodex


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--quiet", "-q", is_flag=True, help="Suppress output")
@click.option("--config", type=click.Path(), help="Specify config file")
@click.pass_context
def cli(ctx: click.Context, verbose: bool, quiet: bool, config: Optional[str]) -> None:
    """Pyffice - Comprehensive document and media framework."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["config"] = config
    # Initialize Pyffice instance
    ctx.obj["pyffice"] = Pyffice()


# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", help="Output format")
@click.option("--template", "-t", help="Template to use")
@click.pass_context
def document_convert(
    ctx: click.Context, input: str, output: str, format: Optional[str], template: Optional[str]
) -> None:
    """Convert documents between formats.

    INPUT: Source document path
    OUTPUT: Destination document path
    """
    pyffice = ctx.obj.get("pyffice")
    try:
        doc = PyfficeDocument()
        doc.file_open(input)
        doc.save(output, syntax=format or "pdf")
        click.echo(f"✓ Converted document: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def document_info(ctx: click.Context, input: str) -> None:
    """Show document information.

    INPUT: Document path to inspect
    """
    try:
        doc = PyfficeDocument()
        doc.file_open(input)
        info = doc.to_dict()
        click.echo(f"Document: {input}")
        click.echo(f"  Name: {info.get('name', 'N/A')}")
        click.echo(f"  Type: {info.get('document_type', 'N/A')}")
        click.echo(f"  Version: {info.get('version', 0)}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# SPREADSHEET COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", type=click.Choice(["xlsx", "csv", "ods"]), help="Output format")
@click.pass_context
def spreadsheet_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert spreadsheets between formats.

    INPUT: Source spreadsheet path
    OUTPUT: Destination spreadsheet path
    """
    from pyffice.spreadsheet.spreadsheet import PyfficeMatrix

    try:
        wb = PyfficeMatrix()
        wb.file_import(input)
        wb.save(output, syntax=format or "excel")
        click.echo(f"✓ Converted spreadsheet: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def spreadsheet_info(ctx: click.Context, input: str) -> None:
    """Show spreadsheet information.

    INPUT: Spreadsheet path to inspect
    """
    from pyffice.spreadsheet.spreadsheet import PyfficeMatrix

    try:
        wb = PyfficeMatrix()
        wb.file_import(input)
        sheets = wb.sheets.keys() if wb.sheets else []
        click.echo(f"Spreadsheet: {input}")
        click.echo(f"  Sheets: {len(list(sheets))}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# PRESENTATION COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", type=click.Choice(["pptx", "odp"]), help="Output format")
@click.pass_context
def presentation_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert presentations between formats.

    INPUT: Source presentation path
    OUTPUT: Destination presentation path
    """
    from pyffice.presentation.presentation import PyfficePresentation

    try:
        pres = PyfficePresentation()
        pres.file_import(input)
        pres.save(output, syntax=format or "pptx")
        click.echo(f"✓ Converted presentation: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def diagram() -> None:
    """Diagram operations."""
    return None


@diagram.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", help="Output format")
@click.pass_context
def diagram_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert diagram formats.

    INPUT: Source diagram file
    OUTPUT: Destination diagram file
    """
    from pyffice.diagrams.diagrams import PyfficeDiagram

    try:
        sketch = PyfficeDiagram()
        sketch.load(input)
        sketch.save(output, format=format or "svg")
        click.echo(f"✓ Converted diagram: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@diagram.command(name="validate")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def diagram_validate(ctx: click.Context, input: str) -> None:
    """Validate diagram file.

    INPUT: Diagram file to validate
    """
    from pyffice.diagrams.formats import DiaConverter

    try:
        converter = DiaConverter({})
        converter.validate(input)
        click.echo(f"✓ Valid diagram: {input}")
    except (OSError, ValueError, AttributeError, TypeError) as e:
        click.echo(f"Invalid: {e}", err=True)


@diagram.command(name="info")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def diagram_info(ctx: click.Context, input: str) -> None:
    """Show diagram information.

    INPUT: Diagram file to inspect
    """
    from pyffice.diagrams.diagrams import PyfficeDiagram

    try:
        sketch = PyfficeDiagram()
        sketch.load(input)
        info = sketch.to_dict()
        click.echo(f"Diagram: {input}")
        click.echo(f"  Elements: {len(info.get('elements', []))}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def image() -> None:
    """Image operations."""
    return None


@image.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option(
    "--format", "-f", type=click.Choice(["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"]), help="Output format"
)
@click.pass_context
def image_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert images between formats.

    INPUT: Source image path
    OUTPUT: Destination image path
    """
    from pyffice.images.images import PyfficeImage

    try:
        img = PyfficeImage()
        img.load(input)
        img.convert(output, format=format or "png")
        click.echo(f"✓ Converted image: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@image.command(name="resize")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--width", "-w", type=int, help="Target width")
@click.option("--height", "-h", type=int, help="Target height")
@click.pass_context
def image_resize(ctx: click.Context, input: str, output: str, width: Optional[int], height: Optional[int]) -> None:
    """Resize an image.

    INPUT: Source image path
    OUTPUT: Destination image path
    """
    from pyffice.images.images import PyfficeImage

    try:
        img = PyfficeImage()
        img.load(input)
        img.resize(width or 800, height or 600)
        img.save(output)
        click.echo(f"✓ Resized image: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@image.command(name="info")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def image_info(ctx: click.Context, input: str) -> None:
    """Show image information.

    INPUT: Image path to inspect
    """
    from pyffice.images.images import PyfficeImage

    try:
        img = PyfficeImage()
        img.load(input)
        info = img.to_dict()
        click.echo(f"Image: {input}")
        click.echo(f"  Size: {info.get('width', '?')}x{info.get('height', '?')}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# VIDEO COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def video() -> None:
    """Video operations."""
    return None


@video.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", type=click.Choice(["mp4", "avi", "mov", "mkv"]), help="Output format")
@click.pass_context
def video_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert videos between formats.

    INPUT: Source video path
    OUTPUT: Destination video path
    """
    from pyffice.video.video import PyfficeVideo

    try:
        vid = PyfficeVideo()
        vid.load(input)
        vid.convert(output, format=format or "mp4")
        click.echo(f"✓ Converted video: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@video.command(name="info")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def video_info(ctx: click.Context, input: str) -> None:
    """Show video information.

    INPUT: Video path to inspect
    """
    from pyffice.video.video import PyfficeVideo

    try:
        vid = PyfficeVideo()
        vid.load(input)
        info = vid.to_dict()
        click.echo(f"Video: {input}")
        click.echo(f"  Duration: {info.get('duration', 'N/A')}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# AUDIO COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def audio() -> None:
    """Audio operations."""
    return None


@audio.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", type=click.Choice(["mp3", "wav", "ogg", "flac"]), help="Output format")
@click.pass_context
def audio_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert audio between formats.

    INPUT: Source audio path
    OUTPUT: Destination audio path
    """
    from pyffice.audio.audio import PyfficeAudio

    try:
        aud = PyfficeAudio()
        aud.load(input)
        aud.convert(output, format=format or "mp3")
        click.echo(f"✓ Converted audio: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@audio.command(name="info")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def audio_info(ctx: click.Context, input: str) -> None:
    """Show audio information.

    INPUT: Audio path to inspect
    """
    from pyffice.audio.audio import PyfficeAudio

    try:
        aud = PyfficeAudio()
        aud.load(input)
        info = aud.to_dict()
        click.echo(f"Audio: {input}")
        click.echo(f"  Duration: {info.get('duration', 'N/A')}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAD COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def cad() -> None:
    """CAD operations."""
    return None


@cad.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.pass_context
def cad_convert(ctx: click.Context, input: str, output: str) -> None:
    """Convert CAD formats.

    INPUT: Source CAD file
    OUTPUT: Destination CAD file
    """
    from pyffice.cad.cad import PyfficeCAD

    try:
        cad = PyfficeCAD()
        cad.load(input)
        cad.convert(output)
        click.echo(f"✓ Converted CAD: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@cad.command(name="info")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def cad_info(ctx: click.Context, input: str) -> None:
    """Show CAD file information.

    INPUT: CAD file to inspect
    """
    from pyffice.cad.cad import PyfficeCAD

    try:
        cad = PyfficeCAD()
        cad.load(input)
        info = cad.to_dict()
        click.echo(f"CAD: {input}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CHART COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def chart() -> None:
    """Chart operations."""
    return None


@chart.command(name="create")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--type", "-t", type=click.Choice(["bar", "line", "pie", "scatter"]), help="Chart type")
@click.pass_context
def chart_create(ctx: click.Context, input: str, output: str, type: str) -> None:
    """Create a chart from data.

    INPUT: Data file (CSV, Excel)
    OUTPUT: Output chart file
    """
    from pyffice.charts.charts import PyfficeChart

    try:
        chart = PyfficeChart()
        chart.load_data(input)
        chart.set_type(type or "bar")
        chart.save(output)
        click.echo(f"✓ Created chart: {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CALENDAR COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def calendar() -> None:
    """Calendar operations."""
    return None


@calendar.command(name="list")
@click.option("--from", "from_date", help="Start date (YYYY-MM-DD)")
@click.option("--to", "to_date", help="End date (YYYY-MM-DD)")
@click.pass_context
def calendar_list(ctx: click.Context, from_date: Optional[str], to_date: Optional[str]) -> None:
    """List calendar events.

    FROM: Start date
    TO: End date
    """
    from pyffice.calendars.calendars import PyfficeCalendar

    try:
        cal = PyfficeCalendar()
        events = cal.get_events(from_date, to_date)
        click.echo(f"Calendar events ({len(events)}):")
        for event in events:
            click.echo(f"  - {event.get('title', 'Untitled')}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONTACT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def contact() -> None:
    """Contact operations."""
    return None


@contact.command(name="list")
@click.pass_context
def contact_list(ctx: click.Context) -> None:
    """List contacts."""
    from pyffice.contacts.contacts import PyfficeContacts

    try:
        contacts = PyfficeContacts()
        all_contacts = contacts.get_all()
        click.echo(f"Contacts ({len(all_contacts)}):")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@contact.command(name="search")
@click.argument("query")
@click.pass_context
def contact_search(ctx: click.Context, query: str) -> None:
    """Search contacts.

    QUERY: Search term
    """
    from pyffice.contacts.contacts import PyfficeContacts

    try:
        contacts = PyfficeContacts()
        results = contacts.search(query)
        click.echo(f"Found {len(results)} contacts:")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# EMAIL COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def email_cmd() -> None:
    """Email operations."""
    return None


@email_cmd.command(name="send")
@click.option("--to", required=True, help="Recipient address")
@click.option("--subject", required=True, help="Email subject")
@click.option("--body", help="Email body")
@click.option("--attach", multiple=True, help="Attachment files")
@click.pass_context
def email_send(ctx: click.Context, to: str, subject: str, body: Optional[str], attach: tuple) -> None:
    """Send an email.

    TO: Recipient email address
    SUBJECT: Email subject
    BODY: Email body text
    """
    from pyffice.email.email import PyfficeEmail

    try:
        email = PyfficeEmail()
        email.send(to, subject, body or "", list(attach))
        click.echo(f"✓ Sent email to {to}: {subject}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def database() -> None:
    """Database operations."""
    return None


@database.command(name="connect")
@click.argument("connection_string")
@click.pass_context
def database_connect(ctx: click.Context, connection_string: str) -> None:
    """Connect to a database.

    CONNECTION_STRING: Database connection string
    """
    from pyffice.databases.databases import PyfficeDatabase

    try:
        db = PyfficeDatabase()
        db.connect(connection_string)
        click.echo(f"✓ Connected to database")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@database.command(name="query")
@click.argument("query")
@click.pass_context
def database_query(ctx: click.Context, query: str) -> None:
    """Execute a database query.

    QUERY: SQL query to execute
    """
    from pyffice.databases.databases import PyfficeDatabase

    try:
        db = PyfficeDatabase()
        results = db.execute(query)
        click.echo(f"✓ Executed query: {query[:50]}...")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# FILESYSTEM COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def filesystem() -> None:
    """Filesystem operations."""
    return None


@filesystem.command(name="list")
@click.argument("path", type=click.Path(exists=True))
@click.option("--recursive", "-r", is_flag=True, help="List recursively")
@click.pass_context
def filesystem_list(ctx: click.Context, path: str, recursive: bool) -> None:
    """List filesystem contents.

    PATH: Directory path to list
    """
    from pyffice.filesystems.filesystems import PyfficeFileSystem

    try:
        fs = PyfficeFileSystem()
        items = fs.list(path, recursive=recursive)
        click.echo(f"Items in {path}: {len(items)}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@filesystem.command(name="sync")
@click.argument("source", type=click.Path(exists=True))
@click.argument("destination", type=click.Path())
@click.pass_context
def filesystem_sync(ctx: click.Context, source: str, destination: str) -> None:
    """Sync directories.

    SOURCE: Source directory
    DESTINATION: Destination directory
    """
    from pyffice.filesystems.filesystems import PyfficeFileSystem

    try:
        fs = PyfficeFileSystem()
        fs.sync(source, destination)
        click.echo(f"✓ Synced: {source} -> {destination}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# ANALYTICS COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def analytics() -> None:
    """Analytics operations."""
    return None


@analytics.command(name="report")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.pass_context
def analytics_report(ctx: click.Context, input: str, output: str) -> None:
    """Generate analytics report.

    INPUT: Data file
    OUTPUT: Report output path
    """
    from pyffice.analytics.sources import PyfficeAnalytics

    try:
        an = PyfficeAnalytics()
        an.generate_report(input, output)
        click.echo(f"✓ Generated report: {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# PROJECT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def project() -> None:
    """Project operations."""
    return None


@project.command(name="create")
@click.argument("name")
@click.argument("output", type=click.Path())
@click.pass_context
def project_create(ctx: click.Context, name: str, output: str) -> None:
    """Create a new project.

    NAME: Project name
    OUTPUT: Output directory
    """
    from pyffice.projects.paxn import PyfficeProject

    try:
        proj = PyfficeProject()
        proj.create(name, output)
        click.echo(f"✓ Created project: {name}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def config() -> None:
    """Configuration operations."""
    return None


@config.command(name="show")
@click.pass_context
def config_show(ctx: click.Context) -> None:
    """Show current configuration."""
    from pyffice.config.config import PyfficeConfig

    try:
        cfg = PyfficeConfig()
        click.echo("Pyffice Configuration:")
        click.echo(f"  version: {cfg.get('version', '0.1.0')}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@config.command(name="validate")
@click.pass_context
def config_validate(ctx: click.Context) -> None:
    """Validate configuration."""
    from pyffice.config.config import PyfficeConfig

    try:
        cfg = PyfficeConfig()
        if cfg.validate():
            click.echo("✓ Configuration is valid.")
    except (OSError, ValueError, AttributeError, TypeError) as e:
        click.echo(f"Invalid: {e}", err=True)


@config.command(name="set")
@click.argument("key")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str) -> None:
    """Set configuration value.

    KEY: Configuration key
    VALUE: Configuration value
    """
    from pyffice.config.config import PyfficeConfig

    try:
        cfg = PyfficeConfig()
        cfg.set(key, value)
        click.echo(f"✓ Set {key} = {value}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# FORMS COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def form() -> None:
    """Form operations."""
    return None


@form.command(name="create")
@click.argument("output", type=click.Path())
@click.option("--title", help="Form title")
@click.pass_context
def form_create(ctx: click.Context, output: str, title: Optional[str]) -> None:
    """Create a new form.

    OUTPUT: Output file path
    """
    from pyffice.forms.forms import PyfficeForm

    try:
        frm = PyfficeForm()
        frm.create(title or "Untitled")
        frm.save(output)
        click.echo(f"✓ Created form: {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@form.command(name="validate")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def form_validate(ctx: click.Context, input: str) -> None:
    """Validate a form.

    INPUT: Form file to validate
    """
    from pyffice.forms.forms import PyfficeForm

    try:
        frm = PyfficeForm()
        frm.load(input)
        if frm.validate():
            click.echo(f"✓ Valid form: {input}")
    except (OSError, ValueError, AttributeError, TypeError) as e:
        click.echo(f"Invalid: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# NOTEBOK COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def notebook() -> None:
    """Notebook operations."""
    return None


@notebook.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.pass_context
def notebook_convert(ctx: click.Context, input: str, output: str) -> None:
    """Convert notebook formats.

    INPUT: Source notebook file
    OUTPUT: Destination notebook file
    """
    from pyffice.notebooks.notebooks import PyfficeNotebook

    try:
        nb = PyfficeNotebook()
        nb.load(input)
        nb.save(output)
        click.echo(f"✓ Converted notebook: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# REPORT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def report() -> None:
    """Report operations."""
    return None


@report.command(name="generate")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.pass_context
def report_generate(ctx: click.Context, input: str, output: str) -> None:
    """Generate a report.

    INPUT: Data file
    OUTPUT: Report output path
    """
    from pyffice.reports.reports import PyfficeReport

    try:
        rep = PyfficeReport()
        rep.generate(input, output)
        click.echo(f"✓ Generated report: {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# SOCIAL COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def social() -> None:
    """Social operations."""
    return None


@social.command(name="post")
@click.argument("message")
@click.option("--platform", "-p", help="Target platform")
@click.pass_context
def social_post(ctx: click.Context, message: str, platform: Optional[str]) -> None:
    """Post to social media.

    MESSAGE: Message to post
    """
    from pyffice.socials.socials import PyfficeSocial

    try:
        soc = PyfficeSocial()
        soc.post(message, platform)
        click.echo(f"✓ Posted to social media")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAG COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def tag() -> None:
    """Tag operations."""
    return None


@tag.command(name="list")
@click.argument("input", type=click.Path(exists=True))
@click.pass_context
def tag_list(ctx: click.Context, input: str) -> None:
    """List tags in a file.

    INPUT: File to list tags from
    """
    from pyffice.tags.manager import PyfficeTagManager

    try:
        mgr = PyfficeTagManager()
        tags = mgr.list_tags(input)
        click.echo(f"Tags in {input}: {len(tags)}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def text() -> None:
    """Text operations."""
    return None


@text.command(name="convert")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", help="Output format")
@click.pass_context
def text_convert(ctx: click.Context, input: str, output: str, format: Optional[str]) -> None:
    """Convert text documents.

    INPUT: Source text file
    OUTPUT: Destination text file
    """
    from pyffice.items.text import PyfficeText

    try:
        txt = PyfficeText()
        txt.load(input)
        txt.save(output, format=format or "txt")
        click.echo(f"✓ Converted text: {input} -> {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# UPDATE COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def update() -> None:
    """Update operations."""
    return None


@update.command(name="check")
@click.pass_context
def update_check(ctx: click.Context) -> None:
    """Check for updates."""
    from pyffice.updates.updates import PyfficeUpdates

    try:
        up = PyfficeUpdates()
        if up.check():
            click.echo("Updates available!")
        else:
            click.echo("No updates available.")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@update.command(name="install")
@click.argument("package")
@click.pass_context
def update_install(ctx: click.Context, package: str) -> None:
    """Install an update.

    PACKAGE: Package name to update
    """
    from pyffice.updates.updates import PyfficeUpdates

    try:
        up = PyfficeUpdates()
        up.install(package)
        click.echo(f"✓ Installed update: {package}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# WEB COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def web() -> None:
    """Web operations."""
    return None


@web.command(name="fetch")
@click.argument("url")
@click.argument("output", type=click.Path())
@click.pass_context
def web_fetch(ctx: click.Context, url: str, output: str) -> None:
    """Fetch a web page.

    URL: URL to fetch
    OUTPUT: Output file path
    """
    from pyffice.web.web import PyfficeWeb

    try:
        wb = PyfficeWeb()
        wb.fetch(url, output)
        click.echo(f"✓ Fetched: {url}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@web.command(name="parse")
@click.argument("input", type=click.Path(exists=True))
@click.option("--format", "-f", help="Output format")
@click.pass_context
def web_parse(ctx: click.Context, input: str, format: Optional[str]) -> None:
    """Parse web content.

    INPUT: Input file
    """
    from pyffice.web.web import PyfficeWeb

    try:
        wb = PyfficeWeb()
        data = wb.parse(input)
        click.echo(f"✓ Parsed: {input}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOW COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def workflow() -> None:
    """Workflow operations."""
    return None


@workflow.command(name="run")
@click.argument("workflow_file", type=click.Path(exists=True))
@click.pass_context
def workflow_run(ctx: click.Context, workflow_file: str) -> None:
    """Run a workflow.

    WORKFLOW_FILE: Workflow definition file
    """
    from pyffice.workflows.workflows import PyfficeWorkflow

    try:
        wf = PyfficeWorkflow()
        wf.load(workflow_file)
        wf.run()
        click.echo(f"✓ Ran workflow: {workflow_file}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


@workflow.command(name="list")
@click.pass_context
def workflow_list(ctx: click.Context) -> None:
    """List available workflows."""
    from pyffice.workflows.workflows import PyfficeWorkflow

    try:
        wf = PyfficeWorkflow()
        workflows = wf.list()
        click.echo(f"Available workflows: {len(workflows)}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# CAM COMMANDS
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def cam() -> None:
    """CAM operations."""
    return None


@cam.command(name="generate")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.pass_context
def cam_generate(ctx: click.Context, input: str, output: str) -> None:
    """Generate CNC code.

    INPUT: CAD file
    OUTPUT: CNC output file
    """
    # Use the canonical cad/ implementation rather than the
    # parallel cam/ dataclass module (see review: PyfficeCAM
    # duplicated across pyffice/cam/cam.py and
    # pyffice/cad/cam.py).
    from pyffice.cad.gcode import PyfficeGCode

    try:
        gcode = PyfficeGCode()
        gcode.file_import(input)
        gcode.save_gcode(output)
        click.echo(f"✓ Generated CNC code: {output}")
    except (OSError, ValueError, KeyError, AttributeError, TypeError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# FORMAT LISTING
# ══════════════════════════════════════════════════════════════════════════════


@cli.command(name="formats")
def list_formats() -> None:
    """List supported file formats."""
    formats = {
        "documents": ["docx", "odt", "rtf", "txt", "pdf"],
        "spreadsheets": ["xlsx", "ods", "csv"],
        "presentations": ["pptx", "odp"],
        "diagrams": ["dia", "svg", "dot", "graphml", "vsdx", "drawio"],
        "images": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"],
        "video": ["mp4", "avi", "mov", "mkv"],
        "audio": ["mp3", "wav", "ogg", "flac"],
    }
    for category, items in formats.items():
        click.echo(f"{category}: {', '.join(items)}")


# ══════════════════════════════════════════════════════════════════════════════
# CLOUD COMMANDS (T-NEW-070)
# ══════════════════════════════════════════════════════════════════════════════


@cli.group()
def cloud() -> None:
    """Cloud storage operations (Google Drive, Dropbox)."""
    pass


@cloud.command(name="auth")
@click.option("--service", "-s", required=True, type=click.Choice(["google", "dropbox"]), help="Cloud service")
@click.option("--credential-file", "-c", type=click.Path(exists=True), help="Path to credential JSON file")
@click.option("--token", "-t", help="Raw access token")
def cloud_auth(service: str, credential_file: Optional[str], token: Optional[str]) -> None:
    """Authenticate with a cloud service."""
    import json as _json
    from pyffice.ports.cloud_ports import PyfficePortGoogleDrive, PyfficePortDropbox

    creds = {}
    if credential_file:
        with open(credential_file) as f:
            creds = _json.load(f)
    elif token:
        creds = {"access_token": token}
    else:
        click.echo("Error: --credential-file or --token required", err=True)
        return

    try:
        if service == "google":
            port = PyfficePortGoogleDrive()
            port.authenticate(creds)
            click.echo(f"✓ Google Drive authenticated")
        elif service == "dropbox":
            port = PyfficePortDropbox()
            port.authenticate(creds)
            click.echo(f"✓ Dropbox authenticated")
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cloud.command(name="list")
@click.option("--service", "-s", required=True, type=click.Choice(["google", "dropbox"]))
@click.option("--credential-file", "-c", required=True, type=click.Path(exists=True))
@click.option("--folder", "-f", default=None, help="Folder ID or path")
def cloud_list(service: str, credential_file: str, folder: Optional[str]) -> None:
    """List files in a cloud folder."""
    import json as _json
    from pyffice.ports.cloud_ports import PyfficePortGoogleDrive, PyfficePortDropbox

    with open(credential_file) as f:
        creds = _json.load(f)

    try:
        if service == "google":
            port = PyfficePortGoogleDrive()
            port.authenticate(creds)
            files = port.list_files(folder)
        elif service == "dropbox":
            port = PyfficePortDropbox()
            port.authenticate(creds)
            files = port.list_files(folder)
        for f_info in files:
            click.echo(f"  {f_info['id']:<40} {f_info['name']}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cloud.command(name="pull")
@click.option("--service", "-s", required=True, type=click.Choice(["google", "dropbox"]))
@click.option("--credential-file", "-c", required=True, type=click.Path(exists=True))
@click.option("--file-id", "-i", required=True, help="Cloud file ID or path")
@click.option("--output", "-o", required=True, type=click.Path(), help="Local output path")
def cloud_pull(service: str, credential_file: str, file_id: str, output: str) -> None:
    """Download a file from cloud storage."""
    import json as _json
    from pyffice.ports.cloud_ports import PyfficePortGoogleDrive, PyfficePortDropbox

    with open(credential_file) as f:
        creds = _json.load(f)

    try:
        if service == "google":
            port = PyfficePortGoogleDrive()
            port.authenticate(creds)
            port.download_file(file_id, output)
        elif service == "dropbox":
            port = PyfficePortDropbox()
            port.authenticate(creds)
            port.download_file(file_id, output)
        click.echo(f"✓ Downloaded {file_id} -> {output}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cloud.command(name="push")
@click.option("--service", "-s", required=True, type=click.Choice(["google", "dropbox"]))
@click.option("--credential-file", "-c", required=True, type=click.Path(exists=True))
@click.option("--file", "-f", required=True, type=click.Path(exists=True), help="Local file to upload")
@click.option("--folder-id", default=None, help="Cloud destination folder ID")
def cloud_push(service: str, credential_file: str, file: str, folder_id: Optional[str]) -> None:
    """Upload a file to cloud storage."""
    import json as _json
    from pyffice.ports.cloud_ports import PyfficePortGoogleDrive, PyfficePortDropbox

    with open(credential_file) as f:
        creds = _json.load(f)

    try:
        if service == "google":
            port = PyfficePortGoogleDrive()
            port.authenticate(creds)
            result = port.upload_file(file, folder_id)
        elif service == "dropbox":
            port = PyfficePortDropbox()
            port.authenticate(creds)
            result = port.upload_file(file, folder_id)
        click.echo(f"✓ Uploaded {file} -> {result.get('id', 'unknown')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════


def main() -> None:
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
