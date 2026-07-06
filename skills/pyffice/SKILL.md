# Pyffice Skill

## Overview
Pyffice is a polyglot office document package that creates YAML versions of office files with bidirectional conversion. It provides AI Agent enhanced tool-ready functions.

## Quick Start
```python
from pyffice.pyffice import PyfficeCodex

# Create a codex
codex = PyfficeCodex()

# Create documents
calendar = codex.init_calendar({"name": "my_calendar"})
matrix = codex.init_matrix({"name": "budget"})
contacts = codex.init_contacts({"name": "contacts"})

# Export to YAML
yaml_str = codex.to_yaml()

# Get summary for LLM
summary = codex.to_summary()
```

## Document Types

| Type | Method | Description |
|------|--------|-------------|
| calendar | `init_calendar(cfg)` | Calendar/scheduling document |
| chart | `init_chart(cfg)` | Chart/visualization document |
| contacts | `init_contacts(cfg)` | Contact/rolodex database |
| files | `init_files(cfg)` | Filesystem document |
| form | `init_form(cfg)` | Form document |
| image | `init_image(cfg)` | Image document |
| matrix | `init_matrix(cfg)` | Spreadsheet document |
| notebook | `init_notebook(cfg)` | Notebook document |
| pdf | `init_pdf(cfg)` | PDF document |
| prompt | `init_prompt(cfg)` | Prompts manager |
| script | `init_script(cfg)` | Text/script document |
| sketch | `init_sketch(cfg)` | Diagram/sketch document |
| source | `init_source(cfg)` | Data source |
| browser | `init_browser(cfg)` | Web browser |

## AI Agent Methods

### to_yaml() -> str
Convert entire codex to YAML string for serialization.

### from_yaml(yaml_str) -> PyfficeCodex
Load a codex from a YAML string.

### to_summary() -> dict
Get token-efficient summary for AI agents.
```python
{
    "version": "0.0.1.0.1.0",
    "document_count": 5,
    "document_types": ["PyfficeCalendar", "PyfficeMatrix"],
    "has_contacts": True,
    "has_forms_manager": False,
    "import_count": 0
}
```

### to_json_schema() -> dict
Get JSON Schema for LLM output validation.

### to_chunks(chunk_size=1000, overlap=100) -> list
Split codex into embedding-ready chunks for vector storage.

## CLI Commands

```bash
# Create a document
pyffice create <type> [--name NAME]

# List all documents
pyffice list

# Get document info
pyffice info <doc_id>

# Export codex
pyffice export [--output FILE] [--format yaml|json]

# Get summary
pyffice summary

# Get JSON schema
pyffice schema

# Import from YAML
pyffice import <source.yaml>

# Show this skill
pyffice skill
```

## Configuration
Pyffice uses `_data_/pyffice.yaml` for configuration.

## Project Location
- Project: `/home/solubrew/.orin/workspace/projects/pyffice/`
- Main module: `pyffice/pyffice/pyffice.py`
- CLI script: `pyffice_cli.py`

## Usage with CLI
```bash
# Make executable
chmod +x /home/solubrew/.orin/workspace/projects/pyffice/pyffice_cli.py

# Run
python3 /home/solubrew/.orin/workspace/projects/pyffice/pyffice_cli.py skill
```
