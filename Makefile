.PHONY: help install dev test lint format typecheck clean docs

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  dev        - Install dev dependencies and setup hooks"
	@echo "  test       - Run tests"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  lint       - Run linter (ruff)"
	@echo "  format     - Format code"
	@echo "  typecheck  - Run mypy type checking"
	@echo "  clean      - Clean generated files"
	@echo "  check      - Run all checks (lint, format, typecheck, test)"

install:
	pip install -e ".[dev]"

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest -v

test-coverage:
	pytest -v --cov=src/plane_mcp_server --cov-report=html

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

typecheck:
	mypy src/plane_mcp_server

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
	rm -rf build/ dist/ *.egg-info/

check: lint format typecheck test
