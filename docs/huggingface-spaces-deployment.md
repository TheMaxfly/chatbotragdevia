# Déploiement Hugging Face Spaces

Ce déploiement utilise un Space Hugging Face avec SDK Docker.

Architecture :

```text
Hugging Face Space Docker
  ├─ Chainlit sur le port 8000
  ├─ Chroma embarqué dans l'image Docker
  ├─ embeddings sentence-transformers sur CPU
  └─ appel LLM via Hugging Face Inference Providers
```

## Prérequis

- un compte Hugging Face ;
- un token Hugging Face avec droit d'appel aux Inference Providers ;
- le dossier `chroma_db/` généré localement.

Si `chroma_db/` n'existe pas :

```bash
uv run python scripts/ingest.py
```

## Créer le Space

1. Aller sur <https://huggingface.co/new-space>.
2. Choisir un nom, par exemple `rncp-rag`.
3. Sélectionner **SDK: Docker**.
4. Choisir la visibilité souhaitée.
5. Créer le Space.

## Configurer les variables et secrets

Dans le Space, ouvrir **Settings** puis ajouter :

Secrets :

```text
HF_TOKEN=<token Hugging Face>
```

Variables :

```text
LLM_BASE_URL=https://router.huggingface.co/v1
LLM_MODEL=Qwen/Qwen3-4B-Instruct-2507
LLM_TIMEOUT=600
LLM_MAX_COMPLETION_TOKENS=1200
EMBEDDING_MODEL=intfloat/multilingual-e5-base
CHROMA_PERSIST_DIR=/app/chroma_db
CHROMA_COLLECTION=rncp_referentiel
RETRIEVER_K=12
```

`HF_TOKEN` est automatiquement lu par l'application si `LLM_API_KEY` et
`OPENAI_API_KEY` ne sont pas définies.

## Pousser le code dans le Space

Récupérer l'URL Git du Space depuis l'onglet **Files** ou **Settings**, puis :

```bash
git remote add space https://huggingface.co/spaces/<user-ou-org>/rncp-rag
git push space HEAD:main
```

Si Hugging Face demande une authentification Git, utiliser :

- username : votre identifiant Hugging Face ;
- password : votre token Hugging Face.

## Port exposé

Le `README.md` contient la configuration Space :

```yaml
sdk: docker
app_port: 8000
```

Le `Dockerfile` lance Chainlit sur `0.0.0.0:8000`.

## Points d'attention

- Le modèle local LM Studio `http://localhost:1234/v1` ne fonctionne pas depuis
  un Space Hugging Face.
- Le modèle recommandé pour commencer est
  `Qwen/Qwen3-4B-Instruct-2507`, plus adapté à une sortie JSON stricte que les
  variantes avec thinking activé.
- Le premier démarrage peut être lent : le Space doit installer les dépendances
  et télécharger le modèle d'embedding CPU.
- Le stockage gratuit d'un Space peut être réinitialisé au redémarrage, mais ici
  `chroma_db/` est embarqué dans l'image Docker.
