# CI/CD

## Flux Git

```text
feature/* -> develop -> main
```

Règles attendues :

- ouvrir une Pull Request pour intégrer vers `develop` ou `main`
- exiger la CI verte avant merge
- réserver `main` aux versions publiables
- déclencher les releases depuis `main`

## Jobs CI

| Job | Commande |
|---|---|
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format --check .` |
| Types | `uv run pyright src/` |
| Sécurité code | `uv run bandit -r src/ -c pyproject.toml` |
| Sécurité dépendances | `uv run pip-audit` |
| Sécurité Docker/IaC | Trivy |
| Tests | `uv run pytest tests/unit/ -v --cov=src` |

## Commits et release

Le projet suit Conventional Commits.

| Commit | Effet |
|---|---|
| `feat:` | version mineure |
| `fix:` | version patch |
| `perf:` | version patch |
| `feat!:` ou `BREAKING CHANGE:` | version majeure |
| `docs:`, `test:`, `chore:`, `ci:`, `style:` | pas de release sauf breaking change |

Les releases sont calculées par `python-semantic-release` à partir des commits présents sur `main`.

Prévisualisation locale :

```bash
uv run semantic-release version --print
uv run semantic-release version --print-tag
```
