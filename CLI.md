# Pyffice CLI

## Overview
Pyffice is a polyglot office document package that creates YAML versions of office files with bidirectional conversion. Provides AI Agent enhanced tool-ready functions.

## Usage

```bash
pyffice <command> [OPTIONS]
```

## Arguments

| Argument | Type | Required | Description | Default |
|----------|------|----------|--------------|---------|
| `command` | string | Yes | The subcommand to run | - |
| `type` | string | For create | Document type | - |
| `id` | string | For info | Document ID | - |
| `source` | string | For import | Source YAML file | - |
| `--name` | string | No | Document name | `untitled_<type>` |
| `--output` | string | No | Output file (- for stdout) | stdout |
| `--format` | string | No | Output format (yaml/json) | yaml |

## Commands

| Command | Description |
|---------|-------------|
| `create <type>` | Create a new document |
| `list` | List all documents in codex |
| `info <doc_id>` | Get document info |
| `export` | Export codex to YAML or JSON |
| `summary` | Get token-efficient summary |
| `schema` | Get JSON schema for LLM validation |
| `import <file>` | Import from YAML file |
| `skill` | Show skill document |

## Document Types

| Type | Description |
|------|-------------|
| calendar | Calendar/scheduling document |
| chart | Chart/visualization document |
| contacts | Contact/rolodex database |
| files | Filesystem document |
| form | Form document |
| image | Image document |
| matrix | Spreadsheet document |
| notebook | Notebook document |
| pdf | PDF document |
| prompt | Prompts manager |
| script | Text/script document |
| sketch | Diagram/sketch document |
| source | Data source |
| browser | Web browser |

## Examples

```bash
# Create a calendar document
pyffice create calendar --name "my_calendar"

# Create a matrix document
pyffice create matrix --name "budget"

# List all documents
pyffice list

# Get document info
pyffice info doc_123

# Export to YAML file
pyffice export --output codex.yaml --format yaml

# Get summary for LLM
pyffice summary

# Get JSON schema
pyffice schema

# Import from YAML
pyffice import my_codex.yaml

# Show skill document
pyffice skill
```
