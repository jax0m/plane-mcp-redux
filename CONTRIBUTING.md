# Contributing to Plane MCP Redux

Thank you for your interest in contributing to Plane MCP Redux! This guide will help you get started.

## Development Setup

1. **Clone the repository**

    ```bash
    git clone <your-fork>
    cd plane-mcp-redux
    ```

2. **Set up the virtual environment**

    ```bash
    # Using venv
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

    # Install dependencies
    pip install -e ".[dev]"
    ```

3. **Install pre-commit hooks**
    ```bash
    pre-commit install
    ```

## Development Workflow

### Code Style

This project uses the following tools for code quality:

- **Ruff**: Fast Python linter and formatter
- **Mypy**: Static type checker
- **Pre-commit**: Git hooks for automatic fixes

### Making Changes

1. Create a feature branch:

    ```bash
    git checkout -b feature/your-feature-name
    ```

2. Make your changes

3. Run pre-commit hooks:

    ```bash
    pre-commit run --all-files
    ```

4. Write tests for your changes

5. Commit with a descriptive message:
    ```bash
    git commit -m "feat: add your feature description"
    ```

### Writing Tests

Tests should be in the `tests/` directory. Use pytest:

```python
def test_your_feature():
    # Your test code
    assert result == expected
```

Run tests:

```bash
pytest -v
```

## Pull Request Guidelines

1. **Title**: Use conventional commits (feat:, fix:, docs:, etc.)
2. **Description**: Explain what and why
3. **Tests**: Include tests for new features
4. **Documentation**: Update README or docs as needed

## Code Review

- All PRs require at least one reviewer
- CI must pass before merging
- Keep PRs small and focused

## Questions?

Open an issue for questions or discussions.
