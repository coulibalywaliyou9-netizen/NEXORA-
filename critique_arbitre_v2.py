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

print("=" * 70)
print("   NEXORA - Critique + Arbitre V3 (notation nuancee)")
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
    prompt += "REGLES :\n"
    prompt += "- Reste au niveau des faiblesses de CONCEPTION\n"
    prompt += "- Pas de chiffres inventes (pas de '3 mm de corrosion')\n"
    prompt += "- Parle de risques plausibles et generaux\n"
    prompt += "- Contexte : Ouagadougou (35-45 C, poussiere, pluies 3 mois)\n\n"
    prompt += "Reponds en 3 lignes numerotees."
    
    critique = appeler(prompt)
    print(critique)
    print()
    
    # === NOUVELLE LOGIQUE DE NOTATION ===
    nb_failles = compter_failles(critique)
    gain = d["gain_kwh_an_module"]
    duree = d["duree_vie_mois"]
    
    # Etape 1 : score de base
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
    
    # Etape 2 : penalite failles
    if nb_failles >= 3:
        base = base - 0.5
    
    note = round(base, 1)
    
    # Etape 3 : statut final
    if note >= 8:
        verdict = "RECOMMANDE"
    elif 6.5 <= note < 8 and payback <= 12:
        verdict = "ALTERNATIVE LOW-COST"
    elif 6.5 <= note < 8:
        verdict = "A RETRAVAILLER"
    elif note >= 5:
        verdict = "A RETRAVAILLER"
    else:
        verdict = "NON RECOMMANDE"
    
    notes.append({
        "design": d["nom"],
        "note": note,
        "verdict": verdict,
        "failles": critique,
        "nb_failles": nb_failles,
        "payback_mois": payback
    })
    
    print("  Payback :", payback, "mois")
    print("  Duree :", duree, "mois")
    print("  Gain :", gain, "kWh/an")
    print("  Nombre de failles :", nb_failles)
    print("  Score de base :", base + 0.5 if nb_failles >= 3 else base)
    print("  Penalite failles :", "-0.5" if nb_failles >= 3 else "0")
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
print()
print("Legende :")
print("  RECOMMANDE          : design valide pour deploiement")
print("  ALTERNATIVE LOW-COST: design bon marche et rentable, mais failles a surveiller")
print("  A RETRAVAILLER      : design a ameliorer avant deploiement")
print("  NON RECOMMANDE      : design non viable")
print("=" * 70)

