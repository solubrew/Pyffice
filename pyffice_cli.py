#!/usr/bin/env python3
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name: Pyffice CLI
    description: >
        Command-line interface for Pyffice document management.
        Provides commands to create, manage, and convert office documents.
    version: 0.0.1
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""
# -*- coding: utf-8 -*
from __future__ import annotations

import argparse
import logging
import json
import sys
from os.path import abspath, dirname, join
from typing import Any, Optional
# Configure logging
logger = logging.getLogger(__name__)

# Add project to path
sys.path.insert(0, join(dirname(__file__), ""))

# Try to import PyfficeCodex, but allow CLI to work without full dependency chain
try:
    from pyffice.pyffice import PyfficeCodex
    PYFFICE_AVAILABLE = True
except ImportError as e:
    PYFFICE_AVAILABLE = False
    PyfficeCodex = None
    _import_error = str(e)


def cmd_create(args: argparse.Namespace) -> int:
    """Create a new Pyffice document."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        logger.info("Run 'pyffice skill' to see skill documentation anyway")
        return 1
    
    codex = PyfficeCodex()
    
    doc_type = args.type
    name = args.name or f"untitled_{doc_type}"
    
    doc = None
    if doc_type == "calendar":
        doc = codex.init_calendar({"name": name})
    elif doc_type == "chart":
        doc = codex.init_chart({"name": name})
    elif doc_type == "contacts":
        doc = codex.init_contacts({"name": name})
    elif doc_type == "files":
        doc = codex.init_files({"name": name})
    elif doc_type == "form":
        doc = codex.init_form({"name": name})
    elif doc_type == "image":
        doc = codex.init_image({"name": name})
    elif doc_type == "matrix":
        doc = codex.init_matrix({"name": name})
    elif doc_type == "notebook":
        doc = codex.init_notebook({"name": name})
    elif doc_type == "pdf":
        doc = codex.init_pdf({"name": name})
    elif doc_type == "prompt":
        doc = codex.init_prompt({"name": name})
    elif doc_type == "script":
        doc = codex.init_script({"name": name})
    elif doc_type == "sketch":
        doc = codex.init_sketch({"name": name})
    elif doc_type == "source":
        doc = codex.init_source({"name": name})
    elif doc_type == "browser":
        doc = codex.init_browser({"name": name})
    else:
        logger.error( Unknown document type '{doc_type}'")
        return 1
    
    if doc:
        logger.info(f"Created {doc_type} document: {doc.did}")
        return 0
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    """List documents in the codex."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    codex.load_document()
    
    docs = codex.documents
    if not docs:
        logger.info("No documents in codex")
        return 0
    
    logger.info(f"Documents in codex ({len(docs)}):")
    for doc_id, doc in docs.items():
        doc_type = type(doc).__name__
        logger.info(f"  - {doc_id}: {doc_type}")
    
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    """Get info about a specific document."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    codex.load_document()
    
    doc_id = args.id
    doc = codex.documents.get(doc_id)
    
    if not doc:
        logger.info(f"Document '{doc_id}' not found")
        return 1
    
    logger.info(f"Document: {doc_id}")
    logger.info(f"  Type: {type(doc).__name__}")
    
    if hasattr(doc, 'name'):
        logger.info(f"  Name: {doc.name}")
    if hasattr(doc, 'created'):
        logger.info(f"  Created: {doc.created}")
    
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """Export codex to YAML or JSON."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    codex.load_document()
    
    output = args.output or "-"
    syntax = args.format or "yaml"
    
    if syntax == "yaml":
        result = codex.to_yaml()
    elif syntax == "json":
        result = json.dumps(codex.to_summary(), indent=2)
    else:
        logger.error( Unknown format '{syntax}'")
        return 1
    
    if output == "-":
        logger.info(result)
    else:
        with open(output, 'w') as f:
            f.write(result)
        logger.info(f"Exported to {output}")
    
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    """Get token-efficient summary of the codex."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    codex.load_document()
    
    summary = codex.to_summary()
    logger.info(json.dumps(summary, indent=2))
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    """Get JSON schema for LLM validation."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    
    schema = codex.to_json_schema()
    logger.info(json.dumps(schema, indent=2))
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """Import documents into the codex."""
    if not PYFFICE_AVAILABLE:
        logger.error( PyfficeCodex not available - {_import_error}")
        return 1
    
    codex = PyfficeCodex()
    
    source = args.source
    if source.endswith('.yaml') or source.endswith('.yml'):
        with open(source, 'r') as f:
            yaml_str = f.read()
        codex = PyfficeCodex.from_yaml(yaml_str)
        logger.info(f"Imported from {source}")
    else:
        logger.error( Unsupported file format. Use .yaml or .yml")
        return 1
    
    return 0


def cmd_skill(args: argparse.Namespace) -> int:
    """Generate skill document for Pyffice."""
    skill_doc = '''# Pyffice Skill

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
'''
    logger.info(skill_doc)
    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='pyffice',
        description='Pyffice - Polyglot Office Document Management'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # create
    create_parser = subparsers.add_parser('create', help='Create a new document')
    create_parser.add_argument('type', help='Document type (calendar, chart, contacts, etc.)')
    create_parser.add_argument('--name', help='Document name')
    
    # list
    subparsers.add_parser('list', help='List all documents')
    
    # info
    info_parser = subparsers.add_parser('info', help='Get document info')
    info_parser.add_argument('id', help='Document ID')
    
    # export
    export_parser = subparsers.add_parser('export', help='Export codex')
    export_parser.add_argument('--output', help='Output file (- for stdout)')
    export_parser.add_argument('--format', choices=['yaml', 'json'], default='yaml')
    
    # summary
    subparsers.add_parser('summary', help='Get codex summary')
    
    # schema
    subparsers.add_parser('schema', help='Get JSON schema')
    
    # import
    import_parser = subparsers.add_parser('import', help='Import from YAML')
    import_parser.add_argument('source', help='Source YAML file')
    
    # skill
    subparsers.add_parser('skill', help='Show skill document')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    commands = {
        'create': cmd_create,
        'list': cmd_list,
        'info': cmd_info,
        'export': cmd_export,
        'summary': cmd_summary,
        'schema': cmd_schema,
        'import': cmd_import,
        'skill': cmd_skill,
    }
    
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
