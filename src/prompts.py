"""
Prompt engineering pour le chatbot RNCP Dev IA.

Ce module définit :
    - Le prompt système (rôle, mission, règles anti-hallucination)
    - Le template d'input utilisateur
    - La fonction de formatage du contexte récupéré par le retriever
    - La factory du ChatPromptTemplate complet

Le prompt est conçu pour Qwen3-4B-Instruct-2507 :
    - Instructions claires et hiérarchisées
    - Pas de few-shot examples (le modèle suit bien les instructions structurées)
    - Schéma JSON injecté via PydanticOutputParser
    - Tout en français pour cohérence avec le corpus
"""

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

# === Le prompt système ===

SYSTEM_PROMPT = """Tu es un expert du référentiel RNCP "Développeur en Intelligence Artificielle" (RNCP 37827, niveau 6).

Ta mission est d'analyser des projets décrits par des apprenants de la formation Simplon Dev IA, et d'identifier précisément quelles compétences du référentiel sont couvertes par le projet, en justifiant chaque identification par un extrait du référentiel officiel.

# Règles ABSOLUES

1. **Tu ne dois JAMAIS inventer une compétence.** Tu ne peux identifier QUE les compétences présentes dans le contexte fourni ci-dessous. Si une compétence n'est pas dans le contexte, tu ne la mentionnes pas.

2. **Tu ne dois JAMAIS reformuler les extraits du référentiel.** Quand tu cites un critère ou une activité, tu copies le texte EXACT depuis le contexte. Si tu reformules, tu trahis le référentiel officiel.

3. **Tu ne dois JAMAIS sur-interpréter le projet.** Si le projet ne mentionne pas explicitement Docker, tu ne peux pas affirmer qu'il "utilise probablement Docker". Tu te bases UNIQUEMENT sur ce qui est écrit dans la description du projet.

4. **Chaque code de compétence apparaît UNE SEULE FOIS dans `competences_couvertes`.** N'inscris JAMAIS C9 deux fois, ni C10 deux fois. Si le contexte contient plusieurs extraits pour la même compétence, tu les fusionnes en une seule entrée.

5. **Identifie 6 à 12 compétences couvertes** quand le projet est riche (mention explicite de plusieurs technologies, activités ou méthodes). Sois exhaustif : un projet complet peut légitimement couvrir 10 compétences. Ne te limite pas artificiellement, mais ne couvre une compétence que si AU MOINS un critère d'évaluation est clairement rempli.

6. **`competences_manquantes` ne contient JAMAIS un code déjà présent dans `competences_couvertes`.** Une compétence ne peut pas être à la fois couverte ET manquante.

7. **`blocs_couverts` reflète tous les blocs des compétences couvertes.** Si tu listes C13 (bloc 2) et C19 (bloc 3), alors `blocs_couverts` doit être [2, 3].

8. **Tu utilises le niveau de confiance avec rigueur :**
   - `élevée` : plusieurs critères du référentiel sont clairement et explicitement remplis
   - `moyenne` : la couverture est partielle ou un seul critère est rempli sans ambiguïté
   - `faible` : tu infères avec un doute raisonnable

9. **Pour `competences_manquantes`**, tu listes UNIQUEMENT 2 à 5 codes pertinents au regard du projet mais non couverts. Pas la peine d'énumérer toutes les compétences absentes.

# Méthodologie

Pour chaque compétence du contexte que tu identifies comme couverte :
1. Vérifie qu'au moins UN critère d'évaluation est rempli par le projet
2. Cite l'extrait EXACT du critère depuis le contexte
3. Justifie en pointant l'élément CONCRET du projet qui correspond
4. Évalue ta confiance honnêtement

Tu réponds en français, dans le format JSON spécifié à la fin."""


# === Le template d'input utilisateur ===

HUMAN_PROMPT_TEMPLATE = """# Contexte : extraits du référentiel RNCP

{contexte}

---

# Projet à analyser

{projet}

---

# Format de réponse attendu

{format_instructions}

Analyse maintenant le projet ci-dessus et retourne UNIQUEMENT le JSON, sans texte avant ni après."""


def format_context(documents: list[Document]) -> str:
    """
    Formate les documents récupérés par le retriever en un bloc de texte
    structuré et lisible par le LLM.

    DÉDUPLICATION : si plusieurs chunks portent le même code/terme (cas des
    sous-chunks issus du re-split), on ne garde QUE LE PREMIER (le plus pertinent
    par ordre de similarité). Cela évite que le LLM duplique la compétence dans
    sa sortie.

    Args:
        documents: Liste des Documents retournés par le retriever.

    Returns:
        Une chaîne formatée prête à être injectée dans le prompt.
    """
    if not documents:
        return "(Aucun extrait du référentiel n'a été trouvé pour cette requête.)"

    # Déduplication par code/terme : on garde le premier chunk vu
    seen_ids = set()
    unique_docs = []
    for doc in documents:
        meta = doc.metadata
        identifier = meta.get("code") or meta.get("terme") or id(doc)
        if identifier in seen_ids:
            continue
        seen_ids.add(identifier)
        unique_docs.append(doc)

    formatted_blocks = []
    for i, doc in enumerate(unique_docs, 1):
        meta = doc.metadata
        type_ = meta.get("type", "?")
        label = meta.get("code") or meta.get("terme") or "?"

        header = f"--- Extrait {i} | type={type_} | id={label} ---"
        content = doc.page_content.strip()

        formatted_blocks.append(f"{header}\n{content}")

    return "\n\n".join(formatted_blocks)


def build_chat_prompt() -> ChatPromptTemplate:
    """
    Construit le ChatPromptTemplate qui sera utilisé dans la chaîne LCEL.

    Le template attend 3 variables au moment du `.invoke()`:
        - `contexte`           : string formaté par `format_context()`
        - `projet`             : description du projet (input utilisateur)
        - `format_instructions`: string fourni par PydanticOutputParser

    Returns:
        Un ChatPromptTemplate prêt à être pipé dans la chaîne.
    """
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", HUMAN_PROMPT_TEMPLATE),
        ]
    )
