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
    "eolien.py": ("Eolien", "Tu es l'agent Eolien de NEXORA. Analyse le potentiel eolien de cette ville. Vitesse du vent, emplacement optimal, technologies adaptees au Sahel, cout estime en FCFA. Sois concret."),
    "hydro.py": ("Hydro", "Tu es l'agent Hydro de NEXORA. Analyse le potentiel hydroelectrique du Sahel. Barrages, micro-centrales, cours d'eau, saisonnalite, cout estime en FCFA."),
    "biomasse.py": ("Biomasse", "Tu es l'agent Biomasse de NEXORA. Analyse le potentiel biomasse. Dechets agricoles, biogaz, biocarburants, technologies adaptees, cout estime en FCFA."),
    "geothermie.py": ("Geothermie", "Tu es l'agent Geothermie de NEXORA. Analyse le potentiel geothermique du Sahel. Gradients thermiques, faisabilite, technologies, cout estime."),
    "reseau.py": ("Reseau", "Tu es l'agent Reseau de NEXORA. Analyse le reseau electrique. Pertes, smart grid, distribution, priorites d'investissement en FCFA."),
    "stockage.py": ("Stockage", "Tu es l'agent Stockage de NEXORA. Analyse les solutions de stockage d'energie. Batteries, hydrogene, volants d'inertie, cout en FCFA, duree de vie."),
    "atomique.py": ("Atomique", "Tu es l'agent Atomique de NEXORA. Analyse le potentiel nucleaire au Sahel. SMR, fusion, limites physiques, risques, horizon temporel realiste."),
    "prospecteur.py": ("Prospecteur", "Tu es l'agent Prospecteur de NEXORA. Explore 3 nouvelles sources d'energie meconnues ou emergentes (pas solaire/eolien/hydro classique). Sois creatif mais physiquement credible."),
    "integrateur.py": ("Integrateur", "Tu es l'agent Integrateur de NEXORA. Propose le mix energetique optimal pour cette ville. Repartition par source (en %), justification physique et economique, impact attendu."),
    "politique.py": ("Politique", "Tu es l'agent Politique de NEXORA. Propose une strategie nationale pour atteindre 100% d'acces a l'energie au Sahel. Reformes, investissements, horizons 5-10-20 ans."),
    "visualiseur3d.py": ("Visualiseur 3D", "Tu es l'agent Visualiseur 3D de NEXORA. Decris comment representer cette installation solaire en 3D (formes, couleurs, dimensions, animations). Sois technique."),
    "jumeaunumerique.py": ("Jumeau numerique", "Tu es l'agent Jumeau numerique de NEXORA. Decris comment creer un jumeau numerique d'une installation solaire (capteurs necessaires, donnees collectees, simulations possibles)."),
}

for nom_fichier, (nom_agent, prompt) in agents.items():
    code = template.replace("{PROMPT}", prompt).replace("{NOM}", nom_agent)
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(code)
    print("Cree :", nom_fichier)

print()
print("Total :", len(agents), "agents generes")

