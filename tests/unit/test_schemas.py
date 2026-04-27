import pytest
from pydantic import ValidationError

from src.schemas import AnalyseProjet, CompetenceCouverte


def test_competence_code_is_normalized() -> None:
    competence = CompetenceCouverte(
        code="c13",
        nom="Créer une chaîne de livraison continue d'un modèle d'IA (MLOps)",
        justification="Le projet décrit un pipeline de livraison.",
        extrait_referentiel="Créer une chaîne de livraison continue d'un modèle d'intelligence artificielle",
        confiance="moyenne",
    )

    assert competence.code == "C13"


def test_competence_code_rejects_unknown_code() -> None:
    with pytest.raises(ValidationError):
        CompetenceCouverte(
            code="C42",
            nom="Compétence inexistante",
            justification="Non applicable.",
            extrait_referentiel="Non applicable.",
            confiance="faible",
        )


def test_analyse_filters_invalid_missing_competences_and_blocs() -> None:
    analyse = AnalyseProjet(
        competences_couvertes=[],
        competences_manquantes=["C12", "bad", "C99"],
        blocs_couverts=[1, 4, 2],
        synthese="Synthèse de test.",
    )

    assert analyse.competences_manquantes == ["C12"]
    assert analyse.blocs_couverts == [1, 2]
