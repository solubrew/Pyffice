# AGENT.md - Pyffice Agent Context

## Project Overview
- **Name**: Pyffice
- **Type**: Python Office Suite Wrapper Library
- **Purpose**: Unified Python interface for office document manipulation (diagrams, spreadsheets, presentations, PDFs, etc.)
- **Language**: Python 3.12+

## Architecture
- **Core**: pyffice/document.py - Base document classes
- **Modules**: 30+ submodules covering office formats
- **Testing**: test_pyffice/ with unit tests

## Key Conventions
- All modules use `logger = logging.getLogger(__name__)`
- Classes use snake_case naming internally
- CLI via pyffice/cli.py using Click
- Configuration via config.yaml

## Dependencies
- External: click, pyyaml, reportlab, pillow, etc.
- Internal: ogma (logging), condor (utilities)

## Common Tasks
- Document conversion: `convert_document(input, output, format)`
- Configuration: `validate_config(path)`
- CLI: `pyffice convert <input> <output> --format pdf`

## Quality Gates
- Type annotations preferred (0.7% current - needs improvement)
- Pylint score: 100%
- No security issues (bandit)
