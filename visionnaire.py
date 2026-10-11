import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

question = f"Tu es un visionnaire en energie solaire pour l'Afrique. Voici la situation a {r['ville']} : temperature cellule {r['temperature_cellule']} C, rendement absolu {r['rendement_absolu_pct']} pourcent, perte {r['perte_pct']} pourcent. Propose 3 idees AUDACIEUSES, hors du cadre habituel, qui pourraient revolutionner le solaire au Sahel dans 5-10 ans. Pas des ameliorations incrementales. Des ruptures. Pour chaque idee : 1) le concept en une phrase, 2) pourquoi ca pourrait marcher, 3) quel obstacle majeur reste a surmonter. Sois creatif mais physiquement credible."

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
        time.sleep(3)

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
