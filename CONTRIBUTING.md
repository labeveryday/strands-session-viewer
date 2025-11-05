# Contributing to Strands Session Viewer

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/strands-agents/strands-session-viewer
cd strands-session-viewer
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/strands_viewer --cov-report=html

# Run specific test file
pytest tests/test_session_reader.py -v
```

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Check formatting without changes
black --check src/ tests/
```

### Linting

```bash
# Run Ruff linter
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Security Scanning

```bash
# Run Bandit security scanner
bandit -r src/strands_viewer/
```

### Running the Viewer Locally

```bash
# From package root
strands-viewer /path/to/sessions

# Or with Python module
python -m strands_viewer.cli /path/to/sessions
```

## Code Style Guidelines

- **Line Length**: Maximum 100 characters
- **Formatting**: Use Black for code formatting
- **Linting**: Code must pass Ruff checks
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: All public functions should have docstrings

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use fixtures from `conftest.py`

### Test Coverage

- Aim for at least 80% code coverage
- All new features must include tests
- Bug fixes should include regression tests

### Example Test

```python
def test_feature(temp_sessions_dir):
    """Test description."""
    reader = SessionReader(temp_sessions_dir)
    result = reader.some_method()
    assert result == expected_value
```

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write code following style guidelines
- Add tests for new functionality
- Update documentation if needed

### 3. Run Quality Checks

```bash
# Format code
black src/ tests/

# Run linter
ruff check --fix src/ tests/

# Run tests
pytest --cov

# Security check
bandit -r src/strands_viewer/
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: Add awesome new feature"
```

#### Commit Message Format

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to any related issues
- Screenshots if UI changes

## CI/CD Pipeline

All PRs must pass:

1. **Linting** - Black formatting and Ruff checks
2. **Security** - Bandit security scan
3. **Tests** - All tests pass on Python 3.8-3.12
4. **Build** - Package builds successfully

The CI runs automatically on every PR.

## Release Process

Releases are handled by maintainers:

1. Update version in `src/strands_viewer/__version__.py`
2. Update version in `pyproject.toml`
3. Create release notes
4. Tag release: `git tag v0.x.0`
5. Push tag: `git push origin v0.x.0`
6. GitHub Actions automatically publishes to PyPI

## Questions?

- Open an issue for bug reports or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
