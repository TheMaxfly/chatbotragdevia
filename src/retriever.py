"""
Retriever LangChain pour le chatbot RNCP Dev IA.

Ce module factorise la logique de retrieval (query expansion, intent filter,
similarity search) en une classe BaseRetriever réutilisable par la chaîne LCEL.

Usage :
    from src.retriever import build_retriever

    retriever = build_retriever()
    docs = retriever.invoke("quelle compétence concerne CI/CD ?")
"""

import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import Field

# === Configuration ===
load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "rncp_referentiel")
RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))


# === Tables de patterns (factorisées depuis ingest.py) ===

QUERY_EXPANSIONS = [
    (
        re.compile(r"\bci\s*/?\s*cd\b|github actions", re.IGNORECASE),
        "outil d'intégration continue chaîne d'intégration continue livraison continue tests automatisés",
    ),
    (
        re.compile(r"\bdocker\b|conteneur|container", re.IGNORECASE),
        "packaging conteneurisation déploiement modèle environnement d'exécution",
    ),
    (
        re.compile(r"\bmlops\b", re.IGNORECASE),
        "livraison continue modèle IA déploiement maintenance monitoring feedback loop",
    ),
]

INTENT_FILTERS = [
    (
        re.compile(
            r"\b(qu['’]?\s*est[- ]ce que|définition|définis|c'est quoi)\b",
            re.IGNORECASE,
        ),
        {"type": "glossaire"},
        "definition",
    ),
    (
        re.compile(
            r"\b(compétence|competence|critère|critere|activité|activite|évaluation|evaluation|modalité|modalite)\b",
            re.IGNORECASE,
        ),
        {"type": "competence"},
        "competence",
    ),
]


# === Wrapper E5 (réutilisé depuis ingest.py) ===


class E5Embeddings(HuggingFaceEmbeddings):
    """
    HuggingFaceEmbeddings + préfixes E5 (passage:/query:).
    Identique à celui d'ingest.py — on duplique pour éviter les imports croisés
    entre src/ et scripts/.
    """

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        prefixed = [f"passage: {text}" for text in texts]
        return super().embed_documents(prefixed)

    def embed_query(self, text: str) -> list[float]:
        return super().embed_query(f"query: {text}")


# === Fonctions privées de transformation de la requête ===


def _expand_query(query: str) -> str:
    """Enrichit une requête utilisateur avec le vocabulaire du référentiel."""
    expansions = [
        expansion for pattern, expansion in QUERY_EXPANSIONS if pattern.search(query)
    ]
    if not expansions:
        return query
    return f"{query}\n\nVocabulaire associé: {' '.join(expansions)}"


def _infer_filter(query: str) -> tuple[dict | None, str]:
    """Déduit un filtre Chroma depuis l'intention de la question."""
    for pattern, search_filter, intent in INTENT_FILTERS:
        if pattern.search(query):
            return search_filter, intent
    return None, "general"


# === Le retriever LangChain ===


class RncpRetriever(BaseRetriever):
    """
    Retriever LangChain pour le référentiel RNCP avec :
        - Query expansion (synonymes vers vocabulaire du référentiel)
        - Intent filter (glossaire pour définitions, competence pour questions métier)
        - Fallback automatique sur recherche générale si filtre trop restrictif

    Cette classe respecte l'interface BaseRetriever, elle est donc utilisable
    dans une chaîne LCEL via l'opérateur | et compatible avec LangSmith.
    """

    vectorstore: Chroma = Field(...)
    k: int = Field(default=5)
    last_query_info: dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        """
        Méthode appelée par LangChain pour récupérer les documents pertinents.

        Pipeline :
        1. Expansion de la requête avec synonymes
        2. Détection de l'intention pour filtre éventuel
        3. Recherche similarity avec filtre
        4. Fallback sur recherche générale si filtre vide les résultats
        """
        expanded = _expand_query(query)
        search_filter, intent = _infer_filter(query)

        # Tentative avec filtre
        if search_filter:
            docs = self.vectorstore.similarity_search(
                expanded,
                k=self.k,
                filter=search_filter,
            )
            if docs:
                self.last_query_info = {
                    "original_query": query,
                    "expanded_query": expanded,
                    "intent": intent,
                    "filter_applied": search_filter,
                    "fallback_used": False,
                    "n_results": len(docs),
                }
                return docs

        # Fallback : recherche générale
        docs = self.vectorstore.similarity_search(expanded, k=self.k)
        self.last_query_info = {
            "original_query": query,
            "expanded_query": expanded,
            "intent": intent,
            "filter_applied": None,
            "fallback_used": search_filter is not None,
            "n_results": len(docs),
        }
        return docs


# === Factory ===


def build_retriever(k: int | None = None) -> RncpRetriever:
    """
    Crée et retourne un retriever prêt à l'emploi.

    Cette fonction charge le modèle d'embedding et ouvre la collection Chroma
    existante. À appeler UNE FOIS au démarrage de l'application (singleton).

    Args:
        k: Nombre de documents à retourner par requête. Si None, lit RETRIEVER_K.

    Returns:
        Un RncpRetriever connecté à la collection Chroma.

    Raises:
        FileNotFoundError: Si le répertoire Chroma n'existe pas (ingest non lancé).
    """
    persist_path = Path(CHROMA_PERSIST_DIR)
    if not persist_path.exists():
        raise FileNotFoundError(
            f"Répertoire Chroma introuvable : {persist_path}\n"
            f"Lance d'abord l'ingestion : uv run python scripts/ingest.py"
        )

    embeddings = E5Embeddings(
        model=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
    )

    return RncpRetriever(
        vectorstore=vectorstore,
        k=k if k is not None else RETRIEVER_K,
    )
