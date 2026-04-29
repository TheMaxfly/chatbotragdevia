"""Interface Chainlit pour l'assistant RAG RNCP Dev IA."""

import traceback

import chainlit as cl

from src.chain import analyze_project, build_chain
from src.rendering import render_analyse
from src.retriever import RncpRetriever, build_retriever

MIN_PROJECT_DESCRIPTION_LENGTH = 40


WELCOME_MESSAGE = """# Assistant RNCP Dev IA

Décris ton projet en langage naturel, puis clique sur **Analyser**.

L'assistant compare ta description avec le référentiel RNCP Dev IA et retourne :

- les compétences couvertes ;
- les blocs concernés ;
- les compétences manquantes pertinentes ;
- une justification basée sur les extraits du référentiel.
"""


EXAMPLE_PROJECT = """Mon projet expose un modèle de classification d'images via une API FastAPI.
J'utilise PostgreSQL pour stocker les métadonnées, Docker pour packager
l'application et GitHub Actions pour lancer les tests pytest à chaque push.
J'ai aussi mis en place Prometheus et Grafana pour surveiller l'application."""


def _get_retriever() -> RncpRetriever | None:
    """Récupère le retriever stocké dans la session Chainlit."""
    retriever = cl.user_session.get("retriever")
    return retriever if isinstance(retriever, RncpRetriever) else None


async def _ensure_retriever() -> RncpRetriever:
    """
    Construit le retriever une seule fois par session utilisateur.

    On ne met pas la chaîne complète en cache car elle contient ChatOpenAI et
    son client HTTP interne. Chainlit peut réutiliser la session après une
    reconnexion, alors on garde seulement Chroma/embeddings et on recrée le LLM
    à chaque analyse.
    """
    retriever = _get_retriever()
    if retriever is not None:
        return retriever

    retriever = await cl.make_async(build_retriever)()
    cl.user_session.set("retriever", retriever)
    return retriever


async def _send_analyze_action(project_description: str) -> None:
    """Affiche le bouton d'analyse pour la dernière description reçue."""
    cl.user_session.set("pending_project_description", project_description)

    await cl.Message(
        content=(
            "Description reçue. Clique sur **Analyser** pour lancer la comparaison "
            "avec le référentiel RNCP."
        ),
        actions=[
            cl.Action(
                name="analyze_project",
                label="Analyser",
                tooltip="Analyser la couverture RNCP du projet",
                payload={},
            )
        ],
    ).send()


@cl.set_starters
async def set_starters(user: cl.User | None, language: str | None) -> list[cl.Starter]:
    """Propose un scénario prêt à tester dans l'interface."""
    del user, language
    return [
        cl.Starter(
            label="Projet API + Docker + CI",
            message=EXAMPLE_PROJECT,
            icon="square-pen",
        )
    ]


@cl.on_chat_start
async def on_chat_start() -> None:
    """Initialise l'écran d'accueil."""
    cl.user_session.set("retriever", None)
    cl.user_session.set("pending_project_description", None)
    await cl.Message(content=WELCOME_MESSAGE).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Reçoit la description du projet et affiche le bouton Analyser."""
    project_description = str(message.content).strip()

    if len(project_description) < MIN_PROJECT_DESCRIPTION_LENGTH:
        await cl.Message(
            content=(
                "La description est trop courte pour une analyse fiable. "
                "Ajoute les technologies, données, modèles, tests, déploiement "
                "et éléments de conformité présents dans ton projet."
            )
        ).send()
        return

    await _send_analyze_action(project_description)


@cl.action_callback("analyze_project")
async def on_analyze_project(action: cl.Action) -> None:
    """Lance la chaîne RAG puis affiche le rendu Markdown."""
    project_description = cl.user_session.get("pending_project_description")
    if not isinstance(project_description, str) or not project_description.strip():
        await cl.Message(
            content="Aucune description de projet n'est disponible. Colle d'abord ton projet dans la zone de texte."
        ).send()
        return

    await cl.Message(content="Analyse RNCP en cours...").send()

    try:
        retriever = await _ensure_retriever()
        chain = build_chain(retriever)
        analyse = await cl.make_async(analyze_project)(chain, project_description)
        markdown = render_analyse(analyse)
        await cl.Message(content=markdown).send()
    except FileNotFoundError:
        await cl.Message(
            content=(
                "L'index Chroma est introuvable. Lance d'abord l'ingestion :\n\n"
                "```bash\nuv run python scripts/ingest.py\n```"
            )
        ).send()
    except Exception as exc:
        traceback.print_exc()
        await cl.Message(
            content=(
                "L'analyse a échoué. Vérifie que LM Studio est lancé, que le modèle "
                "local est chargé et que les variables `.env` sont correctes.\n\n"
                f"**Erreur** : `{type(exc).__name__}: {exc}`"
            )
        ).send()
