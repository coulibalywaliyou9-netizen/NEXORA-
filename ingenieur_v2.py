import json

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

# ===== HYPOTHESES EXPLICITES =====
PRIX_KWH = 600                    # FCFA/kWh en zone rurale
CONSO_FAMILLE_KWH_AN = 300        # kWh/an pour 1 famille (usage minimal : eclairage + telephone)
NB_PERSONNES_FAMILLE = 6          # personnes par famille
NB_MODULES_VILLAGE = 100          # taille typique d'une installation villageoise

# ===== SCENARIO DE REFERENCE =====
ref = clim["mois_plus_chaud"]
T_ref = ref["T_cellule"]
prod_ref = ref["production_kwh_an"]  # pour 1 module
r_avant = ref["rendement_absolu_pct"] / 100

# ===== DESIGN 1 : BASSIN D'EAU =====
gain_temp_d1 = 8
r_apres_d1 = r_avant * (1 + 0.004 * gain_temp_d1)
gain_prod_d1_module = prod_ref * (r_apres_d1 / r_avant - 1)  # kWh/an pour 1 module
gain_prod_d1_village = gain_prod_d1_module * NB_MODULES_VILLAGE  # kWh/an pour 100 modules

# ===== DESIGN 2 : PEINTURE + VENTILATION =====
gain_temp_d2 = 5
r_apres_d2 = r_avant * (1 + 0.004 * gain_temp_d2)
gain_prod_d2_module = prod_ref * (r_apres_d2 / r_avant - 1)
gain_prod_d2_village = gain_prod_d2_module * NB_MODULES_VILLAGE

# ===== CALCUL HABITANTS IMPACTES =====
def calc_habitants(gain_village_kwh):
    familles = gain_village_kwh / CONSO_FAMILLE_KWH_AN
    return int(familles * NB_PERSONNES_FAMILLE)

designs = [
    {
        "nom": "Bassin d'eau sous panneau",
        "description": "Cadre metallique + bassin d'eau 5 cm sous le panneau. Evaporation naturelle + conduction.",
        "materiaux": [
            "Cadre acier galvanise : 5 000 FCFA",
            "Bassin beton leger : 6 000 FCFA",
            "Bache plastique etanche : 3 000 FCFA",
            "Tuyau PVC remplissage : 1 000 FCFA"
        ],
        "cout_fcfa": 15000,
        "gain_temp": gain_temp_d1,
        "gain_rendement_pct": round((r_apres_d1 - r_avant) * 100, 2),
        
        # Pour 1 module
        "gain_kwh_an_module": round(gain_prod_d1_module, 2),
        "gain_fcfa_an_module": round(gain_prod_d1_module * PRIX_KWH, 0),
        
        # Pour 100 modules (village)
        "gain_kwh_an_village": round(gain_prod_d1_village, 1),
        "gain_fcfa_an_village": round(gain_prod_d1_village * PRIX_KWH, 0),
        "habitants_impactes_village": calc_habitants(gain_prod_d1_village),
        
        "duree_vie_mois": 24
    },
    {
        "nom": "Peinture reflechissante + ventilation",
        "description": "Peinture blanche haute albedo + grille de ventilation naturelle sous le panneau.",
        "materiaux": [
            "Peinture blanche a base de chaux : 3 000 FCFA",
            "Grille metallique : 1 000 FCFA",
            "Support sureleve 10 cm : 1 000 FCFA"
        ],
        "cout_fcfa": 5000,
        "gain_temp": gain_temp_d2,
        "gain_rendement_pct": round((r_apres_d2 - r_avant) * 100, 2),
        
        "gain_kwh_an_module": round(gain_prod_d2_module, 2),
        "gain_fcfa_an_module": round(gain_prod_d2_module * PRIX_KWH, 0),
        
        "gain_kwh_an_village": round(gain_prod_d2_village, 1),
        "gain_fcfa_an_village": round(gain_prod_d2_village * PRIX_KWH, 0),
        "habitants_impactes_village": calc_habitants(gain_prod_d2_village),
        
        "duree_vie_mois": 18
    }
]

with open("designs.json", "w", encoding="utf-8") as f:
    json.dump(designs, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("   NEXORA - Ingenieur V2.2 (habitants clarifie)")
print("=" * 70)
print()
print("HYPOTHESES :")
print("  Prix kWh rural      :", PRIX_KWH, "FCFA")
print("  Conso famille       :", CONSO_FAMILLE_KWH_AN, "kWh/an (", NB_PERSONNES_FAMILLE, "personnes)")
print("  Conso par personne  :", round(CONSO_FAMILLE_KWH_AN / NB_PERSONNES_FAMILLE, 1), "kWh/an")
print("  Modules par village :", NB_MODULES_VILLAGE)
print()
print("Scenario de reference :", ref["description"])
print("T cellule avant :", T_ref, "C")
print("Production 1 module :", prod_ref, "kWh/an")
print()
for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an_module"] * 12, 1)
    print("--- " + d["nom"] + " ---")
    print("  Cout                       : " + str(d["cout_fcfa"]) + " FCFA (pour 1 module)")
    print("  Gain temp                  : -" + str(d["gain_temp"]) + " C")
    print("  Gain rendement             : +" + str(d["gain_rendement_pct"]) + " %")
    print("  --- POUR 1 MODULE ---")
    print("  Gain energie               : +" + str(d["gain_kwh_an_module"]) + " kWh/an")
    print("  Gain economique            : +" + str(int(d["gain_fcfa_an_module"])) + " FCFA/an")
    print("  Payback 1 module           : " + str(payback) + " mois")
    print("  --- POUR 100 MODULES (village) ---")
    print("  Gain energie               : +" + str(d["gain_kwh_an_village"]) + " kWh/an")
    print("  Gain economique            : +" + str(int(d["gain_fcfa_an_village"])) + " FCFA/an")
    print("  Habitants impactes         : " + str(d["habitants_impactes_village"]) + " personnes")
    print("  Duree de vie               : " + str(d["duree_vie_mois"]) + " mois")
    print()
print("Fichier : designs.json")

