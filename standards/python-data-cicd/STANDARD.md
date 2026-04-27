# Standard Python Data CI/CD

Ce dossier définit la norme réutilisable pour les projets Python orientés IA, data engineering, API ou application conteneurisée.

## Socle obligatoire

| Domaine | Standard |
|---|---|
| Gestion Python | `uv`, `pyproject.toml`, `uv.lock` versionné |
| Lint | Ruff |
| Formatage | Ruff format |
| Typage | Pyright |
| Tests | pytest + pytest-cov |
| Hooks locaux | pre-commit |
| Sécurité code | Bandit |
| Sécurité dépendances | pip-audit |
| Sécurité Docker/IaC | Trivy si Docker, IaC ou déploiement cloud |
| Versioning | SemVer |
| Commits | Conventional Commits |
| Release | python-semantic-release |
| CI/CD | GitHub Actions |
| Images Docker | GHCR, tags branche + SHA + SemVer + `latest` sur `main` |

## Stratégie Git

Flux standard :

```text
feature/* -> develop -> main
```

Règles :

- aucun push direct sur `main` ou `develop`,
- toutes les intégrations passent par Pull Request,
- `develop` reçoit le travail quotidien validé,
- `main` représente l'état publiable,
- une release officielle est créée après merge vers `main`,
- après release, `main` est resynchronisée vers `develop`.

## Conventional Commits

Format :

```text
<type>[scope optionnel][!]: description
```

Mapping release :

| Type | Effet SemVer |
|---|---|
| `feat:` | MINOR |
| `fix:`, `perf:` | PATCH |
| `feat!:` ou `BREAKING CHANGE:` | MAJOR |
| `docs:`, `chore:`, `ci:`, `style:`, `test:`, `refactor:` | Pas de release sauf breaking change |

## CI minimale

Chaque PR vers `develop` ou `main` doit exécuter :

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright <package>/
uv run bandit -r <package>/ -c pyproject.toml
uv run pip-audit
uv run pytest tests/unit/ -v --cov=<package> --cov-report=term-missing --cov-report=xml
```

Si le projet contient Docker, IaC ou déploiement cloud, la CI doit aussi lancer Trivy.

## Politique sécurité

- Bandit est bloquant.
- Trivy est bloquant sur vulnérabilités `HIGH` et `CRITICAL`.
- pip-audit est bloquant par défaut sur projet applicatif simple.
- pip-audit peut être temporairement non bloquant si une dépendance transitive lourde IA/ML impose une vulnérabilité non corrigeable immédiatement. Dans ce cas, l'exception doit être documentée.

## Release

`python-semantic-release` est la source de vérité pour :

- calculer la prochaine version,
- modifier `project.version`,
- générer `CHANGELOG.md`,
- créer le tag Git `vX.Y.Z`,
- publier la GitHub Release.

Les images Docker doivent être taggées avec :

- nom de branche,
- SHA court `git-xxxxxxx`,
- tag SemVer `vX.Y.Z`,
- `latest` uniquement sur `main`.

## Structure attendue

```text
.
├── .github/workflows/
│   ├── ci.yml
│   ├── build.yml
│   ├── release.yml
│   ├── sync-develop.yml
│   └── docs.yml
├── docs/
├── tests/
│   ├── unit/
│   └── integration/
├── <package>/
├── pyproject.toml
├── uv.lock
├── .pre-commit-config.yaml
└── .python-version
```

