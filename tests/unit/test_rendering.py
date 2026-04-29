from src.rendering import render_analyse
from src.schemas import AnalyseProjet, CompetenceCouverte


def test_render_analyse_outputs_markdown_sections() -> None:
    analyse = AnalyseProjet(
        competences_couvertes=[
            CompetenceCouverte(
                code="C18",
                nom="Automatiser les phases de tests via une chaîne d'intégration continue",
                justification="Le projet utilise GitHub Actions pour exécuter les tests.",
                extrait_referentiel="La chaîne exécute les tests de l'application disponibles lors de son déclenchement",
                confiance="élevée",
            )
        ],
        competences_manquantes=["C19"],
        blocs_couverts=[],
        synthese="Le projet couvre la partie intégration continue.",
    )

    markdown = render_analyse(analyse)

    assert "# Analyse RNCP Dev IA" in markdown
    assert "## Synthèse" in markdown
    assert "### C18" in markdown
    assert "Bloc 3" in markdown
    assert "- C19" in markdown


def test_render_analyse_handles_empty_result() -> None:
    analyse = AnalyseProjet(
        competences_couvertes=[],
        competences_manquantes=[],
        blocs_couverts=[],
        synthese="Aucune compétence identifiable.",
    )

    markdown = render_analyse(analyse)

    assert "_Aucun bloc du référentiel n'est couvert" in markdown
    assert "_Aucune compétence du référentiel n'a pu être identifiée" in markdown
    assert "_Aucune compétence n'a été signalée comme manquante" in markdown
