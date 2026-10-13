import json

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

# Scenario de reference : mois le plus chaud (pire cas)
ref = clim["mois_plus_chaud"]
T_ref = ref["T_cellule"]
prod_ref = ref["production_kwh_an"]

# Design 1 : Refroidissement passif par bassin d'eau
gain_temp_d1 = 8
T_apres_d1 = T_ref - gain_temp_d1
r_avant = ref["rendement_absolu_pct"] / 100
r_apres_d1 = r_avant * (1 + 0.004 * gain_temp_d1)
gain_rend_d1 = (r_apres_d1 - r_avant) * 100
prod_apres_d1 = prod_ref * (r_apres_d1 / r_avant)
gain_prod_d1 = prod_apres_d1 - prod_ref
prix_kwh = 600
gain_fcfa_d1 = gain_prod_d1 * prix_kwh

# Design 2 : Peinture reflechissante + ventilation naturelle
gain_temp_d2 = 5
T_apres_d2 = T_ref - gain_temp_d2
r_apres_d2 = r_avant * (1 + 0.004 * gain_temp_d2)
gain_rend_d2 = (r_apres_d2 - r_avant) * 100
prod_apres_d2 = prod_ref * (r_apres_d2 / r_avant)
gain_prod_d2 = prod_apres_d2 - prod_ref
gain_fcfa_d2 = gain_prod_d2 * prix_kwh

designs = [
    {
        "nom": "Bassin d'eau sous panneau",
        "description": "Cadre metallique + bassin d'eau 5 cm de profondeur sous le panneau. Evaporation naturelle + conduction thermique.",
        "materiaux": [
            "Cadre en acier galvanise (recupere)",
            "Bassin en beton leger (ciment + sable)",
            "Bache plastique etanche",
            "Tuyau PVC pour remplissage"
        ],
        "cout_fcfa": 15000,
        "gain_temp": gain_temp_d1,
        "gain_rendement_pct": round(gain_rend_d1, 2),
        "gain_kwh_an": round(gain_prod_d1, 1),
        "gain_fcfa_an": round(gain_fcfa_d1, 0),
        "habitants_impactes": 25
    },
    {
        "nom": "Peinture reflechissante + ventilation",
        "description": "Peinture blanche haute albedo sur le cadre + grille de ventilation naturelle sous le panneau.",
        "materiaux": [
            "Peinture blanche a base de chaux",
            "Grille metallique (recuperee)",
            "Support surélevé 10 cm"
        ],
        "cout_fcfa": 5000,
        "gain_temp": gain_temp_d2,
        "gain_rendement_pct": round(gain_rend_d2, 2),
        "gain_kwh_an": round(gain_prod_d2, 1),
        "gain_fcfa_an": round(gain_fcfa_d2, 0),
        "habitants_impactes": 15
    }
]

with open("designs.json", "w", encoding="utf-8") as f:
    json.dump(designs, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("   NEXORA - Ingenieur V2 (designs robustes)")
print("=" * 60)
print()
print("Scenario de reference :", ref["description"])
print("T cellule avant :", T_ref, "C")
print()
for d in designs:
    print("---", d["nom"], "---")
    print("  Cout         :", d["cout_fcfa"], "FCFA")
    print("  Gain temp    :", d["gain_temp"], "C")
    print("  Gain rendement :", d["gain_rendement_pct"], "%")
    print("  Gain kWh/an  :", d["gain_kwh_an"], "kWh")
    print("  Gain FCFA/an :", d["gain_fcfa_an"], "FCFA")
    print("  Payback      :", round(d["cout_fcfa"] / d["gain_fcfa_an"] * 12, 1), "mois")
    print()
print("Fichier : designs.json")

