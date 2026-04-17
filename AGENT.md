# AGENT.md - Pyffice Agent Context

## Project Overview
- **Name**: Pyffice
- **Type**: Python Office Suite Wrapper Library
- **Purpose**: Unified Python interface for office document manipulation (diagrams, spreadsheets, presentations, PDFs, etc.)
- **Language**: Python 3.12+
- **Agent**: orin (this workspace)
- **Git Branch**: orin-ws
- **Audit Score**: 82.27% (target: 95%)

## Architecture
- **Core**: pyffice/document.py - Base document classes
- **Modules**: 30+ submodules covering office formats
- **Testing**: test_pyffice/ with unit tests
- **CLI**: pyffice/cli.py with Click (30 commands)

## Current Status
### Dimensions Passing (9/15)
- cli_documentation (100%)
- configuration (100%)
- dependency_strategy (100%)
- documentation (100%)
- git_workflow (100%)
- structure (100%)
- licenses (100%)

### Dimensions Failing/Partial (6/15)
- module_cli_coverage (0%) - CLI exists but analyzer not detecting
- agent_awareness (0%) - Need comprehensive agent context
- license_dependencies (25%) - Need pip-licenses
- logging (50%) - Uses logging but not logma
- kiss_dry (50%) - 328 magic numbers
- duplicate_files (50%) - 10 duplicate files

## Key Conventions
- All modules use `logger = logging.getLogger(__name__)`
- Classes use snake_case naming internally
- CLI via pyffice/cli.py using Click
- Configuration via config.yaml

## Dependencies
- External: click, pyyaml, reportlab, pillow, etc.
- Internal: ogma (logging), kahndor (utilities)

## Common Tasks
- Document conversion: `convert_document(input, output, format)`
- Configuration: `validate_config(path)`
- CLI: `pyffice convert <input> <output> --format pdf`

## Quality Gates
- Type annotations preferred (0.7% current - needs improvement)
- Pylint score: 100%
- No security issues (bandit)
