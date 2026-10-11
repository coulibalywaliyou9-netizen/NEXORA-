import json
import os
from datetime import datetime

if not os.path.exists("rapport.json"):
    print("Aucun rapport trouve. Lance d'abord rapport.py.")
    exit()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

if not os.path.exists("historique.json"):
    historique = []
else:
    with open("historique.json", "r", encoding="utf-8") as f:
        historique = json.load(f)

entree = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "rapport": r
}
historique.append(entree)

with open("historique.json", "w", encoding="utf-8") as f:
    json.dump(historique, f, indent=2, ensure_ascii=False)

print("Rapport archive. Total dans l'historique :", len(historique))
print()
print("--- 5 dernieres entrees ---")
for e in historique[-5:]:
    r2 = e["rapport"]
    print(e["date"], "|", r2["temperature_cellule"], "C |", r2["rendement_absolu_pct"], "%")

