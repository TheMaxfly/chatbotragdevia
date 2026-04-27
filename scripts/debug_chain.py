"""Debug : intercepte la sortie brute du LLM avant parsing."""

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from src.chain import _make_llm, _make_retrieve_and_format
from src.prompts import build_chat_prompt
from src.retriever import build_retriever
from src.schemas import AnalyseProjet

# Setup identique à build_chain() MAIS sans le parser final
retriever = build_retriever()
llm = _make_llm()
prompt = build_chat_prompt()
parser = PydanticOutputParser(pydantic_object=AnalyseProjet)
retrieve_and_format = _make_retrieve_and_format(retriever)

inputs = RunnableParallel(
    contexte=retrieve_and_format,
    projet=RunnablePassthrough(),
    format_instructions=RunnableLambda(lambda _: parser.get_format_instructions()),
)

# Chaîne SANS le parser : on s'arrête juste après le LLM
chain_raw = inputs | prompt | llm

# Cas de test
projet_test = """
Mon projet est une application web FastAPI exposant un modèle de classification
d'images. Pipeline GitHub Actions, packaging Docker, base PostgreSQL, monitoring
Prometheus.
"""

print("🚀 Lancement avec interception de la sortie brute...")
result = chain_raw.invoke(projet_test)

print("\n" + "=" * 60)
print("📦 SORTIE BRUTE DU LLM")
print("=" * 60)
print(f"Type Python : {type(result).__name__}")
print(
    f"Longueur du content : {len(result.content) if hasattr(result, 'content') else 'N/A'}"
)
print("\n--- Contenu brut ---")
print(result.content if hasattr(result, "content") else result)
print("\n--- Fin du contenu brut ---")
