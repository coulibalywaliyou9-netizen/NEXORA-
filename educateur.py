import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

question = f"""Tu es un educateur populaire au Burkina Faso. Tu expliques la science aux villageois et aux ONG.

CONTEXTE :
- Ville : {r['ville']}
- Temperature cellule : {r['temperature_cellule']} C
- Rendement : {r['rendement_absolu_pct']} %
- Perte thermique : {r['perte_pct']} %

OBJECTIF :
Explique en langage TRES SIMPLE (comme si tu parlais a un villageois qui n'a jamais fait d'etudes scientifiques) :

1) Pourquoi un panneau solaire chauffe et perd de la puissance
2) Comment un simple systeme de refroidissement (eau, ventilation, peinture blanche) peut aider
3) Combien ca coute et combien ca rapporte, en FCFA
4) Comment un village peut le faire lui-meme, avec des materiaux locaux
5) Un exemple concret : "Si vous installez X, vous gagnez Y"

Utilise des metaphores simples (comparaison avec le corps humain, avec une marmite, etc.).
Pas de formules compliquees. Pas de vocabulaire scientifique.
Termine par un message d'encouragement pour les villageois."""

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
print("   NEXORA - Educateur")
print("=" * 50)
print()

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
