# Assistant RAG RNCP Dev IA

Assistant conversationnel pour aider les formateurs et apprenants Simplon à analyser la couverture d'un projet par rapport au référentiel RNCP **Développeur en Intelligence Artificielle**.

## Problème traité

Chez Simplon, une question revient souvent avant les soutenances :

> Est-ce que mon projet couvre bien les compétences du référentiel RNCP Dev IA ?

Aujourd'hui, répondre à cette question demande de relire manuellement un PDF de 40+ pages, de retrouver les compétences, les activités et les critères d'évaluation, puis de comparer ces éléments avec ce que le projet implémente réellement.

Ce projet vise à construire un assistant capable de répondre à des questions comme :

- "Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?"
- "La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans CI/CD ?"
- "Quelles compétences me manquent pour valider le bloc MLOps ?"

L'objectif est de fournir une réponse structurée, justifiée par des extraits du référentiel, sans inventer de compétences absentes du document source.

## État du projet

Le dépôt contient actuellement le socle RAG :

- conversion du référentiel PDF en Markdown dans `data/referentiel_rncp.md`
- découpage du Markdown en chunks structurés
- enrichissement des métadonnées RNCP (`bloc`, `type`, `code`, `titre`, `terme`)
- génération d'embeddings avec un modèle local Hugging Face
- stockage persistant dans Chroma
- smoke tests mesurables sur la pertinence du retriever
- expansion de requêtes utilisateur (`CI/CD`, `GitHub Actions`, `Docker`, `MLOps`)
- filtrage simple par intention (`glossaire`, `competence`, recherche générale)

L'interface conversationnelle reste à brancher sur ce socle. Le contexte projet mentionne Chainlit, et le `pyproject.toml` contient déjà la dépendance `chainlit`. Si l'évaluation impose Gradio, l'interface pourra être adaptée, mais le pipeline RAG reste identique.

## Architecture RAG

```text
PDF RNCP
   |
   v
Markdown nettoyé
   |
   v
Découpage Markdown
   |
   v
Chunks + métadonnées RNCP
   |
   v
Embeddings Hugging Face E5
   |
   v
Vector store Chroma persistant
   |
   v
Retriever avec expansion + filtres d'intention
   |
   v
Prompt enrichi avec sources
   |
   v
LLM local via LM Studio ou autre backend compatible OpenAI
   |
   v
Réponse argumentée avec compétences et extraits
```

Le principe est le suivant :

1. Le référentiel est converti en Markdown pour faciliter le découpage.
2. Le script d'ingestion découpe le document par titres Markdown (`##`, `###`).
3. Chaque chunk est enrichi avec des métadonnées métier : bloc, compétence, code, titre, type.
4. Le texte indexé est préfixé avec ces métadonnées pour améliorer la recherche vectorielle.
5. Les embeddings sont générés avec `intfloat/multilingual-e5-base`.
6. Les vecteurs sont stockés dans Chroma, dans le dossier `chroma_db/`.
7. Une requête utilisateur est enrichie avec du vocabulaire métier avant la recherche.
8. Un filtre d'intention peut limiter la recherche au glossaire ou aux compétences.
9. Les passages récupérés servent ensuite de contexte au LLM.

## Technologies utilisées

- **Python 3.12**
- **LangChain** : orchestration du pipeline RAG
- **LangChain Chroma** : intégration Chroma
- **ChromaDB** : vector store persistant
- **Hugging Face / sentence-transformers** : embeddings locaux
- **Modèle d'embedding** : `intfloat/multilingual-e5-base`
- **LM Studio** : exécution d'un LLM local via API compatible OpenAI
- **Chainlit** : interface conversationnelle prévue pour la démonstration
- **uv** : gestion de l'environnement et des dépendances

## Structure du dépôt

```text
.
├── data/
│   └── referentiel_rncp.md       # Référentiel RNCP converti en Markdown
├── scripts/
│   └── ingest.py                 # Ingestion, embeddings, Chroma, smoke tests
├── .env.example                  # Variables d'environnement à copier
├── .gitignore
├── pyproject.toml                # Dépendances Python
├── uv.lock
└── README.md
```

Les fichiers suivants sont générés localement et ne doivent pas être commités :

- `.env`
- `.venv/`
- `chroma_db/`
- fichiers PDF source dans `data/*.pdf`

## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd rncp-rag
```

### 2. Installer les dépendances

```bash
uv sync
```

### 3. Configurer l'environnement

```bash
cp .env.example .env
```

Variables principales :

```env
# LM Studio ou serveur compatible OpenAI
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=lm-studio
LLM_MODEL=qwen/qwen3-4b-2507

# Embeddings
EMBEDDING_MODEL=intfloat/multilingual-e5-base

# Chroma
CHROMA_PERSIST_DIR=./chroma_db
CHROMA_COLLECTION=rncp_referentiel

# RAG
RETRIEVER_K=5
```

## Générer l'index vectoriel

Lancer l'ingestion :

```bash
uv run python scripts/ingest.py
```

Le script effectue les étapes suivantes :

- lit `data/referentiel_rncp.md`
- découpe le document en chunks
- enrichit les métadonnées
- ajoute le contexte métier au texte indexé
- génère les embeddings
- recrée la collection Chroma
- lance un smoke test du retriever

Sortie attendue :

```text
Résultat smoke test : 4/4 OK
✅ Ingestion terminée avec succès
```

## Smoke tests actuels

Le script teste notamment :

```text
qu'est-ce que MLOps ?
```

Résultat attendu : `MLOps` ou `C13`.

```text
quelle compétence concerne les tests avec une chaîne d'intégration continue ?
```

Résultat attendu : `C18`.

```text
quelle compétence correspond à GitHub Actions CI/CD tests automatisés ?
```

Résultat attendu : `C18`.

```text
packaging Docker déploiement modèle IA
```

Résultat attendu : `Packaging (d'un modèle d'IA)` ou `C13`.

Ces tests ne prouvent pas toute la qualité du chatbot, mais ils permettent de vérifier que le retriever retourne des passages cohérents avant de brancher le LLM.

## Lancement de l'interface

L'interface conversationnelle n'est pas encore présente dans le dépôt. La cible recommandée pour ce projet est Chainlit, déjà déclaré dans les dépendances.

Commande prévue une fois l'application ajoutée :

```bash
uv run chainlit run app.py
```

Pour une version Gradio, le même pipeline RAG pourra être appelé depuis une fonction `respond(message, history)`.

## Qualité, tests et CI/CD

Le projet applique le standard `standards/python-data-cicd` :

- Ruff pour le lint et le formatage
- Pyright pour le typage statique
- Pytest et pytest-cov pour les tests unitaires
- Bandit et pip-audit pour la sécurité
- pre-commit pour les hooks locaux
- GitHub Actions pour la CI
- python-semantic-release pour les releases SemVer

Installation des hooks locaux :

```bash
uv run pre-commit install
```

Commandes utiles :

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright src/
uv run bandit -r src/ -c pyproject.toml
uv run pip-audit
uv run pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-report=xml
```

Audit complet du standard :

```bash
standards/python-data-cicd/scripts/audit-standard.sh src
```

Les workflows GitHub sont dans `.github/workflows/` :

- `ci.yml` : lint, format, typage, sécurité, tests, pre-commit
- `build.yml` : build/push Docker si un `Dockerfile` est présent
- `release.yml` : release SemVer après CI verte sur `main`
- `sync-develop.yml` : resynchronisation de `develop` après release

## Scénarios de démonstration

### Scénario 1 : projet API + Docker + CI/CD

Question :

```text
Mon projet expose un modèle avec une API FastAPI, contient un Dockerfile et lance les tests avec GitHub Actions. Quelles compétences RNCP couvre-t-il ?
```

Réponse attendue :

- identifier des compétences liées à l'API et à l'intégration dans une application
- identifier les compétences liées aux tests automatisés et à l'intégration continue
- discuter la livraison continue si le pipeline va au-delà des tests
- citer les extraits du référentiel utilisés

### Scénario 2 : validation partielle de C13

Question :

```text
La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans pipeline CI/CD ?
```

Réponse attendue :

- expliquer que le Dockerfile peut contribuer au packaging ou au déploiement
- signaler que C13 demande une chaîne de livraison continue
- mentionner les éléments manquants : déclencheurs, tests, entraînement/validation, livraison, documentation
- éviter de valider complètement C13 sans preuves suffisantes

## Critères de qualité visés

### Architecture RAG

- le référentiel est chargé et découpé correctement
- les chunks conservent les métadonnées RNCP utiles
- les embeddings sont générés localement
- Chroma persiste l'index vectoriel
- le retriever retourne des passages pertinents
- le LLM reçoit uniquement des extraits récupérés comme contexte

### Qualité des réponses

- les compétences couvertes sont identifiées avec leur code (`C13`, `C18`, etc.)
- chaque compétence est justifiée par un extrait du référentiel
- les compétences non couvertes sont mentionnées explicitement
- le modèle ne doit pas inventer de compétence absente du référentiel
- les limites de validation doivent être expliquées quand les informations du projet sont insuffisantes

### Interface

- interface simple utilisable sans connaissance technique
- zone de saisie claire
- réponse lisible et structurée
- affichage des sources utilisées
- gestion des erreurs sans crash de l'application

## Améliorations prévues

- ajouter l'application Chainlit
- afficher les sources sous chaque réponse
- ajouter un historique multi-tours
- ajouter un score de confiance par compétence
- ajouter un mode debug pour inspecter les chunks récupérés
- ajouter un Dockerfile
- ajouter un déploiement Hugging Face Spaces, Render ou équivalent
- ajouter un support Ollama pour un fonctionnement 100% local

## Auteur

Projet étudiant réalisé dans le cadre de la formation Simplon **Développeur en Intelligence Artificielle**.

Auteur : à compléter.
