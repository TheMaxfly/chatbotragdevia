# Déploiement Azure Container Apps

Ce projet est une application Chainlit containerisée. La cible recommandée pour
un premier déploiement est Azure Container Apps :

- image Docker stockée dans Azure Container Registry ;
- secret Azure Container Apps pour `OPENAI_API_KEY` ;
- ingress HTTP public vers le port `8000` ;
- index Chroma embarqué dans l'image Azure via `Dockerfile.azure`.

## Prérequis

- un compte Azure ;
- un groupe de ressources existant ;
- Azure CLI installé, ou Azure Cloud Shell ;
- le dossier `chroma_db/` généré localement ;
- une clé API OpenAI.

Si `chroma_db/` n'existe pas :

```bash
uv run python scripts/ingest.py
```

## Déployer

Définir les variables nécessaires :

```bash
export AZURE_RESOURCE_GROUP="<nom-du-groupe-de-ressources>"
export AZURE_LOCATION="francecentral"
export AZURE_ACR_NAME="<nom-acr-unique-en-minuscules>"
export AZURE_CONTAINERAPP_ENV="rncp-rag-env"
export AZURE_CONTAINERAPP_NAME="rncp-rag"

export OPENAI_API_KEY="sk-..."
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="<modele-openai>"
```

Puis lancer :

```bash
bash scripts/deploy_azure_container_apps.sh
```

Le script :

1. vérifie la connexion Azure CLI ;
2. crée l'Azure Container Registry si nécessaire ;
3. build et push l'image avec `Dockerfile.azure` ;
4. crée l'environnement Azure Container Apps si nécessaire ;
5. crée ou met à jour la Container App ;
6. affiche l'URL publique.

## Pourquoi un Dockerfile Azure séparé ?

Le `Dockerfile` local garde `chroma_db/` hors image et le monte en volume.
C'est mieux pour le développement.

Sur Azure Container Apps, pour un premier déploiement simple, `Dockerfile.azure`
embarque `chroma_db/` dans l'image. Cela évite de configurer Azure Files ou un
job d'ingestion séparé.

## Points d'attention

- `AZURE_ACR_NAME` doit être globalement unique, en minuscules, sans tirets.
- Le script active l'admin user ACR pour simplifier le premier déploiement.
  Pour une version production, utiliser plutôt une managed identity.
- Le container utilise les embeddings sur CPU pour préserver la mémoire GPU et
  parce qu'Azure Container Apps standard ne fournit pas de GPU.
- L'image actuelle peut être volumineuse car le lock Python installe PyTorch
  avec des dépendances CUDA. Elle fonctionne, mais une image CPU-only serait
  préférable pour réduire le temps de build et de pull.
