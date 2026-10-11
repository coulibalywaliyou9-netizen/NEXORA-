import subprocess
import sys

print("=" * 50)
print("   NEXORA - Orchestrateur")
print("=" * 50)

etapes = [
    ("Chercheur", "chercheur.py"),
    ("Physicien", "rapport.py"),
    ("Critique", "critique.py"),
    ("Analyste", "analyste.py"),
    ("Ingenieur", "ingenieur.py"),
    ("Memoire", "memoire.py")
]
for nom, fichier in etapes:
    print()
    print("--- Etape :", nom, "---")
    resultat = subprocess.run(
        [sys.executable, fichier],
        capture_output=True,
        text=True
    )
    if resultat.returncode == 0:
        print(resultat.stdout)
    else:
        print("ERREUR dans", fichier)
        print(resultat.stderr)
        break

print()
print("=" * 50)
print("   Cycle NEXORA termine")
print("=" * 50)
