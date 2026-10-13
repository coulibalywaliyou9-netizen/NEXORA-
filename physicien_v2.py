import json
from climat import CLIMAT, VILLE

COEF_TEMP = -0.004
COEF_REND_NOMINAL = 0.20

resultats = {}

for scenario, data in CLIMAT.items():
    Ta = data["T_air"]
    irr = data["irradiation"]  # kWh/m2/jour
    vent = data["vent"]
    
    # Formule correcte : T_cellule = T_air + k * irradiation_journaliere
    # k ~ 3.5 C par kWh/m2/jour (coefficient empirique terrain)
    k = 3.5
    T_cell = Ta + k * irr
    
    # Rendement relatif
    r_rel = 1 + COEF_TEMP * (T_cell - 25)
    
    # Rendement absolu
    r_abs = COEF_REND_NOMINAL * r_rel
    
    # Perte
    perte = (1 - r_rel) * 100
    
    # Production annuelle (module 300W, surface 1.72 m2)
    surf = 1.72
    prod_jour = irr * surf * r_abs  # kWh/jour
    prod_an = prod_jour * 365  # kWh/an
    
    resultats[scenario] = {
        "description": data["description"],
        "T_air": Ta,
        "irradiation": irr,
        "vent": vent,
        "T_cellule": round(T_cell, 1),
        "rendement_relatif_pct": round(r_rel * 100, 1),
        "rendement_absolu_pct": round(r_abs * 100, 1),
        "perte_pct": round(perte, 1),
        "production_kwh_an": round(prod_an, 1)
    }

with open("analyse_climat.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("   NEXORA - Physicien V2 (analyse climatique)")
print("=" * 60)
print()
print("Ville :", VILLE)
print()
for scenario, r in resultats.items():
    print("--- " + r["description"] + " ---")
    print("  T air       : " + str(r["T_air"]) + " C")
    print("  T cellule   : " + str(r["T_cellule"]) + " C")
    print("  Rendement   : " + str(r["rendement_absolu_pct"]) + " %")
    print("  Production  : " + str(r["production_kwh_an"]) + " kWh/an")
    print()
print("Fichier : analyse_climat.json")
print("=" * 60)

