"""
Rendu markdown d'un AnalyseProjet pour l'interface utilisateur.

Cette couche transforme la donnée structurée produite par la chaîne LCEL
(`src/chain.py`) en markdown lisible affiché par Chainlit / Gradio.

Aucune logique métier ici : on ne recalcule rien, on ne filtre rien. Les
invariants (cohérence couvertes/manquantes, blocs reconstruits) sont
garantis en amont par les `model_validator` de `src/schemas.py`.
"""

from src.schemas import AnalyseProjet, CompetenceCouverte

CONFIANCE_EMOJI: dict[str, str] = {
    "élevée": "✅",
    "moyenne": "🟡",
    "faible": "⚠️",
}

BLOCS_LIBELLES: dict[int, str] = {
    1: "Bloc 1 — Collecte, stockage et mise à disposition des données (C1-C5)",
    2: "Bloc 2 — Intégration de modèles et services d'IA (C6-C13)",
    3: "Bloc 3 — Application intégrant un service d'IA (C14-C21)",
}


def _render_competence(comp: CompetenceCouverte) -> str:
    """Rend une seule compétence couverte en markdown."""
    emoji = CONFIANCE_EMOJI.get(comp.confiance, "")
    return "\n".join(
        [
            f"### {comp.code} — {comp.nom}",
            f"**Confiance** : {emoji} {comp.confiance}",
            f"**Justification** : {comp.justification}",
            f"> _Extrait du référentiel_ : {comp.extrait_referentiel}",
        ]
    )


def _render_blocs(blocs: list[int]) -> str:
    """Rend la section blocs couverts."""
    if not blocs:
        return "_Aucun bloc du référentiel n'est couvert par ce projet._"
    return "\n".join(f"- {BLOCS_LIBELLES.get(b, f'Bloc {b}')}" for b in blocs)


def render_analyse(analyse: AnalyseProjet) -> str:
    """
    Transforme un AnalyseProjet en markdown complet pour affichage UI.

    Args:
        analyse: Résultat validé de la chaîne LCEL.

    Returns:
        Une chaîne markdown prête à être passée à Chainlit / Gradio.
    """
    sections: list[str] = ["# Analyse RNCP Dev IA"]

    sections.append("## Synthèse")
    sections.append(analyse.synthese)

    sections.append("## Blocs couverts")
    sections.append(_render_blocs(analyse.blocs_couverts))

    nb_couvertes = len(analyse.competences_couvertes)
    sections.append(f"## Compétences couvertes ({nb_couvertes})")
    if nb_couvertes == 0:
        sections.append(
            "_Aucune compétence du référentiel n'a pu être identifiée à partir "
            "de la description fournie. Essaie de détailler davantage les "
            "outils, méthodes et étapes de ton projet._"
        )
    else:
        sections.extend(_render_competence(c) for c in analyse.competences_couvertes)

    sections.append("## Compétences manquantes")
    if not analyse.competences_manquantes:
        sections.append(
            "_Aucune compétence n'a été signalée comme manquante par l'analyse._"
        )
    else:
        sections.append(
            "\n".join(f"- {code}" for code in analyse.competences_manquantes)
        )

    return "\n\n".join(sections)
