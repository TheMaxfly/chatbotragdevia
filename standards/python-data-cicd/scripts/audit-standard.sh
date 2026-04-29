#!/usr/bin/env bash
set -euo pipefail

package="${1:-your_package}"

echo "== Ruff lint =="
uv run ruff check .

echo "== Ruff format =="
uv run ruff format --check .

echo "== Pyright =="
uv run pyright "${package}/"

echo "== Bandit =="
uv run bandit -r "${package}/" -c pyproject.toml

echo "== pip-audit =="
uv run pip-audit

echo "== pytest =="
uv run pytest tests/unit/ -v --cov="${package}" --cov-report=term-missing --cov-report=xml

if command -v trivy >/dev/null 2>&1; then
  echo "== Trivy =="
  trivy fs --severity HIGH,CRITICAL --ignore-unfixed .
else
  echo "== Trivy skipped: command not found =="
fi

