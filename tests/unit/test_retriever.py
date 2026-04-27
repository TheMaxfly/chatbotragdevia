from src.retriever import _expand_query, _infer_filter


def test_expand_query_adds_ci_cd_vocabulary() -> None:
    query = "GitHub Actions CI/CD tests automatisés"

    expanded = _expand_query(query)

    assert query in expanded
    assert "outil d'intégration continue" in expanded
    assert "livraison continue" in expanded


def test_expand_query_keeps_unknown_query_unchanged() -> None:
    query = "analyse du besoin utilisateur"

    assert _expand_query(query) == query


def test_infer_filter_detects_definition_intent() -> None:
    search_filter, intent = _infer_filter("qu'est-ce que MLOps ?")

    assert intent == "definition"
    assert search_filter == {"type": "glossaire"}


def test_infer_filter_detects_competence_intent() -> None:
    search_filter, intent = _infer_filter(
        "quelle compétence correspond aux tests automatisés ?"
    )

    assert intent == "competence"
    assert search_filter == {"type": "competence"}


def test_infer_filter_defaults_to_general() -> None:
    search_filter, intent = _infer_filter("FastAPI Docker PostgreSQL")

    assert intent == "general"
    assert search_filter is None
