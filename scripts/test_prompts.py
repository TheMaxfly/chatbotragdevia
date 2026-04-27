"""Test du prompt template avec un cas concret."""

from langchain_core.output_parsers import PydanticOutputParser

from src.prompts import build_chat_prompt, format_context
from src.retriever import build_retriever
from src.schemas import AnalyseProjet

# Setup
retriever = build_retriever()
prompt = build_chat_prompt()
parser = PydanticOutputParser(pydantic_object=AnalyseProjet)

# Cas de test : un projet réaliste
projet_test = (
    "Mon projet déploie une API FastAPI exposant un modèle de classification "
    "d'images. J'ai mis en place un pipeline GitHub Actions qui exécute mes "
    "tests pytest à chaque push, puis package l'application dans une image "
    "Docker. La base de données PostgreSQL stocke les métadonnées des images "
    "uploadées par les utilisateurs."
)

# 1. Retrieval
print("🔍 Étape 1 : Retrieval")
docs = retriever.invoke(projet_test)
print(f"   {len(docs)} documents récupérés")
for doc in docs:
    label = doc.metadata.get("code") or doc.metadata.get("terme") or "?"
    print(f"   - [{label}]")

# 2. Formatage du contexte
print("\n📝 Étape 2 : Formatage du contexte")
contexte = format_context(docs)
print(f"   Longueur : {len(contexte)} caractères")
print("   Aperçu (200 premiers car.) :")
print(f"   {contexte[:200]}...")

# 3. Construction du prompt complet
print("\n🧱 Étape 3 : Construction du prompt complet")
final_messages = prompt.format_messages(
    contexte=contexte,
    projet=projet_test,
    format_instructions=parser.get_format_instructions(),
)

print(f"   Nombre de messages : {len(final_messages)}")
for msg in final_messages:
    print(f"   - Rôle: {msg.type:8} | Longueur: {len(msg.content)} caractères")

# 4. Aperçu du prompt final
print("\n🔍 Aperçu des 500 premiers caractères du prompt 'human' :")
human_msg = final_messages[1].content
print(human_msg[:500] + "...")

print("\n✅ Prompt template fonctionnel")
