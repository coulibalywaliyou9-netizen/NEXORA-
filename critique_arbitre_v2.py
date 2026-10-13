
import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("designs.json", "r", encoding="utf-8") as f:
    designs = json.load(f)

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": "Bearer " + cle, "Content-Type": "application/json"}

def appeler(prompt):
    data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": prompt}]}
    for essai in range(3):
        try:
            r = requests.post(url, headers=headers, json=data, timeout=60)
            resultat = r.json()
            if "choices" in resultat:
                return resultat["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(3)
    return ""

print("=" * 70)
print("   NEXORA - Critique + Arbitre V2.2 (realiste)")
print("=" * 70)
print()

notes = []

for d in designs:
    print("--- Critique : " + d["nom"] + " ---")
    print()
    
    payback = round(d["cout_fcfa"] / d["gain_fcfa_an_module"] * 12, 1)
    
    prompt = "Tu es un ingenieur critique de NEXORA, specialise en installations solaires au Sahel (Ouagadougou).\n\n"
    prompt += "Analyse ce design :\n"
    prompt += "- Nom : " + d["nom"] + "\n"
    prompt += "- Description : " + d["description"] + "\n"
    prompt += "- Materiaux : " + ", ".join(d["materiaux"]) + "\n"
    prompt += "- Cout : " + str(d["cout_fcfa"]) + " FCFA par module\n"
    prompt += "- Payback : " + str(payback) + " mois\n"
    prompt += "- Duree de vie estimee : " + str(d["duree_vie_mois"]) + " mois\n\n"
    
    prompt += "Donne 3 FAILLES CONCRETES et REALISTES.\n\n"
    prompt += "REGLES IMPORTANTES :\n"
    prompt += "- Reste au niveau des faiblesses de CONCEPTION, pas d'invention de defauts specifiques\n"
    prompt += "- Pas de chiffres inventes comme '3 mm de corrosion' ou '15 cm de vide'\n"
    prompt += "- Parle de risques generaux mais plausibles\n"
    prompt += "- Exemples acceptables : 'dependance a l'eau disponible', 'maintenance reguliere necessaire', 'duree de vie incertaine en conditions extremes'\n"
    prompt += "- Exemples interdits : 'fuite en 6 mois exactement', 'corrosion de X mm'\n\n"
    prompt += "Contexte terrain :\n"
    prompt += "- Ouagadougou : 35-45 C, poussiere abondante, saison des pluies 3 mois\n"
    prompt += "- Eau : ressource limitee dans certains villages\n"
    prompt += "- Maintenance : techniciens rares\n\n"
    prompt += "Reponds en 3 lignes numerotees. Sois precis mais realiste."
    
    critique = appeler(prompt)
    print(critique)
    print()
    
    if payback <= 18 and d["duree_vie_mois"] >= 24:
        note = 8
        verdict = "RECOMMANDE"
    elif payback <= 24:
        note = 6
        verdict = "A RETRAVAILLER"
    else:
        note = 4
        verdict = "NON RECOMMANDE"
    
    notes.append({
        "design": d["nom"],
        "note": note,
        "verdict": verdict,
        "failles": critique,
        "payback_mois": payback
    })
    
    print("  Note :", note, "/10 -", verdict)
    print()

with open("verdict.json", "w", encoding="utf-8") as f:
    json.dump(notes, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("   VERDICT FINAL")
print("=" * 70)
print()
for n in notes:
    print(n["design"] + " : " + n["verdict"] + " (note " + str(n["note"]) + "/10)")
print()
best = max(notes, key=lambda x: x["note"])
print("Meilleur design : " + best["design"])
print("=" * 70)

