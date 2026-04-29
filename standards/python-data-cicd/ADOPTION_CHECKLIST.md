# Checklist d'adoption

Utiliser cette checklist au démarrage d'un nouveau projet ou lors de la mise à niveau d'un projet existant.

## Initialisation

- [ ] Créer ou vérifier `pyproject.toml`.
- [ ] Définir `requires-python`.
- [ ] Ajouter les dépendances dev : `ruff`, `pyright`, `pytest`, `pytest-cov`, `bandit`, `pip-audit`, `pre-commit`, `python-semantic-release`.
- [ ] Générer et versionner `uv.lock`.
- [ ] Ajouter `.python-version`.
- [ ] Ajouter `.pre-commit-config.yaml`.

## Qualité

- [ ] Configurer `[tool.ruff]`.
- [ ] Configurer `[tool.ruff.lint]`.
- [ ] Configurer `[tool.ruff.format]`.
- [ ] Configurer `[tool.pyright]`.
- [ ] Configurer `[tool.pytest.ini_options]`.
- [ ] Configurer `[tool.bandit]`.
- [ ] Lancer `uv run pre-commit run --all-files`.

## CI/CD

- [ ] Copier `template/.github/workflows/ci.yml`.
- [ ] Remplacer `your_package` par le nom réel du package.
- [ ] Activer la CI sur `develop` et `main`.
- [ ] Copier `build.yml` si le projet a une image Docker.
- [ ] Ajouter Trivy si Docker, IaC ou déploiement cloud.
- [ ] Copier `release.yml`.
- [ ] Copier `sync-develop.yml`.
- [ ] Copier `docs.yml` si MkDocs est utilisé.

## Branches

- [ ] Créer `develop`.
- [ ] Protéger `main`.
- [ ] Protéger `develop`.
- [ ] Exiger une PR avant merge.
- [ ] Exiger la CI verte avant merge.
- [ ] Interdire le push direct sur `main`.

## Release

- [ ] Configurer `[tool.semantic_release]`.
- [ ] Vérifier que `version_toml` pointe vers `pyproject.toml:project.version`.
- [ ] Vérifier que `CHANGELOG.md` est généré.
- [ ] Vérifier que les commits respectent Conventional Commits.
- [ ] Tester avec `uv run semantic-release version --print`.
- [ ] Vérifier que les images Docker reçoivent le tag `vX.Y.Z`.
