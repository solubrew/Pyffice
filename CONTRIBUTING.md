# Contributing to Pyffice

Thank you for your interest in contributing to Pyffice!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/solutionsbrewer/pyffice.git
cd pyffice

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install pytest pytest-cov
```

## Running Tests

```bash
# Run all tests
pytest test_pyffice/ -v

# Run with coverage
pytest test_pyffice/ --cov=pyffice --cov-report=html
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Run linters before committing:
  ```bash
  ruff check pyffice/
  black pyffice/
  isort pyffice/
  ```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
