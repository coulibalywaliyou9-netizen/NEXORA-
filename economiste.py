import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

prix_kwh = 100

question = f"""Tu es un economiste specialise en energie solaire en Afrique de l'Ouest.

CONTEXTE :
- Ville : {r['ville']}
- Temperature cellule : {r['temperature_cellule']} C
- Rendement absolu actuel : {r['rendement_absolu_pct']} %
- Perte thermique : {r['perte_pct']} %
- Prix moyen du kWh au Burkina Faso : environ {prix_kwh} FCFA

OBJECTIF :
1) Estimer le gain annuel en kWh si on refroidit le panneau de 10 C (gain de rendement d'environ 4%)
2) Calculer ce que ca represente en FCFA par an pour un module de 300 W
3) Estimer le cout d'installation d'un systeme de refroidissement passif
4) Calculer le temps de retour sur investissement (payback) en annees
5) Donner une recommandation : est-ce rentable pour un village au Burkina Faso ?

Sois precis, realiste, et utilise des chiffres concrets en FCFA.
Termine par une conclusion claire : OUI c'est rentable / NON ce n'est pas rentable."""

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}
data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": question}]}

resultat = None
for essai in range(3):
    try:
        reponse = requests.post(url, headers=headers, json=data, timeout=60)
        resultat = reponse.json()
        break
    except Exception as e:
        print("Tentative", essai + 1, "echouee")
        time.sleep(3)

print("=" * 50)
print("   NEXORA - Economiste")
print("=" * 50)
print()

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
