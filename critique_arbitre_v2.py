

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

def compter_failles(texte):
    lignes = [l for l in texte.split("\n") if l.strip() and l.strip()[0].isdigit()]
    return len(lignes)

def evaluer_gravite(texte):
    graves = ["fissure", "rupture", "effondrement", "corrosion", "contamination", "inefficacite", "perte totale", "obstruction", "fuite", "degradation"]
    texte_lower = texte.lower()
    count = sum(1 for mot in graves if mot in texte_lower)
    if count >= 3:
        return "grave"
    elif count >= 2:
        return "moderee"
    else:
        return "faible"

print("=" * 70)
print("   NEXORA - Critique + Arbitre V5 (notation juste)")
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
    prompt += "- Duree de vie : " + str(d["duree_vie_mois"]) + " mois\n\n"
    prompt += "Donne JUSQU'A 3 FAILLES CONCRETES. Si tu n'en vois que 1 ou 2, dis-le.\n"
    prompt += "Contexte : Ouagadougou (35-45 C, poussiere, pluies 3 mois).\n"
    prompt += "Reponds en lignes numerotees."
    
    critique = appeler(prompt)
    print(critique)
    print()
    
    nb_failles = compter_failles(critique)
    gravite = evaluer_gravite(critique)
    gain = d["gain_kwh_an_module"]
    duree = d["duree_vie_mois"]
    
    if payback <= 12 and duree >= 36:
        base = 9
    elif payback <= 18 and duree >= 36 and gain >= 18:
        base = 8
    elif payback <= 12:
        base = 7
    elif payback <= 18 and duree >= 36:
        base = 7
    elif payback <= 24:
        base = 6
    else:
        base = 4
    
    # Nouvelle regle : seule les 3 failles GRAVES penalisent
    if nb_failles >= 3 and gravite == "grave":
        penalite = 0.5
    else:
        penalite = 0
    
    note = round(base - penalite, 2)
    
    if note >= 8:
        verdict = "RECOMMANDE"
    elif 6.5 <= note < 8 and payback <= 12:
        verdict = "ALTERNATIVE LOW-COST"
    elif 6.5 <= note < 8:
        verdict = "A RETRAVAILLER"
    else:
        verdict = "NON RECOMMANDE"
    
    notes.append({
        "design": d["nom"],
        "note": note,
        "verdict": verdict,
        "failles": critique,
        "nb_failles": nb_failles,
        "gravite": gravite,
        "payback_mois": payback
    })
    
    print("  Payback :", payback, "| Duree :", duree, "| Gain :", gain)
    print("  Nb failles :", nb_failles, "| Gravite :", gravite)
    print("  Score de base :", base, "| Penalite :", penalite)
    print("  NOTE FINALE :", note, "/10 -", verdict)
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


