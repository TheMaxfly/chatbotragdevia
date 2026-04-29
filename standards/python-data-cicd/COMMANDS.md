# Commandes standard

## Installation

```bash
uv sync --all-groups
uv run pre-commit install
```

## Qualité locale

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright your_package/
```

Correction automatique :

```bash
uv run ruff check --fix .
uv run ruff format .
```

## Sécurité

```bash
uv run bandit -r your_package/ -c pyproject.toml
uv run pip-audit
```

Trivy en local si installé :

```bash
trivy fs --severity HIGH,CRITICAL --ignore-unfixed .
```

## Tests

```bash
uv run pytest tests/unit/ -v --cov=your_package --cov-report=term-missing --cov-report=xml
uv run pytest tests/integration/ -v
```

## Release

```bash
uv run semantic-release version --print
uv run semantic-release version --print-tag
```
