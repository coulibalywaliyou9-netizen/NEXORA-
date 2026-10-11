import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

contexte = "Ville : " + r["ville"] + ". Temperature : " + str(r["temperature_cellule"]) + " C. Rendement : " + str(r["rendement_absolu_pct"]) + " %."

prompt = contexte + "\n\n" + """Tu es l'agent Reseau de NEXORA. Analyse le reseau electrique. Pertes, smart grid, distribution, priorites d'investissement en FCFA."""

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
print("   NEXORA - Reseau")
print("=" * 50)
print()

if resultat is None:
    print("ERREUR")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API")
