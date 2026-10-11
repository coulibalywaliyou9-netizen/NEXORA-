import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

question = """Explique de facon EDUCATIVE et GENERALE :

1) Quels sont les differents types de protection pour un logiciel open source ?
   (droit d'auteur, licence MIT, GPL, Apache)

2) Qu'est-ce qu'une marque deposee et comment ca fonctionne ?

3) Qu'est-ce qu'un brevet logiciel et pourquoi c'est difficile a obtenir ?

4) Quels sont les organismes officiels en Afrique de l'Ouest (OAPI) pour la propriete intellectuelle ?

5) Comment une startup tech africaine peut proteger son travail avec un budget limite ?

Donne des informations generales et documentees, comme un cours d'introduction a la propriete intellectuelle. Pas de conseil juridique personnalise."""

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
print("   NEXORA - Juriste (educatif)")
print("=" * 50)
print()

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
