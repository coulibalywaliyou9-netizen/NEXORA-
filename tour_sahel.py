import subprocess
import sys
import json
import os

villes = [
    {"nom": "Ouagadougou", "lat": 12.37, "lon": -1.52},
    {"nom": "Bobo-Dioulasso", "lat": 11.18, "lon": -4.30},
    {"nom": "Niamey", "lat": 13.51, "lon": 2.11},
    {"nom": "Bamako", "lat": 12.65, "lon": -8.00},
    {"nom": "N'Djamena", "lat": 12.11, "lon": 15.05}
]

resultats = []

print("=" * 50)
print("   NEXORA - Tour du Sahel")
print("=" * 50)

for v in villes:
    print()
    print("--- Analyse :", v["nom"], "---")
    
    with open("config.py", "w") as f:
        f.write(f'VILLE = "{v["nom"]}"\n')
        f.write(f'LATITUDE = {v["lat"]}\n')
        f.write(f'LONGITUDE = {v["lon"]}\n')
    
    subprocess.run([sys.executable, "rapport.py"], capture_output=True)
    
    with open("rapport.json", "r", encoding="utf-8") as f:
        r = json.load(f)
    
    resultats.append({
        "ville": r["ville"],
        "temperature_cellule": r["temperature_cellule"],
        "rendement_absolu_pct": r["rendement_absolu_pct"],
        "perte_pct": r["perte_pct"]
    })
    print("Temp cellule :", r["temperature_cellule"], "C")
    print("Rendement    :", r["rendement_absolu_pct"], "%")

with open("sahel.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print()
print("=" * 50)
print("   Tour du Sahel termine - 5 villes analysees")
print("=" * 50)
print()
print("Resultats sauvegardes dans sahel.json")
