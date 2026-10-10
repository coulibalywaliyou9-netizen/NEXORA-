import json
import requests

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

question = f"Tu es un physicien du photovoltaique. Voici un rapport pour {r['ville']} : temperature air {r['temperature_air']} C, temperature cellule {r['temperature_cellule']} C, rendement absolu {r['rendement_absolu_pct']} pourcent, rendement relatif {r['rendement_relatif_pct']} pourcent, perte {r['perte_pct']} pourcent. Analyse en 3 points : 1) coherence des valeurs, 2) principale perte, 3) une piste d'amelioration."

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}
data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": question}]}

reponse = requests.post(url, headers=headers, json=data)
resultat = reponse.json()

if "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
