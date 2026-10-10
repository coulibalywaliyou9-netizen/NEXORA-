import json

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

print("Verification du rapport de", r["ville"])

ok = True

if r["temperature_cellule"] < 20:
    print("ALERTE : cellule trop froide")
    ok = False

if r["temperature_cellule"] > 90:
    print("ALERTE : cellule trop chaude")
    ok = False

if r["rendement_pct"] > 100:
    print("ALERTE : rendement impossible")
    ok = False

if r["temperature_cellule"] < r["temperature_air"]:
    print("ALERTE : cellule plus froide que l'air")
    ok = False

if ok:
    print("Rapport valide. Aucune anomalie.")

print("Temperature cellule :", r["temperature_cellule"])
print("Rendement :", r["rendement_pct"], "%")

