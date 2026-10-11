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


print("=" * 50)
print("   NEXORA - Debat entre agents")
print("=" * 50)
print()

contexte = "Ville : " + r["ville"] + ". Temperature cellule : " + str(r["temperature_cellule"]) + " C. Rendement : " + str(r["rendement_absolu_pct"]) + " %. Perte : " + str(r["perte_pct"]) + " %."

print(">>> TOUR 1 : L'Ingenieur propose un design")
print()
prompt1 = contexte + "\n\nTu es l'Ingenieur de NEXORA. Propose UN design concret de refroidissement passif adapte au Sahel. Sois bref : design en 3 lignes, materiaux, cout en FCFA."
design1 = appeler(prompt1)
print(design1)
print()

print(">>> TOUR 2 : Le Critique challenge le design")
print()
prompt2 = contexte + "\n\nTu es le Critique de NEXORA. Voici le design propose :\n\n" + design1 + "\n\nTrouve 3 failles CONCRETES. Sois impitoyable."
critique1 = appeler(prompt2)
print(critique1)
print()

print(">>> TOUR 3 : L'Ingenieur revise")
print()
prompt3 = contexte + "\n\nTu es l'Ingenieur. Design initial :\n\n" + design1 + "\n\nCritiques :\n\n" + critique1 + "\n\nREVISE ton design. Sois concret. 3 lignes + cout mis a jour."
design2 = appeler(prompt3)
print(design2)
print()

print(">>> TOUR 4 : Le Critique valide ou challenge")
print()
prompt4 = "Tu es le Critique de NEXORA. Design revise :\n\n" + design2 + "\n\nAcceptable ? OUI ou NON, puis justifie en 2-3 phrases."
critique2 = appeler(prompt4)
print(critique2)
print()

print(">>> TOUR 5 : L'Arbitre decide")
print()
prompt5 = """Tu es l'Arbitre de NEXORA. Tu as suivi un debat entre un Ingenieur et un Critique sur un design de refroidissement solaire au Sahel.

Resume : l'Ingenieur a propose un design, le Critique a trouve des failles, l'Ingenieur a revise, le Critique a encore refuse.

Decide en 10 lignes max :
1) Le design merite-t-il d'etre presente a un client ? OUI ou NON
2) 2 points a ameliorer en priorite
3) Note sur 10
4) Recommandation finale en 1 phrase."""

arbitre = appeler(prompt5)
print(arbitre)
print()

print("=" * 50)
print("   Fin du debat")
print("=" * 50)

