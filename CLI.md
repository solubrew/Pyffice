# Pyffice CLI

## Purpose

Pyffice provides a unified interface across the Microsoft Office ecosystem
— Word, Excel, PowerPoint, Outlook, OneNote, Visio, Project, and SharePoint.
The CLI offers command-line access to the full suite: import/export
between formats, batch document conversion, schema validation, and
template-driven document generation. Use it for scripts, batch jobs, and
automation pipelines that need to programmatically produce or consume Office
files without launching the desktop applications.

## Usage

```bash
pyffice [COMMAND] [OPTIONS]
```

## Global Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable verbose output |
| `-q, --quiet` | Suppress output |
| `--version` | Show version |
| `--help` | Show help message |

## Commands

### document

Work with documents (Word, PDF, RTF, ODT)

```bash
pyffice document open <file>
pyffice document convert <input> <output>
pyffice document info <file>
pyffice document extract <file>
```

### spreadsheet

Work with spreadsheets (Excel, CSV, ODS)

```bash
pyffice spreadsheet open <file>
pyffice spreadsheet create <name>
pyffice spreadsheet convert <input> <output>
pyffice spreadsheet export <file> --format csv
pyffice spreadsheet info <file>
```

### presentation

Work with presentations (PowerPoint, ODP)

```bash
pyffice presentation open <file>
pyffice presentation convert <input> <output>
pyffice presentation info <file>
```

### cad

Process CAD files (STL, OBJ, DWG, DXF, STEP)

```bash
pyffice cad convert <input> <output>
pyffice cad info <file>
pyffice cad validate <file>
pyffice cad repair <file>
```

### image

Process images (PNG, JPG, HEIC, RAW, WebP)

```bash
pyffice image convert <input> <output>
pyffice image resize <file> --width 800 --height 600
pyffice image thumbnail <file>
pyffice image info <file>
pyffice image optimize <file>
```

### video

Process video files

```bash
pyffice video convert <input> <output>
pyffice video info <file>
pyffice video thumbnail <file>
pyffice video extract-audio <file>
```

### audio

Process audio files

```bash
pyffice audio convert <input> <output>
pyffice audio info <file>
pyffice audio trim <file> --start 0 --end 60
pyffice audio extract <file>
```

### diagram

Process diagram files (Draw.io, Graphviz)

```bash
pyffice diagram convert <input> <output>
pyffice diagram validate <file>
pyffice diagram info <file>
pyffice diagram export <file> --format png
```

### chart

Create and process charts

```bash
pyffice chart create <type> --data <data>
pyffice chart export <chart> --output <file>
pyffice chart types
```

### calendar

Manage calendars and events

```bash
pyffice calendar list
pyffice calendar events <date>
pyffice calendar create <name>
pyffice calendar export <calendar>
```

### contact

Manage contacts

```bash
pyffice contact list
pyffice contact search <query>
pyffice contact add <name>
pyffice contact export
```

### email

Manage emails

```bash
pyffice email send --to <recipient> --subject <subject> --body <body>
pyffice email list
pyffice email read <id>
pyffice email attach <file>
```

### database

Work with databases

```bash
pyffice database connect <connection_string>
pyffice database query <sql>
pyffice database tables
pyffice database export <table>
```

### filesystem

Work with filesystems

```bash
pyffice filesystem list <path>
pyffice filesystem sync <source> <target>
pyffice filesystem search <query>
pyffice filesystem info <path>
```

### config

Manage configuration

```bash
pyffice config show
pyffice config set <key> <value>
pyffice config validate
pyffice config reset
```

### update

Manage updates

```bash
pyffice update check
pyffice update install
pyffice update status
pyffice update history
```

### formats

List supported formats

```bash
pyffice formats
pyffice formats --document
pyffice formats --media
pyffice formats --cad
```

### help

Show help information

```bash
pyffice help [command]
```

## Exit Codes

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid arguments |
| `3` | File not found |
| `4` | Permission denied |

## Examples

```bash
# Convert a document to PDF
pyffice document convert report.docx output.pdf

# Create a spreadsheet
pyffice spreadsheet create report.xlsx

# Convert CAD file
pyffice cad convert model.stl model.obj

# Resize an image
pyffice image resize photo.png --width 800 --height 600

# List calendars
pyffice calendar list

# Send an email
pyffice email send --to user@example.com --subject "Hello" --body "Message"

# Check for updates
pyffice update check

# Show configuration
pyffice config show
```

## Configuration File

Pyffice uses `pyffice.yaml` for configuration:

```yaml
version: "1.0"
paths:
  data: "~/.pyffice/data"
  cache: "~/.pyffice/cache"
  logs: "~/.pyffice/logs"
logging:
  level: "INFO"
  file: "~/.pyffice/logs/pyffice.log"
defaults:
  image_format: "png"
  document_format: "pdf"
```
