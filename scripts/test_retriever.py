import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


"""Test rapide du retriever standalone."""


def main() -> None:
    from src.retriever import build_retriever

    print("🔧 Construction du retriever...")
    retriever = build_retriever()
    print(f"   ✓ Retriever prêt (k={retriever.k})")

    queries = [
        "qu'est-ce que MLOps ?",
        "quelle compétence concerne les tests automatisés ?",
        "GitHub Actions CI/CD",
        "FastAPI exposition de données",
    ]

    for query in queries:
        print(f"\n❓ Query : {query!r}")
        docs = retriever.invoke(query)

        info = retriever.last_query_info
        print(f"   Intention : {info['intent']}")
        print(f"   Filtre    : {info['filter_applied']}")
        if info["fallback_used"]:
            print("   ⚠️  Fallback utilisé (filtre n'a rien retourné)")

        for i, doc in enumerate(docs, 1):
            meta = doc.metadata
            label = meta.get("code") or meta.get("terme") or meta.get("type", "?")
            preview = " ".join(doc.page_content.split())[:80]
            print(f"   {i}. [{label}] {preview}...")

    print("\n✅ Retriever fonctionnel")


if __name__ == "__main__":
    main()
