import json

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

PRIX_KWH = 600
CONSO_FAMILLE_KWH_AN = 300
NB_PERSONNES_FAMILLE = 6
NB_MODULES_VILLAGE = 100

ref = clim["mois_plus_chaud"]
prod_ref = ref["production_kwh_an"]
r_avant = ref["rendement_absolu_pct"] / 100

gain_temp_d1 = 8
r_apres_d1 = r_avant * (1 + 0.004 * gain_temp_d1)
gain_prod_d1_module = prod_ref * (r_apres_d1 / r_avant - 1)
gain_prod_d1_village = gain_prod_d1_module * NB_MODULES_VILLAGE

gain_temp_d2 = 5
r_apres_d2 = r_avant * (1 + 0.004 * gain_temp_d2)
gain_prod_d2_module = prod_ref * (r_apres_d2 / r_avant - 1)
gain_prod_d2_village = gain_prod_d2_module * NB_MODULES_VILLAGE

def calc_habitants(gain_village_kwh):
    familles = gain_village_kwh / CONSO_FAMILLE_KWH_AN
    return int(familles * NB_PERSONNES_FAMILLE)

designs = [
    {
        "nom": "Bassin d'eau V4 (renforce + fixe)",
        "description": "Bassin beton fibre + armature metallique legere + bache HDPE 500 microns fixee par crochets + couvercle rigide bois traite + filtre charbon actif anti-algues + flotteur. Structure pour 48 mois.",
        "materiaux": [
            "Bassin beton fibre + armature : 7200 FCFA",
            "Bache HDPE 500 microns UV : 4000 FCFA",
            "Cadre acier galvanise peint : 4000 FCFA",
            "Crochets ancrage bache (12) : 300 FCFA",
            "Couvercle rigide bois traite : 1500 FCFA",
            "Filtre charbon actif + gravier : 1500 FCFA",
            "Tuyau acier galvanise : 500 FCFA"
        ],
        "cout_fcfa": 19000,
        "gain_temp": gain_temp_d1,
        "gain_rendement_pct": round((r_apres_d1 - r_avant) * 100, 2),
        "gain_kwh_an_module": round(gain_prod_d1_module, 2),
        "gain_fcfa_an_module": round(gain_prod_d1_module * PRIX_KWH, 0),
        "gain_kwh_an_village": round(gain_prod_d1_village, 1),
        "gain_fcfa_an_village": round(gain_prod_d1_village * PRIX_KWH, 0),
        "habitants_impactes_village": calc_habitants(gain_prod_d1_village),
        "duree_vie_mois": 48
    },
    {
        "nom": "Peinture reflechissante V2",
        "description": "Peinture chaux + huile de lin + grille aluminium + pieds ancrees beton.",
        "materiaux": [
            "Peinture chaux + huile de lin : 4000 FCFA",
            "Grille aluminium : 2500 FCFA",
            "Pieds ancrees beton : 2000 FCFA",
            "Support sureleve renforce : 1500 FCFA"
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
print("   NEXORA - Ingenieur V4 (retour au design optimal)")
print("=" * 70)
print()
for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an_module"] * 12, 1)
    print("--- " + d["nom"] + " ---")
    print("  Cout             : " + str(d["cout_fcfa"]) + " FCFA")
    print("  Payback          : " + str(payback) + " mois")
    print("  Duree            : " + str(d["duree_vie_mois"]) + " mois")
    print("  Gain kWh/an      : +" + str(d["gain_kwh_an_module"]) + " kWh/module")
    print("  Habitants        : " + str(d["habitants_impactes_village"]) + " personnes")
    print()
print("Fichier : designs.json")

