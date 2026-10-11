template = '''import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

contexte = "Ville : " + r["ville"] + ". Temperature : " + str(r["temperature_cellule"]) + " C. Rendement : " + str(r["rendement_absolu_pct"]) + " %."

prompt = contexte + "\\n\\n" + """{PROMPT}"""

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": "Bearer " + cle, "Content-Type": "application/json"}
data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": prompt}]}

resultat = None
for essai in range(3):
    try:
        reponse = requests.post(url, headers=headers, json=data, timeout=60)
        resultat = reponse.json()
        break
    except Exception:
        time.sleep(3)

print("=" * 50)
print("   NEXORA - {NOM}")
print("=" * 50)
print()

if resultat is None:
    print("ERREUR")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API")
'''

agents = {
    "optimiseur.py": ("Optimiseur", "Tu es l'agent Optimiseur de NEXORA. Analyse le mix energetique optimal pour cette ville. Repartition par source (solaire, eolien, hydro, biomasse), justification, gain de rendement attendu, cout d'optimisation en FCFA."),
    "alertes.py": ("Alertes", "Tu es l'agent Alertes de NEXORA. Identifie 5 alertes potentielles pour cette installation solaire (surchauffe, poussiere, panne, vol, obsolescence). Pour chaque alerte : seuil, consequence, action preventive."),
    "cartographe2d.py": ("Cartographe 2D", "Tu es l'agent Cartographe 2D de NEXORA. Decris comment creer une carte 2D interactive du Sahel montrant les ressources energetiques par region (couleurs, donnees a afficher, interactions)."),
    "simulateur.py": ("Simulateur", "Tu es l'agent Simulateur de NEXORA. Simule 3 scenarios pour atteindre 100% d'acces a l'energie au Sahel : scenario 2026 (court terme), scenario 2030 (moyen terme), scenario 2040 (long terme). Pour chaque : cout, technologies, impact."),
    "hub_central.py": ("Hub Central", "Tu es le Hub Central de NEXORA. Produis un rapport de synthese qui resume TOUT le systeme : 34 agents actifs, sources d'energie couvertes, analyses produites, impact potentiel, prochaines etapes."),
}

for nom_fichier, (nom_agent, prompt) in agents.items():
    code = template.replace("{PROMPT}", prompt).replace("{NOM}", nom_agent)
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(code)
    print("Cree :", nom_fichier)

print()
print("Total :", len(agents), "agents generes")

