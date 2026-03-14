# Pyffice CLI

## Overview
Command-line interface for Pyffice document conversion.

## Commands

### convert
Convert a document from one format to another.

```bash
pyffice convert input.dia output.svg
```

### diagram
Work with diagram files.

```bash
# Convert diagram
pyffice diagram convert input.dot output.png

# List supported formats
pyffice diagram formats
```

### info
Show Pyffice information.

```bash
pyffice info
```

## Options

- `--verbose`, `-v` - Enable verbose output
- `--quiet`, `-q` - Suppress output
- `--config CONFIG` - Specify config file

## Examples

Convert a Dia diagram to SVG:
```bash
pyffice convert diagram.dia -o diagram.svg
```

Convert multiple files:
```bash
pyffice batch convert --input-dir ./diagrams --output-dir ./output
```
