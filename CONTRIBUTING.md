# Contributing to Pyffice

Welcome to the Pyffice project! We're excited that you want to contribute.

## Development Workflow

### 1. Branch Management

- **Main Branch**: `main` - Production-ready code
- **Development Branch**: `develop` - Integration branch for features
- **Gamma Branch**: `gamma` - Active development and fixes

### 2. Making Changes

```bash
# Create a new branch for your work
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix

# Make your changes
# ... edit files ...

# Run tests
pytest

# Run linting
pylint pyffice/

# Run security checks
bandit -r pyffice/
```

### 3. Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, Refactor)
- Keep commits focused and atomic
- Reference issues when applicable

Good commit messages:
```
Add support for PDF to DOCX conversion
Fix memory leak in image processing
Update CLI documentation for new commands
Refactor document module imports
```

### 4. Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add/update tests for new features
4. Create a pull request to `gamma` branch
5. Request review from maintainers

### 5. Code Standards

- Follow PEP 8 style guidelines
- Add type hints where possible
- Write docstrings for public functions/classes
- Keep functions focused (single responsibility)
- Maximum line length: 100 characters

### 6. Testing Requirements

- All new features must include tests
- All bug fixes must include regression tests
- Maintain test coverage above 80%
- Run `pytest` before submitting PR

### 7. Documentation

- Update README.md for user-facing changes
- Update CLI.md for CLI changes
- Add docstrings to new functions/classes
- Update docstrings when changing existing code

### 8. Reporting Issues

When reporting bugs:
- Use the issue tracker
- Include Python version
- Include minimal reproduction case
- Include full traceback

## Quick Reference

```bash
# Setup development environment
pip install -e ".[dev]"

# Run all checks
pytest && pylint pyffice/ && bandit -r pyffice/

# Run specific test file
pytest tests/test_pyffice/tests/test_csv.py

# Format code
black pyffice/ && isort pyffice/
```

## Questions?

Feel free to open an issue for questions or discussion.

Thank you for contributing to Pyffice!
