import json

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

PRIX_KWH = 600
CONSO_FAMILLE_KWH_AN = 300
NB_PERSONNES_FAMILLE = 6
NB_MODULES_VILLAGE = 100

ref = clim["mois_plus_chaud"]
T_ref = ref["T_cellule"]
prod_ref = ref["production_kwh_an"]
r_avant = ref["rendement_absolu_pct"] / 100

# Design 1 V3 : Bassin optimise (gain 8 C, duree 36 mois, cout maitrise)
gain_temp_d1 = 8
r_apres_d1 = r_avant * (1 + 0.004 * gain_temp_d1)
gain_prod_d1_module = prod_ref * (r_apres_d1 / r_avant - 1)
gain_prod_d1_village = gain_prod_d1_module * NB_MODULES_VILLAGE

# Design 2 V2 : Peinture renforcee (gain 5 C, duree 36 mois)
gain_temp_d2 = 5
r_apres_d2 = r_avant * (1 + 0.004 * gain_temp_d2)
gain_prod_d2_module = prod_ref * (r_apres_d2 / r_avant - 1)
gain_prod_d2_village = gain_prod_d2_module * NB_MODULES_VILLAGE

def calc_habitants(gain_village_kwh):
    familles = gain_village_kwh / CONSO_FAMILLE_KWH_AN
    return int(familles * NB_PERSONNES_FAMILLE)

designs = [
    {
        "nom": "Bassin d'eau V3 (optimise)",
        "description": "Bassin beton leger + bache HDPE 500 microns + couvercle flottant anti-evaporation (bouteilles plastiques recyclees) + gouttiere recuperation eau de pluie + cadre acier galvanise peint.",
        "materiaux": [
            "Bassin beton leger (ciment + sable) : 6 000 FCFA",
            "Bache HDPE 500 microns UV-resistant : 4 000 FCFA",
            "Cadre acier galvanise + peinture antirouille : 4 000 FCFA",
            "Couvercle flottant (bouteilles recyclees) : 1 500 FCFA",
            "Gouttiere recuperation eau pluie : 1 500 FCFA",
            "Tuyau acier galvanise : 500 FCFA"
        ],
        "cout_fcfa": 17500,
        "gain_temp": gain_temp_d1,
        "gain_rendement_pct": round((r_apres_d1 - r_avant) * 100, 2),
        "gain_kwh_an_module": round(gain_prod_d1_module, 2),
        "gain_fcfa_an_module": round(gain_prod_d1_module * PRIX_KWH, 0),
        "gain_kwh_an_village": round(gain_prod_d1_village, 1),
        "gain_fcfa_an_village": round(gain_prod_d1_village * PRIX_KWH, 0),
        "habitants_impactes_village": calc_habitants(gain_prod_d1_village),
        "duree_vie_mois": 36
    },
    {
        "nom": "Peinture reflechissante V2 + ventilation renforcee",
        "description": "Peinture blanche a base de chaux + huile de lin (tenue UV renforcee) + grille aluminium anti-corrosion + pieds ancrees dans le beton pour la stabilite.",
        "materiaux": [
            "Peinture chaux + huile de lin : 4 000 FCFA",
            "Grille aluminium (anti-corrosion) : 2 500 FCFA",
            "Pieds ancrees beton (4 pieds) : 2 000 FCFA",
            "Support sureleve renforce : 1 500 FCFA"
        ],
        "cout_fcfa": 10000,
        "gain_temp": gain_temp_d2,
        "gain_rendement_pct": round((r_apres_d2 - r_avant) * 100, 2),
        "gain_kwh_an_module": round(gain_prod_d2_module, 2),
        "gain_fcfa_an_module": round(gain_prod_d2_module * PRIX_KWH, 0),
        "gain_kwh_an_village": round(gain_prod_d2_village, 1),
        "gain_fcfa_an_village": round(gain_prod_d2_village * PRIX_KWH, 0),
        "habitants_impactes_village": calc_habitants(gain_prod_d2_village),
        "duree_vie_mois": 36
    }
]

with open("designs.json", "w", encoding="utf-8") as f:
    json.dump(designs, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("   NEXORA - Ingenieur V2.4 (Design 1 + Design 2 ameliores)")
print("=" * 70)
print()
print("HYPOTHESES :")
print("  Prix kWh rural      :", PRIX_KWH, "FCFA")
print("  Conso famille       :", CONSO_FAMILLE_KWH_AN, "kWh/an")
print("  Modules par village :", NB_MODULES_VILLAGE)
print()
print("Scenario de reference :", ref["description"])
print()
for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an_module"] * 12, 1)
    print("--- " + d["nom"] + " ---")
    print("  Cout             : " + str(d["cout_fcfa"]) + " FCFA (1 module)")
    print("  Gain temp        : -" + str(d["gain_temp"]) + " C")
    print("  Gain rendement   : +" + str(d["gain_rendement_pct"]) + " %")
    print("  Gain kWh/an      : +" + str(d["gain_kwh_an_module"]) + " kWh/module")
    print("  Gain FCFA/an     : +" + str(int(d["gain_fcfa_an_module"])) + " FCFA")
    print("  Payback          : " + str(payback) + " mois")
    print("  Habitants (100 mod) : " + str(d["habitants_impactes_village"]) + " personnes")
    print("  Duree de vie     : " + str(d["duree_vie_mois"]) + " mois")
    print()
print("Fichier : designs.json")

