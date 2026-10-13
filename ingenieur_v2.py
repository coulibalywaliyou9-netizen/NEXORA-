import json

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

# Hypotheses
PRIX_KWH = 600
CONSO_FAMILLE_AN = 300
NB_PERSONNES_FAMILLE = 6
NB_MODULES_VILLAGE = 100

ref = clim["mois_plus_chaud"]
T_ref = ref["T_cellule"]
prod_ref = ref["production_kwh_an"]
r_avant = ref["rendement_absolu_pct"] / 100

gain_temp_d1 = 8
r_apres_d1 = r_avant * (1 + 0.004 * gain_temp_d1)
gain_prod_d1 = prod_ref * (r_apres_d1 / r_avant - 1)

gain_temp_d2 = 5
r_apres_d2 = r_avant * (1 + 0.004 * gain_temp_d2)
gain_prod_d2 = prod_ref * (r_apres_d2 / r_avant - 1)

def calc_habitants(gain_module):
    gain_village = gain_module * NB_MODULES_VILLAGE
    familles = gain_village / CONSO_FAMILLE_AN
    return int(familles * NB_PERSONNES_FAMILLE)

designs = [
    {
        "nom": "Bassin d'eau sous panneau",
        "description": "Cadre metallique + bassin d'eau 5 cm sous le panneau. Evaporation naturelle + conduction.",
        "materiaux": [
            "Cadre acier galvanise (recupere) : 5 000 FCFA",
            "Bassin beton leger (ciment + sable) : 6 000 FCFA",
            "Bache plastique etanche : 3 000 FCFA",
            "Tuyau PVC remplissage : 1 000 FCFA"
        ],
        "cout_fcfa": 15000,
        "gain_temp": gain_temp_d1,
        "gain_rendement_pct": round((r_apres_d1 - r_avant) * 100, 2),
        "gain_kwh_an": round(gain_prod_d1, 1),
        "gain_fcfa_an": round(gain_prod_d1 * PRIX_KWH, 0),
        "habitants_impactes": calc_habitants(gain_prod_d1),
        "duree_vie_mois": 24
    },
    {
        "nom": "Peinture reflechissante + ventilation",
        "description": "Peinture blanche haute albedo + grille de ventilation naturelle sous le panneau.",
        "materiaux": [
            "Peinture blanche a base de chaux : 3 000 FCFA",
            "Grille metallique (recuperee) : 1 000 FCFA",
            "Support sureleve 10 cm : 1 000 FCFA"
        ],
        "cout_fcfa": 5000,
        "gain_temp": gain_temp_d2,
        "gain_rendement_pct": round((r_apres_d2 - r_avant) * 100, 2),
        "gain_kwh_an": round(gain_prod_d2, 1),
        "gain_fcfa_an": round(gain_prod_d2 * PRIX_KWH, 0),
        "habitants_impactes": calc_habitants(gain_prod_d2),
        "duree_vie_mois": 18
    }
]

with open("designs.json", "w", encoding="utf-8") as f:
    json.dump(designs, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("   NEXORA - Ingenieur V2 (avec habitants)")
print("=" * 60)
print()
print("Scenario de reference :", ref["description"])
print("T cellule avant :", T_ref, "C")
print("Prix kWh rural :", PRIX_KWH, "FCFA")
print("Modules par village :", NB_MODULES_VILLAGE)
print()
for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an"] * 12, 1)
    print("--- " + d["nom"] + " ---")
    print("  Cout           : " + str(d["cout_fcfa"]) + " FCFA")
    print("  Gain temp      : -" + str(d["gain_temp"]) + " C")
    print("  Gain rendement : +" + str(d["gain_rendement_pct"]) + " %")
    print("  Gain kWh/an    : +" + str(d["gain_kwh_an"]) + " kWh/module")
    print("  Gain FCFA/an   : +" + str(int(d["gain_fcfa_an"])) + " FCFA")
    print("  Payback        : " + str(payback) + " mois")
    print("  Habitants      : " + str(d["habitants_impactes"]) + " personnes")
    print("  Duree de vie   : " + str(d["duree_vie_mois"]) + " mois")
    print()
print("Fichier : designs.json")

