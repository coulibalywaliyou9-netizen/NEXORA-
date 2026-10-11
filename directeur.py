import json
import requests
import time
import subprocess
import sys

with open(".groq_key", "r") as f:
    cle = f.read().strip()

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
print("   NEXORA - Directeur")
print("=" * 60)
print()

# Etape 1 : Physicien (calcul de base)
print(">>> Etape 1 : Le Physicien calcule la situation")
print()
subprocess.run([sys.executable, "rapport.py"], capture_output=True)
with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)
print("Ville :", r["ville"])
print("Temperature cellule :", r["temperature_cellule"], "C")
print("Rendement :", r["rendement_absolu_pct"], "%")
print()

contexte = "Ville : " + r["ville"] + ". Temperature cellule : " + str(r["temperature_cellule"]) + " C. Rendement : " + str(r["rendement_absolu_pct"]) + " %. Perte : " + str(r["perte_pct"]) + " %."

# Etape 2 : Le Directeur decide de la suite
print(">>> Etape 2 : Le Directeur analyse la situation et decide")
print()
prompt_decision = contexte + """

Tu es le Directeur de NEXORA. Tu as 13 agents a ta disposition :
- Chercheur (lit la science mondiale)
- Physicien (calcule la physique)
- Critique (verifie la plausibilite)
- Analyste (raisonne avec l'IA)
- Explorateur (explore les ruptures technologiques)
- Ingenieur (concoit un design)
- Economiste (chiffre la rentabilite)
- Juriste (protege la propriete intellectuelle)
- Educateur (vulgarise pour les villages)
- Visionnaire (imagine le futur)
- Memoire (archive)
- Historien (analyse les tendances)
- Arbitre (decide de la qualite finale)

QUESTION : Quel est le probleme le plus important a analyser aujourd'hui ?
Reponds en UNE PHRASE en te concentrant sur ce qui apporterait le plus de valeur."""

decision = appeler(prompt_decision)
print("Probleme prioritaire :", decision)
print()

# Etape 3 : L'Ingenieur propose
print(">>> Etape 3 : L'Ingenieur propose un design")
print()
prompt_ing = contexte + "\n\nTu es l'Ingenieur de NEXORA. Propose UN design de refroidissement passif pour ce probleme :\n\n" + decision + "\n\nDesign en 3 lignes, materiaux, cout en FCFA."
design = appeler(prompt_ing)
print(design)
print()

# Etape 4 : Le Critique challenge
print(">>> Etape 4 : Le Critique challenge le design")
print()
prompt_crit = "Tu es le Critique de NEXORA. Design propose :\n\n" + design + "\n\nTrouve 3 failles CONCRETES. Sois impitoyable."
critique = appeler(prompt_crit)
print(critique)
print()

# Etape 5 : L'Arbitre decide
print(">>> Etape 5 : L'Arbitre decide")
print()
prompt_arb = """Tu es l'Arbitre de NEXORA. Un Ingenieur a propose un design, le Critique a trouve des failles.

Decide en 8 lignes max :
1) Le design est-il accepte ? OUI ou NON
2) Note sur 10
3) 1 point a ameliorer en priorite
4) Recommandation finale en 1 phrase."""

arbitre = appeler(prompt_arb)
print(arbitre)
print()

# Etape 6 : Synthese finale
print("=" * 60)
print("   Synthese du Directeur")
print("=" * 60)
print()

prompt_synth = "Tu es le Directeur de NEXORA. Voici le travail du jour :\n\n- Probleme analyse : " + decision + "\n\n- Design propose : " + design + "\n\n- Verdict de l'Arbitre : " + arbitre + "\n\nProduis une synthese en 5 lignes pour le rapport final. Sois clair et direct."

synthese = appeler(prompt_synth)
print(synthese)
print()

# Archivage
with open("historique.json", "r", encoding="utf-8") as f:
    h = json.load(f)
h.append({"date": time.strftime("%Y-%m-%d %H:%M:%S"), "rapport": r, "synthese": synthese})
with open("historique.json", "w", encoding="utf-8") as f:
    json.dump(h, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("   Cycle Directeur termine")
print("=" * 60)

