import json
from datetime import datetime

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)
with open("designs.json", "r", encoding="utf-8") as f:
    designs = json.load(f)
with open("verdict.json", "r", encoding="utf-8") as f:
    verdicts = json.load(f)

html = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEXORA - Rapport final</title>
<style>
body { font-family: system-ui, sans-serif; background: #0a0a0a; color: #e0e0e0; padding: 20px; line-height: 1.6; max-width: 900px; margin: 0 auto; }
h1 { color: #ff6b35; }
h2 { color: #ff6b35; border-bottom: 2px solid #ff6b35; padding-bottom: 5px; margin-top: 30px; }
table { width: 100%; border-collapse: collapse; margin: 15px 0; }
th, td { padding: 10px; text-align: left; border-bottom: 1px solid #2a2a2a; }
th { color: #ff6b35; }
.card { background: #1a1a1a; border-radius: 8px; padding: 20px; margin: 15px 0; }
.vert { color: #4ade80; font-weight: bold; }
.orange { color: #fb923c; font-weight: bold; }
.rouge { color: #ef4444; font-weight: bold; }
.footer { margin-top: 40px; text-align: center; color: #666; font-size: 0.9rem; }
</style>
</head>
<body>
<h1>NEXORA - Rapport final</h1>
<p>Ville : Ouagadougou (Burkina Faso)</p>
<p>Date : """ + datetime.now().strftime("%d/%m/%Y %H:%M") + """</p>

<h2>1. Analyse climatique</h2>
<table>
<tr><th>Scenario</th><th>T air</th><th>T cellule</th><th>Rendement</th><th>Production</th></tr>"""

for s, r in clim.items():
    html += "<tr><td>" + r["description"] + "</td><td>" + str(r["T_air"]) + " C</td><td>" + str(r["T_cellule"]) + " C</td><td>" + str(r["rendement_absolu_pct"]) + " %</td><td>" + str(r["production_kwh_an"]) + " kWh/an</td></tr>"

html += """</table>

<h2>2. Designs proposes</h2>"""

for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an"] * 12, 1)
    html += """<div class="card">
<h3>""" + d["nom"] + """</h3>
<p>""" + d["description"] + """</p>
<p><strong>Materiaux :</strong> """ + ", ".join(d["materiaux"]) + """</p>
<table>
<tr><td>Cout</td><td>""" + str(d["cout_fcfa"]) + """ FCFA</td></tr>
<tr><td>Gain temperature</td><td>-""" + str(d["gain_temp"]) + """ C</td></tr>
<tr><td>Gain rendement</td><td>+""" + str(d["gain_rendement_pct"]) + """ %</td></tr>
<tr><td>Gain energie</td><td>+""" + str(d["gain_kwh_an"]) + """ kWh/an</td></tr>
<tr><td>Gain economique</td><td>+""" + str(int(d["gain_fcfa_an"])) + """ FCFA/an</td></tr>
<tr><td>Payback</td><td>""" + str(payback) + """ mois</td></tr>
<tr><td>Habitants impactes</td><td>""" + str(d["habitants_impactes"]) + """</td></tr>
</table>
</div>"""

html += """<h2>3. Critique et notes</h2>
<table>
<tr><th>Design</th><th>Failles</th><th>Note</th><th>Verdict</th></tr>"""

for v in verdicts:
    if v["note"] >= 7:
        verdict = '<span class="vert">RECOMMANDE</span>'
    elif v["note"] >= 5:
        verdict = '<span class="orange">A RETRAVAILLER</span>'
    else:
        verdict = '<span class="rouge">NON RECOMMANDE</span>'
    html += "<tr><td>" + v["design"] + "</td><td>" + "; ".join(v["failles"]) + "</td><td>" + str(v["note"]) + "/10</td><td>" + verdict + "</td></tr>"

html += """</table>

<h2>4. Recommandation finale</h2>
<div class="card">
<p><strong>Design recommande :</strong> """ + max(verdicts, key=lambda x: x["note"])["design"] + """</p>
<p>Ce design offre le meilleur compromis entre cout, gain energetique et faisabilite locale.</p>
</div>

<div class="footer">
<p>NEXORA - L'IA qui invente pour le monde depuis l'Afrique</p>
<p>Le feu ne doit jamais rester aux dieux.</p>
</div>
</body>
</html>"""

with open("rapport_final.html", "w", encoding="utf-8") as f:
    f.write(html)

print("=" * 60)
print("   NEXORA - Rapport final genere")
print("=" * 60)
print()
print("Fichier : rapport_final.html")
print("Taille :", len(html), "caracteres")
print()
print("Ouvre-le dans un navigateur.")
print("=" * 60)

