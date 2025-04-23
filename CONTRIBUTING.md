# Contributing to Paddle SDK

Thank you for your interest in contributing to Paddle SDK! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/CCXLV/paddle-sdk.git
   cd paddle-sdk
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```
5. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Run `black .` and `ruff check .` before committing

### Type Hints

- Use type hints throughout the codebase
- Follow the existing type hint patterns in the code
- Make sure all function parameters and return values are properly typed

### Testing

- Write tests for all new features
- Ensure all tests pass before submitting a PR
- Follow the existing test structure:
  - Unit tests in `tests`
- Use pytest fixtures from `conftest.py` when appropriate
- Mock external API calls in unit tests

### Documentation

- Update the README.md if your changes affect usage
- Update the CHANGELOG.md with your changes
- Add docstrings to all new functions and classes
- Follow the existing docstring format:
  ```python
  def function(param: str) -> bool:
      """
      Brief description of the function.

      Args
      ----
          param: Description of the parameter.

      Returns
      -------
          Description of the return value.

      Raises
      ------
          ExceptionType: Description of when this exception is raised.

      Examples
      ------- ::
            function("Hello World")
      """
  ```

## API Implementation Guidelines

When implementing new API endpoints:

1. Create a new resource class in `paddle/models/resources/`
2. Add response models in `paddle/models/responses/`
3. Add the resource to the client in `_init_resources()`
4. Implement all CRUD operations:
   - List
   - Get
   - Create
   - Update
5. Add comprehensive tests
6. Update the CHANGELOG.md checklist

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the CHANGELOG.md with your changes
3. Submit a pull request with a clear description of the changes
4. Reference any related issues in your PR description
5. Wait for review and address any feedback

## Release Process

1. Update version in `paddle/__init__.py`
2. Update CHANGELOG.md with release date
3. Create a new release on GitHub
4. Update PyPI package

## Questions?

Feel free to open an issue if you have any questions about contributing! 