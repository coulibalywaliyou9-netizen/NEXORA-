import json
import requests

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

question = f"Tu es un ingenieur specialise en energie solaire au Sahel. Voici un rapport pour {r['ville']} : temperature cellule {r['temperature_cellule']} C, rendement absolu {r['rendement_absolu_pct']} pourcent, perte {r['perte_pct']} pourcent. Propose UNE solution concrete de refroidissement passif. Donne : 1) le design en 3 lignes, 2) les materiaux exacts, 3) le cout estime en FCFA, 4) la faisabilite locale au Burkina Faso, 5) l'impact attendu sur le rendement. Sois precis et realiste."

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}
data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": question}]}

resultat = None
for essai in range(3):
    try:
        reponse = requests.post(url, headers=headers, json=data, timeout=30)
        resultat = reponse.json()
        break
    except Exception as e:
        print("Tentative", essai + 1, "echouee")
        import time
        time.sleep(3)

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
