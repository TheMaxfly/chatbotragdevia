#!/usr/bin/env bash
set -euo pipefail

require_env() {
  local name="$1"
  if [[ -z "${!name:-}" ]]; then
    echo "Variable requise manquante: ${name}" >&2
    exit 1
  fi
}

require_cmd() {
  local name="$1"
  if ! command -v "${name}" >/dev/null 2>&1; then
    echo "Commande introuvable: ${name}" >&2
    exit 1
  fi
}

require_cmd az

require_env AZURE_RESOURCE_GROUP
require_env AZURE_ACR_NAME
require_env OPENAI_API_KEY
require_env LLM_MODEL

AZURE_LOCATION="${AZURE_LOCATION:-francecentral}"
AZURE_CONTAINERAPP_ENV="${AZURE_CONTAINERAPP_ENV:-rncp-rag-env}"
AZURE_CONTAINERAPP_NAME="${AZURE_CONTAINERAPP_NAME:-rncp-rag}"
AZURE_IMAGE_NAME="${AZURE_IMAGE_NAME:-rncp-rag}"
AZURE_IMAGE_TAG="${AZURE_IMAGE_TAG:-$(date +%Y%m%d%H%M%S)}"
LLM_BASE_URL="${LLM_BASE_URL:-https://api.openai.com/v1}"
LLM_TIMEOUT="${LLM_TIMEOUT:-600}"
LLM_MAX_COMPLETION_TOKENS="${LLM_MAX_COMPLETION_TOKENS:-1200}"
EMBEDDING_MODEL="${EMBEDDING_MODEL:-intfloat/multilingual-e5-base}"
RETRIEVER_K="${RETRIEVER_K:-5}"

if [[ ! -d chroma_db ]]; then
  echo "Le dossier chroma_db est introuvable. Lance d'abord: uv run python scripts/ingest.py" >&2
  exit 1
fi

az account show >/dev/null
az extension add --name containerapp --upgrade --only-show-errors >/dev/null

if ! az acr show --name "${AZURE_ACR_NAME}" --resource-group "${AZURE_RESOURCE_GROUP}" >/dev/null 2>&1; then
  az acr create \
    --name "${AZURE_ACR_NAME}" \
    --resource-group "${AZURE_RESOURCE_GROUP}" \
    --location "${AZURE_LOCATION}" \
    --sku Basic
fi

az acr update --name "${AZURE_ACR_NAME}" --admin-enabled true >/dev/null

ACR_LOGIN_SERVER="$(az acr show --name "${AZURE_ACR_NAME}" --query loginServer -o tsv)"
ACR_USERNAME="$(az acr credential show --name "${AZURE_ACR_NAME}" --query username -o tsv)"
ACR_PASSWORD="$(az acr credential show --name "${AZURE_ACR_NAME}" --query passwords[0].value -o tsv)"
IMAGE="${ACR_LOGIN_SERVER}/${AZURE_IMAGE_NAME}:${AZURE_IMAGE_TAG}"

az acr build \
  --registry "${AZURE_ACR_NAME}" \
  --image "${AZURE_IMAGE_NAME}:${AZURE_IMAGE_TAG}" \
  --file Dockerfile.azure \
  .

if ! az containerapp env show --name "${AZURE_CONTAINERAPP_ENV}" --resource-group "${AZURE_RESOURCE_GROUP}" >/dev/null 2>&1; then
  az containerapp env create \
    --name "${AZURE_CONTAINERAPP_ENV}" \
    --resource-group "${AZURE_RESOURCE_GROUP}" \
    --location "${AZURE_LOCATION}"
fi

if ! az containerapp show --name "${AZURE_CONTAINERAPP_NAME}" --resource-group "${AZURE_RESOURCE_GROUP}" >/dev/null 2>&1; then
  az containerapp create \
    --name "${AZURE_CONTAINERAPP_NAME}" \
    --resource-group "${AZURE_RESOURCE_GROUP}" \
    --environment "${AZURE_CONTAINERAPP_ENV}" \
    --image "${IMAGE}" \
    --registry-server "${ACR_LOGIN_SERVER}" \
    --registry-username "${ACR_USERNAME}" \
    --registry-password "${ACR_PASSWORD}" \
    --target-port 8000 \
    --ingress external \
    --cpu 2 \
    --memory 4Gi \
    --min-replicas 1 \
    --max-replicas 1 \
    --secrets "openai-api-key=${OPENAI_API_KEY}" \
    --env-vars \
      "OPENAI_API_KEY=secretref:openai-api-key" \
      "LLM_BASE_URL=${LLM_BASE_URL}" \
      "LLM_MODEL=${LLM_MODEL}" \
      "LLM_TIMEOUT=${LLM_TIMEOUT}" \
      "LLM_MAX_COMPLETION_TOKENS=${LLM_MAX_COMPLETION_TOKENS}" \
      "EMBEDDING_MODEL=${EMBEDDING_MODEL}" \
      "CHROMA_PERSIST_DIR=/app/chroma_db" \
      "CHROMA_COLLECTION=rncp_referentiel" \
      "RETRIEVER_K=${RETRIEVER_K}"
else
  az containerapp secret set \
    --name "${AZURE_CONTAINERAPP_NAME}" \
    --resource-group "${AZURE_RESOURCE_GROUP}" \
    --secrets "openai-api-key=${OPENAI_API_KEY}"

  az containerapp update \
    --name "${AZURE_CONTAINERAPP_NAME}" \
    --resource-group "${AZURE_RESOURCE_GROUP}" \
    --image "${IMAGE}" \
    --set-env-vars \
      "OPENAI_API_KEY=secretref:openai-api-key" \
      "LLM_BASE_URL=${LLM_BASE_URL}" \
      "LLM_MODEL=${LLM_MODEL}" \
      "LLM_TIMEOUT=${LLM_TIMEOUT}" \
      "LLM_MAX_COMPLETION_TOKENS=${LLM_MAX_COMPLETION_TOKENS}" \
      "EMBEDDING_MODEL=${EMBEDDING_MODEL}" \
      "CHROMA_PERSIST_DIR=/app/chroma_db" \
      "CHROMA_COLLECTION=rncp_referentiel" \
      "RETRIEVER_K=${RETRIEVER_K}" \
      "AZURE_IMAGE_TAG=${AZURE_IMAGE_TAG}"
fi

FQDN="$(az containerapp show \
  --name "${AZURE_CONTAINERAPP_NAME}" \
  --resource-group "${AZURE_RESOURCE_GROUP}" \
  --query properties.configuration.ingress.fqdn \
  -o tsv)"

echo "Déploiement terminé: https://${FQDN}"
