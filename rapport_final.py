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
h3 { color: #ff6b35; }
table { width: 100%; border-collapse: collapse; margin: 15px 0; }
th, td { padding: 10px; text-align: left; border-bottom: 1px solid #2a2a2a; }
th { color: #ff6b35; }
.card { background: #1a1a1a; border-radius: 8px; padding: 20px; margin: 15px 0; }
.vert { color: #4ade80; font-weight: bold; }
.orange { color: #fb923c; font-weight: bold; }
.rouge { color: #ef4444; font-weight: bold; }
.hypo { background: #2a2a2a; border-radius: 8px; padding: 15px; font-size: 0.9rem; }
.hypo code { color: #ff6b35; background: #1a1a1a; padding: 2px 6px; border-radius: 3px; }
.footer { margin-top: 40px; text-align: center; color: #666; font-size: 0.9rem; }
</style>
</head>
<body>
<h1>NEXORA - Rapport final</h1>
<p>Ville : Ouagadougou (Burkina Faso)</p>
<p>Date : """ + datetime.now().strftime("%d/%m/%Y %H:%M") + """</p>

<h2>0. Hypotheses utilisees</h2>
<div class="hypo">
<p><strong>Climat (Ouagadougou) :</strong></p>
<ul>
<li>Moyenne annuelle : <code>29 C</code>, <code>5.8 kWh/m2/jour</code></li>
<li>Mois chauds : <code>35 C</code>, <code>6.5 kWh/m2/jour</code></li>
<li>Canicule : <code>45 C</code>, <code>7.5 kWh/m2/jour</code></li>
<li>Meilleur ensoleillement : <code>32 C</code>, <code>7.0 kWh/m2/jour</code></li>
</ul>
<p><strong>Panneau :</strong></p>
<ul>
<li>Puissance nominale : <code>300 W</code></li>
<li>Surface : <code>1.72 m2</code></li>
<li>Rendement nominal : <code>20 %</code></li>
<li>Coefficient temperature : <code>-0.4 %/C</code></li>
<li>Modele NOCT : <code>T_cell = T_air + 3.5 x irradiation</code></li>
</ul>
<p><strong>Economie :</strong></p>
<ul>
<li>Prix kWh rural : <code>600 FCFA</code></li>
<li>Conso famille : <code>300 kWh/an</code> (6 personnes)</li>
<li>Installation village : <code>100 modules</code></li>
</ul>
</div>

<h2>1. Analyse climatique</h2>
<table>
<tr><th>Scenario</th><th>T air</th><th>T cellule</th><th>Rendement</th><th>Energie recue</th><th>Production</th><th>Coherent</th></tr>"""

for s, r in clim.items():
    icon = "OK" if r.get("coherent", True) else "KO"
    html += "<tr><td>" + r["description"] + "</td><td>" + str(r["T_air"]) + " C</td><td>" + str(r["T_cellule"]) + " C</td><td>" + str(r["rendement_absolu_pct"]) + " %</td><td>" + str(r.get("energie_recue_kwh_jour", "?")) + " kWh/j</td><td>" + str(r.get("production_kwh_jour", "?")) + " kWh/j</td><td>" + icon + "</td></tr>"

html += "</table><h2>2. Designs proposes</h2>"

for d in designs:
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an"] * 12, 1)
    html += '<div class="card"><h3>' + d["nom"] + '</h3><p>' + d["description"] + '</p>'
    html += "<p><strong>Materiaux :</strong></p><ul>"
    for m in d["materiaux"]:
        html += "<li>" + m + "</li>"
    html += "</ul><table>"
    html += "<tr><td>Cout total</td><td>" + str(d["cout_fcfa"]) + " FCFA</td></tr>"
    html += "<tr><td>Gain temperature</td><td>-" + str(d["gain_temp"]) + " C</td></tr>"
    html += "<tr><td>Gain rendement</td><td>+" + str(d["gain_rendement_pct"]) + " %</td></tr>"
    html += "<tr><td>Gain energie</td><td>+" + str(d["gain_kwh_an"]) + " kWh/an/module</td></tr>"
    html += "<tr><td>Gain economique</td><td>+" + str(int(d["gain_fcfa_an"])) + " FCFA/an</td></tr>"
    html += "<tr><td>Payback</td><td>" + str(payback) + " mois</td></tr>"
    html += "<tr><td>Habitants impactes (100 modules)</td><td>" + str(d["habitants_impactes"]) + " personnes</td></tr>"
    html += "<tr><td>Duree de vie</td><td>" + str(d["duree_vie_mois"]) + " mois</td></tr>"
    html += "</table></div>"

html += "<h2>3. Critique et notes</h2>"

for v in verdicts:
    if v["note"] >= 7:
        verdict_html = '<span class="vert">RECOMMANDE</span>'
    elif v["note"] >= 5:
        verdict_html = '<span class="orange">A RETRAVAILLER</span>'
    else:
        verdict_html = '<span class="rouge">NON RECOMMANDE</span>'
    html += '<div class="card"><h3>' + v["design"] + ' - ' + verdict_html + ' (note ' + str(v["note"]) + '/10)</h3>'
    html += "<p><strong>Payback :</strong> " + str(v["payback_mois"]) + " mois</p>"
    html += "<p><strong>Failles identifiees par le Critique :</strong></p>"
    html += "<p>" + v["failles"].replace("\n", "<br>") + "</p></div>"

best = max(verdicts, key=lambda x: x["note"])
html += '<h2>4. Recommandation finale</h2>'
html += '<div class="card">'
html += '<p><strong>Design recommande :</strong> ' + best["design"] + '</p>'
html += '<p><strong>Note :</strong> ' + str(best["note"]) + '/10</p>'
html += '<p><strong>Verdict :</strong> ' + best["verdict"] + '</p>'
html += '</div>'

html += '<div class="footer"><p>NEXORA - L\'IA qui invente pour le monde depuis l\'Afrique</p><p>Le feu ne doit jamais rester aux dieux.</p></div></body></html>'

with open("rapport_final.html", "w", encoding="utf-8") as f:
    f.write(html)

print("=" * 60)
print("   NEXORA - Rapport final genere")
print("=" * 60)
print()
print("Fichier : rapport_final.html")
print("Sections : hypotheses, analyse, designs, critique, recommandation")
print("=" * 60)

