import subprocess
import sys

print("=" * 60)
print("   NEXORA V2 - Cycle complet")
print("=" * 60)
print()

etapes = [
    ("1. Physicien (analyse climatique)", "physicien_v2.py"),
    ("2. Ingenieur (designs robustes)", "ingenieur_v2.py"),
    ("3. Critique + Arbitre", "critique_arbitre_v2.py"),
    ("4. Rapport final HTML", "rapport_final.py")
]

for nom, fichier in etapes:
    print()
    print(">>> " + nom)
    print()
    r = subprocess.run([sys.executable, fichier], capture_output=True, text=True)
    if r.returncode == 0:
        print(r.stdout)
    else:
        print("ERREUR :", r.stderr[:500])
        break

print()
print("=" * 60)
print("   Cycle NEXORA V2 termine")
print("=" * 60)
print()
print("Rapport final : rapport_final.html")

