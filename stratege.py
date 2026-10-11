import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}


def appeler(prompt):
    data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": prompt}]}
    for essai in range(3):
        try:
            reponse = requests.post(url, headers=headers, json=data, timeout=60)
            resultat = reponse.json()
            if "choices" in resultat:
                return resultat["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(3)
    return "ERREUR"


print("=" * 60)
print("   NEXORA - Stratege")
print("=" * 60)
print()

contexte = "NEXORA est un systeme d'IA a 14 agents, developpe au Burkina Faso. Il analyse et concoit des solutions solaires pour le Sahel. Il est open source sur GitHub. Il est deja fonctionnel et public."

prompt = contexte + """

Tu es le Stratege de NEXORA. Ta mission est d'identifier les meilleures opportunites pour financer et faire grandir ce projet.

Reponds aux 5 questions suivantes :

1) SUBVENTIONS ET CONCOURS : Cite 5 programmes reels qui financent les projets tech/IA/climat en Afrique (avec montant approximatif et site web). Exemples : Digital Energy Challenge, Tony Elumelu, Google for Startups, etc.

2) INVESTISSEURS : Identifie 3 types d'investisseurs potentiels (impact, climat, IA) actifs en Afrique.

3) STRATEGIE 6 MOIS : Quelles sont les 3 actions prioritaires a faire dans les 6 prochains mois pour passer de projet perso a projet finance ?

4) STRATEGIE 24 MOIS : Quelle pourrait etre la trajectoire ideale sur 2 ans (startup, ONG, collaboration, acquisition) ?

5) RISQUES : Quels sont les 3 risques principaux pour NEXORA (techniques, juridiques, marche) ?

Sois CONCRET et ACTIONNABLE. N'invente pas de programmes qui n'existent pas. Si tu n'es pas sur d'un programme, dis-le."""

resultat = appeler(prompt)

print(resultat)
print()
print("=" * 60)
print("   Fin de la strategie")
print("=" * 60)

