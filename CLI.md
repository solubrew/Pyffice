# CLI Usage

## Pyffice Command Line Interface

Pyffice provides a comprehensive CLI for document processing and conversion.

### Installation

```bash
pip install pyffice
```

### Basic Usage

```bash
# Convert a document
pyffice convert input.docx output.pdf

# Process multiple files
pyffice batch convert --input-dir ./docs --output-dir ./output

# Extract data from documents
pyffice extract --format json document.pdf

# List supported formats
pyffice formats list

# Validate a document
pyffice validate document.docx
```

### Commands

| Command | Description |
|---------|-------------|
| `convert` | Convert between document formats |
| `batch` | Batch process multiple files |
| `extract` | Extract data from documents |
| `formats` | List supported formats |
| `validate` | Validate document structure |

### Options

- `-v, --verbose` - Enable verbose output
- `-q, --quiet` - Suppress output
- `--config PATH` - Custom configuration file

### Examples

```bash
# Convert DOCX to PDF
pyffice convert report.docx report.pdf

# Batch convert all DOCX files
pyffice batch convert --input-dir ./documents --pattern "*.docx"

# Extract tables to JSON
pyffice extract --type tables spreadsheet.xlsx --output tables.json
```
