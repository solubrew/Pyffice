# Pyffice

A unified Python interface for document processing, CAD, media, and office automation.

## Overview

Pyffice provides a consistent API for working with various file formats and office applications:

- **Documents**: PDF, Word, Excel, PowerPoint, RTF, ODT
- **CAD**: STL, OBJ, DWG, DXF, STEP, IGES, FBX, GLTF
- **Media**: Images, Audio, Video, HEIC, RAW
- **Data**: CSV, JSON, XML, YAML
- **Office**: Calendar, Tasks, Contacts, Email

## Installation

```bash
pip install pyffice
```

## Usage

### Command Line

```bash
# Convert a document
pyffice document convert input.docx output.pdf

# Convert a spreadsheet
pyffice spreadsheet convert data.xlsx output.csv

# Convert an image
pyffice image convert photo.png output.jpg

# List supported formats
pyffice formats
```

### Python API

```python
from pyffice import document, spreadsheet, presentation

# Open a document
doc = document.open("report.docx")

# Work with spreadsheets
sheet = spreadsheet.open("data.xlsx")
sheet.save("output.xlsx")

# Process CAD files
cad = pyffice.cad.load("model.stl")
```

## Quick Start

```python
from pyffice import document, spreadsheet, presentation

# Open a document
doc = document.open("report.docx")

# Work with spreadsheets
sheet = spreadsheet.open("data.xlsx")
sheet.save("output.xlsx")

# Process CAD files
cad = pyffice.cad.load("model.stl")
```

## Features

- Unified API across file formats
- Port-based architecture for extensibility
- Full support for create, read, update, delete operations
- Cross-platform compatibility

## License

MIT License
