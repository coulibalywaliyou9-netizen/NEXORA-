import requests
import json
import time

requete = "photovoltaic passive cooling tropical"
url = f"https://api.crossref.org/works?query={requete.replace(' ', '+')}&rows=3&select=title,abstract,URL,published"

print("Recherche Crossref :", requete)
print()

reponse = requests.get(url, timeout=20)
if reponse.status_code != 200:
    print("Erreur Crossref :", reponse.status_code)
    exit()

data = reponse.json()
articles = data.get("message", {}).get("items", [])

texte = "Voici les articles scientifiques trouves :\n\n"
for i, a in enumerate(articles, 1):
    titres = a.get("title", ["N/A"])
    titre = titres[0] if titres else "N/A"
    resume = a.get("abstract", "Pas de resume")
    if resume and resume != "Pas de resume":
        resume = resume.replace("<jats:p>", "").replace("</jats:p>", "")[:400]
    texte += f"--- Article {i} ---\nTitre : {titre}\nResume : {resume}\n\n"

with open(".groq_key", "r") as f:
    cle = f.read().strip()

question = f"{texte}\n\nTu es un ingenieur en energie solaire au Sahel. Analyse ces articles en 3 points : 1) Quel est le sujet principal de chaque article ? 2) Quelle strategie de refroidissement passif semble la plus prometteuse pour le Sahel ? 3) Comment pourrait-on l'adapter au Burkina Faso avec des materiaux locaux ?"

url_groq = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}
data_groq = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": question}]}

resultat = None
for essai in range(3):
    try:
        r2 = requests.post(url_groq, headers=headers, json=data_groq, timeout=30)
        resultat = r2.json()
        break
    except Exception as e:
        print("Tentative", essai + 1, "echouee")
        time.sleep(3)

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
