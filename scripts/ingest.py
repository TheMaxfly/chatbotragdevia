"""
Script d'ingestion du référentiel RNCP Dev IA dans Chroma.

Usage:
    uv run python scripts/ingest.py

Prérequis:
    - Le fichier data/referentiel_rncp.md doit exister
    - Les variables d'environnement sont définies dans .env
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

# === Chargement de la configuration ===
load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-base")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "rncp_referentiel")

# === Chemins du projet ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_PATH = PROJECT_ROOT / "data" / "referentiel_rncp.md"

# === Paramètres de chunking ===
CHUNK_MAX_SIZE = 1500  # Au-delà, on re-split par sécurité
CHUNK_OVERLAP = 150  # Recouvrement pour préserver le contexte aux frontières
SMOKE_TEST_K = 5  # Nombre de résultats contrôlés par requête de smoke test


# Synonymes utilisateur → vocabulaire métier présent dans le référentiel.
# On ajoute ces termes à la requête au lieu de remplacer la formulation initiale.
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


# === Headers Markdown sur lesquels splitter ===
HEADERS_TO_SPLIT_ON = [
    ("##", "bloc"),
    ("###", "competence"),
]


def load_and_split_markdown(markdown_path: Path) -> list:
    """
    Charge le fichier Markdown et le découpe en chunks structurés.

    Stratégie en 2 passes :
    1. Split par headers Markdown (## et ###) → 1 chunk par compétence
    2. Re-split par caractères si chunk > CHUNK_MAX_SIZE (sécurité)

    Les métadonnées `bloc` et `competence` sont préservées à travers les 2 passes.

    Returns:
        Liste de Documents LangChain avec metadata enrichies.
    """
    # Lecture brute du fichier
    print(f"📖 Lecture de {markdown_path}")
    text = markdown_path.read_text(encoding="utf-8")
    print(f"   → {len(text)} caractères lus")

    # Passe 1 : split par headers Markdown
    print("\n✂️  Passe 1 : split par headers Markdown")
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,  # On garde les headers dans le contenu pour le contexte
    )
    chunks_pass1 = md_splitter.split_text(text)
    print(f"   → {len(chunks_pass1)} chunks après split par headers")

    # Passe 2 : re-split de sécurité pour les chunks trop longs
    print(f"\n✂️  Passe 2 : re-split si chunk > {CHUNK_MAX_SIZE} caractères")
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_MAX_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks_final = char_splitter.split_documents(chunks_pass1)
    print(f"   → {len(chunks_final)} chunks après re-split éventuel")

    return chunks_final


def enrich_metadata(chunks: list) -> list:
    """
    Enrichit les métadonnées de chaque chunk en fonction de son type.

    Types détectés :
        - 'competence' : sous un bloc, titre matchant 'Compétence Cn — ...'
        - 'evaluation' : sous "Modalités d'évaluation", titre matchant 'En — ...'
        - 'glossaire'  : sous "Glossaire"
        - 'intro'      : chunk sans bloc parent (début du doc)

    Ajoute également :
        - 'code'    : 'C1', 'E2', etc. quand applicable
        - 'titre'   : le titre nettoyé sans le code
        - 'bloc_num': numéro du bloc (1, 2 ou 3) quand applicable

    Returns:
        Liste de Documents avec metadata enrichies (modifiée en place + retournée).
    """
    print("\n🏷️  Enrichissement des métadonnées")

    competence_pattern = re.compile(r"Compétence C(\d+)\s*—\s*(.+)")
    evaluation_pattern = re.compile(r"E(\d+)\s*—\s*(.+)")
    bloc_pattern = re.compile(r"Bloc\s*(\d+)\s*—")

    stats = {"competence": 0, "evaluation": 0, "glossaire": 0, "intro": 0, "autre": 0}

    for chunk in chunks:
        meta = chunk.metadata
        bloc = meta.get("bloc", "")
        item_title = meta.get("competence", "")  # nom de metadata legacy

        # --- Cas 1 : pas de bloc parent → intro/document ---
        if not bloc:
            meta["type"] = "intro"
            stats["intro"] += 1
            continue

        # --- Cas 2 : sous "Glossaire" ---
        if bloc.strip().lower().startswith("glossaire"):
            meta["type"] = "glossaire"
            meta["terme"] = item_title.strip()
            # On retire la metadata 'competence' (sémantiquement fausse)
            meta.pop("competence", None)
            stats["glossaire"] += 1
            continue

        # --- Cas 3 : sous "Modalités d'évaluation" ---
        if "évaluation" in bloc.lower() or "evaluation" in bloc.lower():
            match = evaluation_pattern.match(item_title)
            if match:
                meta["type"] = "evaluation"
                meta["code"] = f"E{match.group(1)}"
                meta["titre"] = match.group(2).strip()
                meta.pop("competence", None)
                stats["evaluation"] += 1
                continue

        # --- Cas 4 : sous un Bloc N → compétence ---
        match = competence_pattern.match(item_title)
        if match:
            meta["type"] = "competence"
            meta["code"] = f"C{match.group(1)}"
            meta["titre"] = match.group(2).strip()
            meta.pop("competence", None)

            bloc_match = bloc_pattern.search(bloc)
            if bloc_match:
                meta["bloc_num"] = int(bloc_match.group(1))

            stats["competence"] += 1
            continue

        # --- Cas 5 : fallback (intro de bloc, etc.) ---
        meta["type"] = "autre"
        stats["autre"] += 1

    # Rapport
    for type_, count in stats.items():
        print(f"   • {type_:12} : {count} chunks")

    return chunks


def add_embedding_context(chunks: list[Document]) -> list[Document]:
    """
    Ajoute les métadonnées métier au texte indexé.

    Chroma et le modèle d'embedding comparent uniquement le `page_content`.
    Les métadonnées sont utiles pour filtrer ou afficher les sources, mais elles
    n'améliorent pas directement la similarité. On les préfixe donc dans le
    contenu afin que les recherches sur "C18", "MLOps", "intégration continue",
    etc. disposent du contexte complet.

    Returns:
        Nouvelle liste de Documents avec contenu enrichi et métadonnées conservées.
    """
    print("\n🧩 Ajout du contexte métier dans le texte indexé")

    enriched_chunks = []
    for chunk in chunks:
        meta = chunk.metadata
        context_lines = []

        if meta.get("bloc"):
            context_lines.append(f"Bloc: {meta['bloc']}")
        if meta.get("type"):
            context_lines.append(f"Type: {meta['type']}")
        if meta.get("code"):
            context_lines.append(f"Code: {meta['code']}")
        if meta.get("titre"):
            context_lines.append(f"Titre: {meta['titre']}")
        if meta.get("terme"):
            context_lines.append(f"Terme: {meta['terme']}")

        if context_lines:
            page_content = "\n".join(context_lines) + "\n\n" + chunk.page_content
        else:
            page_content = chunk.page_content

        enriched_chunks.append(
            Document(
                page_content=page_content,
                metadata=dict(meta),
            )
        )

    print(f"   → {len(enriched_chunks)} chunks enrichis")
    return enriched_chunks


class E5Embeddings(HuggingFaceEmbeddings):
    """
    Wrapper autour de HuggingFaceEmbeddings qui ajoute les préfixes
    requis par les modèles E5 (intfloat/multilingual-e5-*).

    Le modèle E5 attend :
        - "passage: ..." pour les documents indexés
        - "query: ..."   pour les questions à la recherche
    """

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Préfixe les passages avant embedding."""
        prefixed = [f"passage: {text}" for text in texts]
        return super().embed_documents(prefixed)

    def embed_query(self, text: str) -> list[float]:
        """Préfixe la query avant embedding."""
        return super().embed_query(f"query: {text}")


def build_vectorstore(chunks: list[Document]) -> Chroma:
    """
    Génère les embeddings et stocke les chunks dans Chroma.

    Le vector store est persisté sur disque dans CHROMA_PERSIST_DIR.
    Si une collection du même nom existe déjà, elle est SUPPRIMÉE et recréée
    (idempotence : on peut relancer l'ingestion sans accumuler de doublons).

    Returns:
        L'instance Chroma prête à être interrogée.
    """
    print(f"\n🧮 Initialisation du modèle d'embedding : {EMBEDDING_MODEL}")
    print("   (premier chargement : téléchargement du modèle, ~440 MB)")

    embeddings = E5Embeddings(
        model=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    # Idempotence : on supprime la collection existante si présente
    print(f"\n💾 Création de la collection Chroma : {CHROMA_COLLECTION}")
    print(f"   Persistance dans : {CHROMA_PERSIST_DIR}")

    # On instancie Chroma vide pour pouvoir supprimer la collection si elle existe
    try:
        existing = Chroma(
            collection_name=CHROMA_COLLECTION,
            persist_directory=CHROMA_PERSIST_DIR,
            embedding_function=embeddings,
        )
        existing.delete_collection()
        print("   → Ancienne collection supprimée")
    except Exception:
        # Collection n'existait pas, on continue
        pass

    # Création et indexation
    print(f"\n⚙️  Embedding et indexation de {len(chunks)} chunks...")
    print("   (cela prend ~30-60 secondes sur CPU)")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    print(f"   → Collection créée avec {vectorstore._collection.count()} vecteurs")
    return vectorstore


def result_label(doc: Document) -> str:
    """Retourne le libellé principal d'un résultat pour affichage et validation."""
    meta = doc.metadata
    return meta.get("code") or meta.get("terme") or meta.get("type", "?")


def expand_query(query: str) -> str:
    """
    Enrichit une requête utilisateur avec le vocabulaire du référentiel.

    Exemple : un utilisateur peut écrire "GitHub Actions CI/CD", alors que le
    corpus parle surtout d'"outil d'intégration continue" et de "livraison
    continue". On conserve la requête originale et on ajoute ces synonymes pour
    améliorer le rappel sans perdre l'intention initiale.
    """
    expansions = []
    for pattern, expansion in QUERY_EXPANSIONS:
        if pattern.search(query):
            expansions.append(expansion)

    if not expansions:
        return query

    return f"{query}\n\nVocabulaire associé: {' '.join(expansions)}"


def infer_search_filter(query: str) -> tuple[dict | None, str]:
    """
    Déduit un filtre Chroma simple à partir de l'intention de la question.

    Le corpus mélange des chunks de compétences et des définitions du glossaire.
    Filtrer évite qu'une question de définition soit polluée par des compétences,
    ou qu'une question sur les compétences soit dominée par le glossaire.
    """
    for pattern, search_filter, intent in INTENT_FILTERS:
        if pattern.search(query):
            return search_filter, intent

    return None, "general"


def similarity_search_with_intent(
    vectorstore: Chroma,
    query: str,
    k: int = SMOKE_TEST_K,
) -> tuple[list[tuple[Document, float]], str, dict | None, str]:
    """
    Exécute une recherche avec expansion de requête et filtre d'intention.

    Si un filtre trop restrictif ne retourne aucun résultat, on retombe sur une
    recherche générale afin de ne pas bloquer le futur chatbot.
    """
    search_query = expand_query(query)
    search_filter, intent = infer_search_filter(query)

    if search_filter:
        results = vectorstore.similarity_search_with_score(
            search_query,
            k=k,
            filter=search_filter,
        )
        if results:
            return results, search_query, search_filter, intent

    results = vectorstore.similarity_search_with_score(search_query, k=k)
    return results, search_query, None, "general"


def run_smoke_tests(vectorstore: Chroma) -> bool:
    """
    Exécute des requêtes de validation avec résultats attendus.

    Le test réussit si au moins un des labels attendus apparaît dans le top K.
    Cela ne mesure pas toute la qualité du RAG, mais permet de détecter vite une
    régression grossière du retrieval.
    """
    test_cases = [
        {
            "query": "qu'est-ce que MLOps ?",
            "expected": {"MLOps", "C13"},
        },
        {
            "query": "quelle compétence concerne les tests avec une chaîne d'intégration continue ?",
            "expected": {"C18"},
        },
        {
            "query": "quelle compétence correspond à GitHub Actions CI/CD tests automatisés ?",
            "expected": {"C18"},
        },
        {
            "query": "packaging Docker déploiement modèle IA",
            "expected": {"Packaging (d'un modèle d'IA)", "C13"},
        },
    ]

    print("\n" + "=" * 60)
    print("🧪 SMOKE TEST")
    print("=" * 60)
    print(f"Validation : au moins un résultat attendu dans le top {SMOKE_TEST_K}")

    success_count = 0
    for test_case in test_cases:
        query = test_case["query"]
        expected = test_case["expected"]
        results, search_query, search_filter, intent = similarity_search_with_intent(
            vectorstore,
            query,
            k=SMOKE_TEST_K,
        )
        labels = [result_label(doc) for doc, _ in results]
        success = bool(expected.intersection(labels))

        if success:
            success_count += 1

        status = "OK" if success else "KO"
        print(f"\n{status} Query : {query!r}")
        print(f"   Intention : {intent}")
        if search_filter:
            print(f"   Filtre   : {search_filter}")
        if search_query != query:
            expanded_preview = " ".join(search_query.split())
            print(f"   Requête enrichie : {expanded_preview}")
        print(f"   Attendu : {', '.join(sorted(expected))}")
        print(f"   Obtenu  : {', '.join(labels)}")

        for i, (doc, score) in enumerate(results, 1):
            label = result_label(doc)
            preview = " ".join(doc.page_content.split())[:120]
            print(f"   {i}. [score={score:.3f}] [{label}] {preview}...")

    print(f"\nRésultat smoke test : {success_count}/{len(test_cases)} OK")
    return success_count == len(test_cases)


# === Bloc de test temporaire ===
if __name__ == "__main__":
    # Étape 1 : split du markdown
    chunks = load_and_split_markdown(MARKDOWN_PATH)

    # Étape 2 : enrichissement des métadonnées
    chunks = enrich_metadata(chunks)

    # Étape 3 : ajout du contexte métier dans le texte indexé
    chunks = add_embedding_context(chunks)

    # Étape 4 : embedding et indexation
    vectorstore = build_vectorstore(chunks)

    # Étape 5 : smoke test mesurable
    smoke_ok = run_smoke_tests(vectorstore)

    if not smoke_ok:
        raise SystemExit("❌ Smoke test échoué")

    print("\n✅ Ingestion terminée avec succès")
