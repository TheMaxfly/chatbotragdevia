"""Test end-to-end : chaîne LCEL + rendu markdown."""

import time
from pathlib import Path

from src.chain import analyze_project, build_chain
from src.rendering import render_analyse

PROJET_TEST = """
Mon projet est une application web de classification d'images médicales.

Architecture technique :
- Backend FastAPI exposant le modèle d'IA via une API REST
- Modèle de classification entraîné avec TensorFlow et packagé via Docker
- Base de données PostgreSQL pour stocker les métadonnées et résultats
- Pipeline GitHub Actions qui exécute mes tests pytest à chaque push,
  builde l'image Docker et la pousse sur le registry
- Monitoring de l'application via Prometheus et Grafana
- Interface React pour les utilisateurs (médecins) qui uploadent des images

Conformité RGPD : registre des traitements rédigé, anonymisation des données
patients avant stockage.
"""

OUTPUT_MD = Path("./tmp_analyse.md")


def main() -> None:
    print("🔧 Construction de la chaîne LCEL...")
    t0 = time.time()
    chain = build_chain()
    print(f"   ✓ Chaîne prête en {time.time() - t0:.1f}s")

    print("\n🚀 Analyse du projet (30-60s avec Qwen3-4B)...")
    t0 = time.time()
    analyse = analyze_project(chain, PROJET_TEST)
    print(f"   ✓ Analyse terminée en {time.time() - t0:.1f}s")

    # Résumé technique (debug rapide)
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ TECHNIQUE")
    print("=" * 60)
    print(f"Blocs couverts         : {analyse.blocs_couverts}")
    print(f"Compétences couvertes  : {len(analyse.competences_couvertes)}")
    print(f"Compétences manquantes : {len(analyse.competences_manquantes)}")

    # Rendu markdown → fichier (pour preview VSCode)
    markdown = render_analyse(analyse)
    OUTPUT_MD.write_text(markdown, encoding="utf-8")
    print(f"\n📝 Rendu markdown écrit dans : {OUTPUT_MD.resolve()}")
    print("   → Ouvre-le dans VSCode (Ctrl+Shift+V) pour la preview.")

    # JSON brut pour debug profond
    print("\n" + "=" * 60)
    print("🔬 JSON BRUT")
    print("=" * 60)
    print(analyse.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
