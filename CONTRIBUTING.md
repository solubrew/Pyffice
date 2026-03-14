# Contributing to Pyffice

## Welcome

Thank you for considering contributing to Pyffice!

## Development Setup

```bash
# Clone the repository
git clone git@github.com:pyffice/pyffice.git
cd pyffice

# Create and activate development environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## Code Standards

- Follow PEP 8
- Use type hints where possible
- Add docstrings to all public functions
- Run `ruff check` and `ruff format` before committing
- Ensure tests pass: `pytest`

## Testing

```bash
# Run all tests
pytest

# Run specific test module
pytest test_pyffice/unit/diagrams/

# Run with coverage
pytest --cov=pyffice
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests and linting
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## License

By contributing, you agree that your contributions will be licensed under the project's license.
