from langchain_core.documents import Document

from src.prompts import build_chat_prompt, format_context


def test_format_context_returns_fallback_when_no_documents() -> None:
    assert format_context([]) == (
        "(Aucun extrait du référentiel n'a été trouvé pour cette requête.)"
    )


def test_format_context_includes_metadata_and_content() -> None:
    docs = [
        Document(
            page_content="Critère d'évaluation exact.",
            metadata={"type": "competence", "code": "C18"},
        )
    ]

    context = format_context(docs)

    assert "type=competence" in context
    assert "id=C18" in context
    assert "Critère d'évaluation exact." in context


def test_build_chat_prompt_exposes_expected_variables() -> None:
    prompt = build_chat_prompt()

    assert {"contexte", "projet", "format_instructions"} <= set(prompt.input_variables)
