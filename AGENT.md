# Pyffice Agent Guidelines

## Project Context

Pyffice is a comprehensive Python framework for handling document formats, media types, and office operations. It uses a port-based architecture for extensibility.

## Architecture

```
pyffice/
├── cli.py              # 72+ CLI commands
├── document.py         # Document processing
├── spreadsheet.py      # Spreadsheet handling
├── presentation.py     # Presentation files
├── pyffice.py          # Core Pyffice class
├── pyffice/
│   ├── ports/          # Port interfaces
│   ├── calendars/      # Calendar integration
│   ├── charts/         # Chart generation
│   ├── config/         # Configuration management
│   ├── contacts/       # Contact management
│   ├── filesystems/    # Filesystem operations
│   ├── forms/          # Form processing
│   ├── images/         # Image processing
│   ├── items/          # Item management
│   ├── matrix/         # Matrix operations
│   ├── notebooks/      # Notebook support
│   ├── script/         # Script execution
│   ├── skills/         # Skill definitions
│   ├── tags/           # Tag management
│   ├── updates/        # Update system
│   └── web/            # Web integration
└── workflows/          # Workflow automation
```

## Key Patterns

### Port-Based Architecture

Pyffice uses ports (interfaces) to define capabilities:

```python
from pyffice.ports import DocumentPort

class MyDocumentHandler(DocumentPort):
    def read(self, path: str) -> bytes:
        ...
    def write(self, path: str, data: bytes) -> None:
        ...
```

### CLI Commands

All CLI commands should:
- Use argparse with proper type hints
- Include help text
- Support --verbose and --quiet flags
- Return appropriate exit codes

### Logging

Use the logging module, not print():

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Processing document")
logger.error("Failed to open file")
```

## Quality Standards

- **Pylint**: 0 errors, minimal warnings
- **Bandit**: 0 HIGH/MEDIUM issues
- **Type Annotations**: Use where practical
- **Docstrings**: Required for public APIs

## Version Management

Versions are managed in `pyffice/updates/version.yaml`:

```yaml
version: 0.1.1
transitions:
  - from: 0.1.0
    to: 0.1.1
    changes:
      - Replace print() with logging
      - Fix pylint errors
```

## Agent Workflow

1. Check current state: `git status`
2. Create feature branch: `git checkout -b feature/name`
3. Make changes with tests
4. Run quality checks
5. Update documentation
6. Commit with clear messages
7. Push and create PR
