# Pyffice CLI

## Usage

```bash
pyffice [COMMAND] [OPTIONS]
```

## Commands

### document

Work with documents (Word, PDF, etc.)

```bash
pyffice document open <file>
pyffice document convert <input> <output>
pyffice document info <file>
```

### spreadsheet

Work with spreadsheets (Excel, CSV)

```bash
pyffice spreadsheet open <file>
pyffice spreadsheet create <name>
pyffice spreadsheet export <file> --format csv
```

### cad

Process CAD files

```bash
pyffice cad convert <input> <output>
pyffice cad info <file>
pyffice cad validate <file>
```

### image

Process images

```bash
pyffice image convert <input> <output>
pyffice image resize <file> --width 800 --height 600
pyffice image thumbnail <file>
```

## Options

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable verbose output |
| `-q, --quiet` | Suppress output |
| `--version` | Show version |
| `--help` | Show help |

## Examples

```bash
# Open and convert a document
pyffice document convert input.docx output.pdf

# Create a spreadsheet
pyffice spreadsheet create report.xlsx

# Convert CAD file
pyffice cad convert model.stl model.obj
```

## Exit Codes

- `0` - Success
- `1` - Error
