# CLI Documentation

Pyffice Command Line Interface

## Document Commands

```bash
# Convert documents
pyffice document convert <input> <output>
pyffice document info <file>

# Supported formats
# Input: docx, odt, rtf, txt, md, html, pdf, latex
# Output: pdf, docx, odt, html, md, tex
```

## Spreadsheet Commands

```bash
# Convert spreadsheets
pyffice spreadsheet convert <input> <output>
pyffice spreadsheet info <file>

# Supported formats
# Input: xlsx, xls, csv, ods, tsv
# Output: xlsx, csv, ods, tsv, html
```

## Presentation Commands

```bash
# Convert presentations
pyffice presentation convert <input> <output>
pyffice presentation info <file>

# Supported formats
# Input: pptx, ppt, odp, key
# Output: pdf, pptx, odp, html
```

## Diagram Commands

```bash
# Convert diagrams
pyffice diagram convert <input> <output>
pyffice diagram validate <file>
pyffice diagram info <file>

# Supported formats
# Input: svg, png, visio, dia, drawio
# Output: svg, png, pdf, eps
```

## Image Commands

```bash
# Image operations
pyffice image convert <input> <output>
pyffice image resize <input> --width 800 --height 600
pyffice image info <file>

# Supported formats
# Input: png, jpg, jpeg, gif, bmp, webp, tiff, heic, svg
# Output: png, jpg, webp, gif, bmp, tiff
```

## Video Commands

```bash
# Video operations
pyffice video convert <input> <output> --codec h264
pyffice video info <file>
pyffice video thumbnail <input> --time 00:01:00

# Supported formats
# Input: mp4, avi, mkv, mov, wmv, flv, webm
# Output: mp4, webm, gif, avi, mkv
```

## Audio Commands

```bash
# Audio operations
pyffice audio convert <input> <output>
pyffice audio info <file>
pyffice audio trim <input> --start 0 --end 60

# Supported formats
# Input: mp3, wav, flac, aac, ogg, m4a, wma
# Output: mp3, wav, flac, ogg, aac
```

## CAD Commands

```bash
# CAD operations
pyffice cad convert <input> <output>
pyffice cad info <file>

# Supported formats
# Input: dxf, dwg, svg, pdf
# Output: dxf, svg, pdf
```

## Chart Commands

```bash
# Create charts
pyffice chart create --type bar --data data.csv --output chart.png
pyffice chart create --type line --data data.csv --output chart.png
pyffice chart create --type pie --data data.csv --output chart.png

# Chart types: bar, line, pie, scatter, area, histogram
```

## Calendar Commands

```bash
# Calendar operations
pyffice calendar list
pyffice calendar list --from 2025-01-01 --to 2025-12-31
pyffice calendar add --title "Meeting" --start 2025-05-25T10:00 --end 2025-05-25T11:00
pyffice calendar export --format ics

# Supported formats
# Input: ics, vcs, csv
# Output: ics, csv, json
```

## Contact Commands

```bash
# Contact operations
pyffice contact list
pyffice contact search "John Doe"
pyffice contact add --name "John Doe" --email john@example.com --phone "+1234567890"
pyffice contact export --format vcf

# Supported formats
# Input: vcf, csv, ldif
# Output: vcf, csv, json
```

## Email Commands

```bash
# Email operations
pyffice email send --to recipient@example.com --subject "Hello" --body "Message"
pyffice email send --to recipient@example.com --subject "Hello" --file attachment.pdf
pyffice email list --folder INBOX
pyffice email read --id 123

# Supported formats
# SMTP/IMAP integration
# Attachments: any file type
```

## Database Commands

```bash
# Database operations
pyffice database connect --type sqlite --path database.db
pyffice database query "SELECT * FROM users"
pyffice database export --format csv

# Supported: SQLite, PostgreSQL, MySQL, MariaDB
```

## Filesystem Commands

```bash
# Filesystem operations
pyffice filesystem list --path /data
pyffice filesystem sync --source /source --target /target
pyffice filesystem find --pattern "*.pdf"

# Operations: list, sync, find, copy, move, delete
```

## Analytics Commands

```bash
# Analytics operations
pyffice analytics report --type summary --period month
pyffice analytics dashboard
pyffice analytics export --format json

# Report types: summary, detailed, comparison
```

## Project Commands

```bash
# Project operations
pyffice project create --name "My Project" --template default
pyffice project list
pyffice project status --id 123

# Templates: default, agile, kanban
```

## Config Commands

```bash
# Configuration operations
pyffice config show
pyffice config set --key debug --value true
pyffice config validate
pyffice config export --format yaml

# Configuration file: pyffice.yaml
```

## Form Commands

```bash
# Form operations
pyffice form create --template survey --output form.json
pyffice form validate --input form.json --schema schema.json
pyffice form render --template form.json --data data.json

# Form types: survey, contact, order, feedback
```

## Notebook Commands

```bash
# Notebook operations
pyffice notebook convert notebook.ipynb --output html
pyffice notebook execute notebook.ipynb --output executed.ipynb

# Supported: Jupyter (.ipynb), HTML, PDF, Markdown
```

## Report Commands

```bash
# Report operations
pyffice report generate --template annual --data data.json --output report.pdf
pyffice report list

# Templates: annual, quarterly, monthly, custom
```

## Social Commands

```bash
# Social media operations
pyffice social post --platform twitter --message "Hello World"
pyffice social post --platform linkedin --message "Update" --image image.png

# Platforms: twitter, linkedin, facebook, instagram
```

## Tag Commands

```bash
# Tag operations
pyffice tag list
pyffice tag add --name "important" --color red
pyffice tag search "priority"

# Tag management for organizing content
```

## Text Commands

```bash
# Text operations
pyffice text convert --input text.md --output html
pyffice text summarize --input document.txt --length 200
pyffice text translate --input text.txt --from en --to es

# Operations: convert, summarize, translate, spellcheck
```

## Update Commands

```bash
# Update operations
pyffice update check
pyffice update install --version 0.2.0
pyffice update status

# Version management and migrations
```

## Web Commands

```bash
# Web operations
pyffice web fetch --url "https://example.com" --output page.html
pyffice web parse --input page.html --selector "article"
pyffice web screenshot --url "https://example.com" --output screenshot.png

# Web scraping and parsing utilities
```

## Workflow Commands

```bash
# Workflow operations
pyffice workflow run my-workflow
pyffice workflow list
pyffice workflow status --id 123
pyffice workflow create --name "New Workflow" --definition workflow.yaml

# Workflow automation and execution
```

## CAM Commands

```bash
# CAM operations
pyffice cam generate --input design.dxf --output gcode.nc
pyffice cam preview --input design.dxf

# CNC toolpath generation from CAD designs
```

## Matrix Commands

```bash
# Matrix operations
pyffice matrix multiply --a matrix_a.csv --b matrix_b.csv --output result.csv
pyffice matrix invert --input matrix.csv --output inverse.csv
pyffice matrix eigenvalues --input matrix.csv

# Linear algebra operations
```

## Global Options

```bash
--help, -h          Show help message
--version, -v       Show version
--debug             Enable debug mode
--verbose, -vv      Verbose output
--config CONFIG     Custom config file
--output DIR        Output directory
```

## Examples

```bash
# Convert a document to PDF
pyffice document convert report.docx report.pdf

# Batch convert all spreadsheets in a folder
for f in *.xlsx; do pyffice spreadsheet convert "$f" "${f%.xlsx}.csv"; done

# Create a chart from CSV data
pyffice chart create --type bar --data sales.csv --output chart.png

# Send an email with attachment
pyffice email send --to team@example.com --subject "Report" --body "See attached" --file report.pdf

# Run a workflow
pyffice workflow run data-processing-pipeline
```
