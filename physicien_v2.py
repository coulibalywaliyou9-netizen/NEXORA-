import json
from climat import CLIMAT, VILLE

COEF_TEMP = -0.004
COEF_REND_NOMINAL = 0.20
K_NOCT = 3.5
SURFACE_PANNEAU = 1.72
PUISSANCE_NOMINALE_W = 300

resultats = {}

for scenario, data in CLIMAT.items():
    Ta = data["T_air"]
    irr = data["irradiation"]
    vent = data["vent"]
    
    T_cell = Ta + K_NOCT * irr
    r_rel = 1 + COEF_TEMP * (T_cell - 25)
    r_abs = COEF_REND_NOMINAL * r_rel
    
    # Verification de coherence
    energie_recue = irr * SURFACE_PANNEAU
    prod_jour = energie_recue * r_abs
    prod_an = prod_jour * 365
    
    # Check : la production ne peut pas depasser l'energie recue
    coherent = prod_jour <= energie_recue
    
    resultats[scenario] = {
        "description": data["description"],
        "T_air": Ta,
        "irradiation": irr,
        "vent": vent,
        "T_cellule": round(T_cell, 1),
        "rendement_relatif_pct": round(r_rel * 100, 1),
        "rendement_absolu_pct": round(r_abs * 100, 1),
        "energie_recue_kwh_jour": round(energie_recue, 2),
        "production_kwh_jour": round(prod_jour, 2),
        "production_kwh_an": round(prod_an, 1),
        "perte_pct": round((1 - r_rel) * 100, 1),
        "coherent": coherent
    }

with open("analyse_climat.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

rend_stc = PUISSANCE_NOMINALE_W / (1000 * SURFACE_PANNEAU)

print("=" * 60)
print("   NEXORA - Physicien V2 (avec verification)")
print("=" * 60)
print()
print("Ville :", VILLE)
print("Surface panneau :", SURFACE_PANNEAU, "m2")
print("Puissance nominale :", PUISSANCE_NOMINALE_W, "W")
print("Rendement STC calcule :", round(rend_stc * 100, 1), "%")
print()
for scenario, r in resultats.items():
    print("--- " + r["description"] + " ---")
    print("  T air         : " + str(r["T_air"]) + " C")
    print("  T cellule     : " + str(r["T_cellule"]) + " C")
    print("  Rendement     : " + str(r["rendement_absolu_pct"]) + " %")
    print("  Energie recue : " + str(r["energie_recue_kwh_jour"]) + " kWh/jour")
    print("  Production    : " + str(r["production_kwh_jour"]) + " kWh/jour")
    print("  Production    : " + str(r["production_kwh_an"]) + " kWh/an")
    print("  Coherent      : " + ("OUI" if r["coherent"] else "NON"))
    print()
print("Fichier : analyse_climat.json")
print("=" * 60)

