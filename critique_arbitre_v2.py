import json

with open("designs.json", "r", encoding="utf-8") as f:
    designs = json.load(f)

with open("analyse_climat.json", "r", encoding="utf-8") as f:
    clim = json.load(f)

print("=" * 60)
print("   NEXORA - Critique + Arbitre V2")
print("=" * 60)
print()

notes = []

for d in designs:
    print("--- Critique :", d["nom"], "---")
    failles = []
    
    if d["cout_fcfa"] / d["gain_fcfa_an"] * 12 > 24:
        failles.append("Payback superieur a 24 mois")
    if d["gain_temp"] > 10:
        failles.append("Gain de temperature optimiste")
    if "eau" in d["nom"].lower() and "Sahel" in str(clim):
        failles.append("Consommation d'eau a surveiller")
    if d["cout_fcfa"] > 20000:
        failles.append("Cout eleve pour un village")
    
    if not failles:
        failles.append("Aucune faille majeure identifiee")
    
    for f in failles:
        print("  -", f)
    
    # Note
    if len(failles) == 1 and failles[0] == "Aucune faille majeure identifiee":
        note = 8
    elif len(failles) <= 2:
        note = 6
    else:
        note = 4
    
    notes.append({"design": d["nom"], "note": note, "failles": failles})
    print()
    print("  Note Arbitre :", note, "/ 10")
    print()

# Decision finale
meilleur = max(notes, key=lambda x: x["note"])

print("=" * 60)
print("   VERDICT FINAL")
print("=" * 60)
print()
for n in notes:
    if n["note"] >= 7:
        verdict = "RECOMMANDE"
    elif n["note"] >= 5:
        verdict = "A RETRAVAILLER"
    else:
        verdict = "NON RECOMMANDE"
    print(n["design"], ":", verdict, "(note", n["note"], "/10)")
print()
print("Design recommande :", meilleur["design"])
print("=" * 60)

with open("verdict.json", "w", encoding="utf-8") as f:
    json.dump(notes, f, indent=2, ensure_ascii=False)

