"""
Chaîne LCEL complète du chatbot RNCP Dev IA.

Cette chaîne connecte tous les composants construits dans les blocs précédents :
    1. Retriever (src/retriever.py)
    2. Formatage du contexte (src/prompts.py::format_context)
    3. Prompt template (src/prompts.py::build_chat_prompt)
    4. LLM (Qwen3-4B-Instruct-2507 via LM Studio)
    5. Parser Pydantic (src/schemas.py::AnalyseProjet)

Usage :
    from src.chain import build_chain, analyze_project

    chain = build_chain()
    result = analyze_project(chain, "Mon projet utilise FastAPI et Docker...")
    # result est un AnalyseProjet validé
"""

import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.prompts import build_chat_prompt, format_context
from src.retriever import RncpRetriever, build_retriever
from src.schemas import AnalyseProjet

# === Configuration LLM (chargée depuis .env) ===
load_dotenv()

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3-4b-2507")


# === Factories internes ===


def _make_llm() -> ChatOpenAI:
    """
    Construit un client ChatOpenAI pointant vers LM Studio.

    LM Studio expose une API compatible OpenAI sur localhost:1234. On utilise
    donc le même client que pour OpenAI, mais avec base_url et api_key custom.

    Le temperature=0 garantit des réponses déterministes et factuelles, ce qui
    est crucial pour un chatbot d'analyse de référentiel (pas de créativité).
    """
    return ChatOpenAI(
        base_url=LLM_BASE_URL,
        api_key=SecretStr(LLM_API_KEY),
        model=LLM_MODEL,
        temperature=0,
        timeout=180,  # Qwen3-4B sur GPU peut mettre 30-60s pour des outputs longs
        max_completion_tokens=2500,
    )


def _make_retrieve_and_format(retriever: RncpRetriever) -> Runnable:
    """
    Construit un Runnable qui :
        1. Reçoit une string (la description du projet)
        2. Appelle le retriever pour obtenir les documents pertinents
        3. Formate ces documents en contexte string lisible

    Returns:
        Un RunnableLambda qui transforme str → str (contexte formaté).
    """

    def _retrieve_and_format(query: str) -> str:
        docs: list[Document] = retriever.invoke(query)
        return format_context(docs)

    return RunnableLambda(_retrieve_and_format)


# === Construction de la chaîne complète ===


def build_chain(retriever: RncpRetriever | None = None) -> Runnable:
    """
    Construit la chaîne LCEL complète du chatbot.

    Pipeline (lecture de gauche à droite) :
        Input (str)
            │
            ├─→ [retrieve_and_format] → contexte (str)
            ├─→ [passthrough]         → projet   (str)
            └─→ [parser instructions] → format_instructions (str)
            │
            ▼
        ChatPromptTemplate (assemble system + human)
            │
            ▼
        ChatOpenAI (Qwen3-4B via LM Studio)
            │
            ▼
        PydanticOutputParser (JSON → AnalyseProjet)
            │
            ▼
        Output (AnalyseProjet)

    Args:
        retriever: Retriever pré-construit. Si None, en construit un nouveau.

    Returns:
        Un Runnable LCEL prêt à être .invoke() avec une description de projet.
    """
    # 1. Composants de base
    if retriever is None:
        retriever = build_retriever()

    llm = _make_llm()
    prompt = build_chat_prompt()
    parser = JsonOutputParser(pydantic_object=AnalyseProjet)

    # 2. Préparation des inputs du prompt
    # Le prompt attend 3 variables : contexte, projet, format_instructions
    retrieve_and_format = _make_retrieve_and_format(retriever)

    inputs = RunnableParallel(
        contexte=retrieve_and_format,
        projet=RunnablePassthrough(),
        format_instructions=RunnableLambda(lambda _: parser.get_format_instructions()),
    )

    # 3. Assemblage final via l'opérateur pipe
    chain = inputs | prompt | llm | parser

    return chain


# === Helper d'usage ===


def analyze_project(chain: Runnable, description: str) -> AnalyseProjet:
    """
    Lance l'analyse d'un projet décrit en langage naturel.

    Args:
        chain: La chaîne construite par `build_chain()`.
        description: Description du projet en langage naturel (français).

    Returns:
        Un objet AnalyseProjet validé contenant l'analyse complète.

    Raises:
        ValidationError: Si le LLM produit du JSON invalide ou hors schéma.
        Exception: Toute erreur réseau / LLM (timeout, modèle indisponible, etc.)
    """
    raw_dict = chain.invoke(description)
    return AnalyseProjet.model_validate(raw_dict)
