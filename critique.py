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

if r["rendement_absolu_pct"] > 35:
    print("ALERTE : rendement absolu impossible pour du silicium")
    ok = False

if r["rendement_absolu_pct"] < 5:
    print("ALERTE : rendement absolu trop faible")
    ok = False

if r["temperature_cellule"] < r["temperature_air"]:
    print("ALERTE : cellule plus froide que l'air")
    ok = False

if ok:
    print("Rapport valide. Aucune anomalie.")

print("Temperature cellule :", r["temperature_cellule"])
print("Rendement absolu :", r["rendement_absolu_pct"], "%")
print("Rendement relatif :", r["rendement_relatif_pct"], "%")
