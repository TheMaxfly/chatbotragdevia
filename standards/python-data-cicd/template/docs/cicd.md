# CI/CD

## Flux

```text
feature/* -> develop -> main
```

## Jobs CI

| Job | Commande |
|---|---|
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format --check .` |
| Types | `uv run pyright your_package/` |
| Sécurité code | `uv run bandit -r your_package/ -c pyproject.toml` |
| Sécurité dépendances | `uv run pip-audit` |
| Sécurité Docker/IaC | Trivy |
| Tests | `uv run pytest tests/unit/ -v --cov=your_package` |

## Release

Les releases sont calculées automatiquement par `python-semantic-release` à partir des Conventional Commits.

| Commit | Version |
|---|---|
| `feat:` | MINOR |
| `fix:` | PATCH |
| `perf:` | PATCH |
| `feat!:` | MAJOR |

