# Pyffice CLI

Command-line interface for Pyffice.

## Installation

```bash
pip install pyffice
```

## Usage

### Convert Documents

```bash
pyffice convert input.docx output.pdf
```

### Create New Document

```bash
pyffice create --type spreadsheet output.xlsx
pyffice create --type presentation output.pptx
pyffice create --type document output.docx
```

### List Supported Formats

```bash
pyffice formats
```

### Diagram Operations

```bash
# Convert diagram formats
pyffice diagram convert input.dia output.svg

# List supported diagram formats
pyffice diagram formats
```

### Configuration

```bash
# Show configuration
pyffice config show

# Validate configuration
pyffice config validate
```

## Options

- `--verbose`, `-v` - Enable verbose output
- `--quiet`, `-q` - Suppress output
- `--config CONFIG` - Specify config file

## Examples

Convert a Dia diagram to SVG:
```bash
pyffice diagram convert my_diagram.dia output.svg
```

Create a new spreadsheet:
```bash
pyffice create --type spreadsheet --template monthly_budget.xlsx
```
