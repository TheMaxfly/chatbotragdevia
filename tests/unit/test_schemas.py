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


def test_analyse_filters_invalid_missing_competences() -> None:
    analyse = AnalyseProjet(
        competences_couvertes=[],
        competences_manquantes=["C12", "bad", "C99"],
        blocs_couverts=[1, 4, 2],
        synthese="Synthèse de test.",
    )

    assert analyse.competences_manquantes == ["C12"]
    assert analyse.blocs_couverts == []


def test_analyse_rebuilds_blocs_from_covered_competences() -> None:
    analyse = AnalyseProjet(
        competences_couvertes=[
            CompetenceCouverte(
                code="C13",
                nom="Créer une chaîne de livraison continue d'un modèle d'IA (MLOps)",
                justification="Pipeline de livraison décrit.",
                extrait_referentiel="Créer une chaîne de livraison continue d'un modèle d'intelligence artificielle",
                confiance="moyenne",
            ),
            CompetenceCouverte(
                code="C19",
                nom="Créer un processus de livraison continue d'une application",
                justification="Build et livraison applicative décrits.",
                extrait_referentiel="Créer un processus de livraison continue d'une application",
                confiance="moyenne",
            ),
        ],
        competences_manquantes=["C13", "C18"],
        blocs_couverts=[1],
        synthese="Synthèse de test.",
    )

    assert analyse.competences_manquantes == ["C18"]
    assert analyse.blocs_couverts == [2, 3]
