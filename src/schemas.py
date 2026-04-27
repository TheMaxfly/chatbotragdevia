"""
Schémas Pydantic pour le chatbot RNCP.

Ces modèles définissent le contrat de sortie attendu du LLM lorsqu'il analyse
un projet par rapport au référentiel RNCP Dev IA.

Le schéma est exposé au LLM via PydanticOutputParser dans src/prompts.py.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class CompetenceCouverte(BaseModel):
    """
    Une compétence du référentiel identifiée comme couverte par le projet analysé.

    Chaque champ doit être rempli par le LLM avec rigueur. La justification et
    l'extrait du référentiel sont obligatoires : c'est ce qui distingue ce
    chatbot d'un système qui inventerait des compétences.
    """

    code: str = Field(
        description=(
            "Code de la compétence au format 'Cn' où n est compris entre 1 et 21. "
            "Exemples valides : 'C1', 'C13', 'C21'."
        ),
        examples=["C1", "C13", "C21"],
    )

    nom: str = Field(
        description=(
            "Nom complet de la compétence tel qu'il apparaît dans le référentiel. "
            "Exemple : 'Créer une chaîne de livraison continue d'un modèle d'IA (MLOps)'."
        ),
    )

    justification: str = Field(
        description=(
            "Explication concrète et précise de POURQUOI cette compétence est "
            "couverte par le projet décrit. Doit faire référence à des éléments "
            "EXPLICITES du projet (ex: 'le projet utilise FastAPI', 'pipeline "
            "GitHub Actions configuré'). Une à trois phrases."
        ),
    )

    extrait_referentiel: str = Field(
        description=(
            "Citation EXACTE d'un critère d'évaluation ou d'une activité du "
            "référentiel qui correspond au projet. Ne pas reformuler : copier "
            "tel quel un passage du référentiel fourni dans le contexte."
        ),
    )

    confiance: Literal["faible", "moyenne", "élevée"] = Field(
        description=(
            "Niveau de confiance dans l'identification de cette compétence : "
            "'élevée' si plusieurs critères sont clairement remplis, "
            "'moyenne' si la couverture est partielle, "
            "'faible' si l'on infère sans certitude."
        ),
    )

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Vérifie que le code est au format Cn avec n entre 1 et 21."""
        v = v.strip().upper()
        if not v.startswith("C"):
            raise ValueError(f"Le code doit commencer par 'C', reçu : {v!r}")
        try:
            n = int(v[1:])
        except ValueError:
            raise ValueError(
                f"Le code doit être 'Cn' avec n entier, reçu : {v!r}"
            ) from None
        if not 1 <= n <= 21:
            raise ValueError(f"Le code doit être entre C1 et C21, reçu : {v!r}")
        return v


class AnalyseProjet(BaseModel):
    """
    Analyse complète d'un projet par rapport au référentiel RNCP Dev IA.

    C'est l'objet final retourné par le chatbot. Il contient :
    - Les compétences couvertes avec justifications
    - Les compétences identifiées comme manquantes
    - Les blocs concernés
    - Une synthèse qualitative
    """

    competences_couvertes: list[CompetenceCouverte] = Field(
        description=(
            "Liste des compétences du référentiel qui sont couvertes par le "
            "projet, avec justification et extrait du référentiel pour chacune. "
            "Liste vide si le projet ne couvre aucune compétence identifiable."
        ),
    )

    competences_manquantes: list[str] = Field(
        description=(
            "Liste des codes de compétences (au format 'Cn') qui sont "
            "explicitement manquantes ou pertinentes au regard du projet "
            "mais non couvertes. À limiter aux compétences qui auraient été "
            "naturellement attendues. Format : ['C12', 'C18']."
        ),
        default_factory=list,
    )

    blocs_couverts: list[int] = Field(
        description=(
            "Liste des numéros de blocs (1, 2, ou 3) qui contiennent au moins "
            "une compétence couverte. Format : [1, 2]."
        ),
        default_factory=list,
    )

    synthese: str = Field(
        description=(
            "Synthèse qualitative en 2 à 4 phrases : forces du projet, "
            "blocs bien couverts, points faibles à renforcer pour une "
            "validation complète du titre RNCP."
        ),
    )

    @field_validator("competences_manquantes")
    @classmethod
    def validate_codes_manquantes(cls, v: list[str]) -> list[str]:
        """Valide que chaque code manquant est au format Cn entre 1 et 21."""
        validated = []
        for code in v:
            code = code.strip().upper()
            if not code.startswith("C"):
                continue  # On ignore silencieusement les codes mal formés
            try:
                n = int(code[1:])
                if 1 <= n <= 21:
                    validated.append(code)
            except ValueError:
                continue
        return validated

    @field_validator("blocs_couverts")
    @classmethod
    def validate_blocs(cls, v: list[int]) -> list[int]:
        """Valide que chaque numéro de bloc est entre 1 et 3."""
        return [b for b in v if b in (1, 2, 3)]
