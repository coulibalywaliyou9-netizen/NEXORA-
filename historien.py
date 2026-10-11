import json
import os
from datetime import datetime

if not os.path.exists("historique.json"):
    print("Aucun historique disponible.")
    exit()

with open("historique.json", "r", encoding="utf-8") as f:
    historique = json.load(f)

if len(historique) < 2:
    print("Pas assez de donnees pour analyser une tendance.")
    exit()

print("=" * 50)
print("   NEXORA - Historien")
print("=" * 50)
print()

rendements = [e["rapport"]["rendement_absolu_pct"] for e in historique]
temperatures = [e["rapport"]["temperature_cellule"] for e in historique]

moy_rend = sum(rendements) / len(rendements)
moy_temp = sum(temperatures) / len(temperatures)

print("Nombre d'analyses archivees :", len(historique))
print("Rendement moyen :", round(moy_rend, 2), "%")
print("Temperature cellule moyenne :", round(moy_temp, 1), "C")
print()

if len(rendements) >= 3:
    premier = rendements[0]
    dernier = rendements[-1]
    variation = dernier - premier

    if variation > 0.2:
        tendance = "HAUSSE"
    elif variation < -0.2:
        tendance = "BAISSE"
    else:
        tendance = "STABLE"

    print("--- Tendance ---")
    print("Premier rendement :", premier, "%")
    print("Dernier rendement :", dernier, "%")
    print("Variation :", round(variation, 2), "points")
    print("Tendance :", tendance)
    print()

    if tendance == "BAISSE":
        print("ALERTE : le rendement diminue dans le temps.")
        print("Cause possible : saison chaude, poussiere, degradation.")
    elif tendance == "HAUSSE":
        print("Bon signe : le rendement augmente.")
    else:
        print("Le rendement est stable.")
else:
    print("Tendance : pas assez de donnees (minimum 3 analyses).")

print()
print("=" * 50)
