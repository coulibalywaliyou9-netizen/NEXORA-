import subprocess
import sys

print("=" * 60)
print("   NEXORA - Orchestrateur complet (34 agents)")
print("=" * 60)

etapes = [
    # --- SCIENCE ET ANALYSE ---
    ("Chercheur", "chercheur.py"),
    ("Physicien", "rapport.py"),
    ("Critique", "critique.py"),
    ("Analyste", "analyste.py"),
    ("Explorateur", "explorateur.py"),
    
    # --- INGENIERIE ET DECISION ---
    ("Ingenieur", "ingenieur.py"),
    ("Economiste", "economiste.py"),
    ("Juriste", "juriste.py"),
    ("Educateur", "educateur.py"),
    
    # --- VISION ET STRATEGIE ---
    ("Visionnaire", "visionnaire.py"),
    ("Memoire", "memoire.py"),
    ("Historien", "historien.py"),
    ("Stratege", "stratege.py"),
    
    # --- ENERGIE : SOURCES ---
    ("Eolien", "eolien.py"),
    ("Hydro", "hydro.py"),
    ("Biomasse", "biomasse.py"),
    ("Geothermie", "geothermie.py"),
    
    # --- ENERGIE : INFRASTRUCTURE ---
    ("Reseau", "reseau.py"),
    ("Stockage", "stockage.py"),
    ("Atomique", "atomique.py"),
    
    # --- ENERGIE : EXPLORATION ---
    ("Prospecteur", "prospecteur.py"),
    ("Integrateur", "integrateur.py"),
    ("Politique", "politique.py"),
    
    # --- OPTIMISATION ET SURVEILLANCE ---
    ("Optimiseur", "optimiseur.py"),
    ("Alertes", "alertes.py"),
    
    # --- 3D ET SIMULATION ---
    ("Modelisateur3D", "modelisateur3d.py"),
    ("Cartographe3D", "cartographe3d.py"),
    ("Visualiseur3D", "visualiseur3d.py"),
    ("JumeauNumerique", "jumeaunumerique.py"),
    ("Cartographe2D", "cartographe2d.py"),
    ("Simulateur", "simulateur.py"),
    
    # --- SYNTHESE FINALE ---
    ("HubCentral", "hub_central.py")
]

total = len(etapes)
reussis = 0
echoues = 0

for i, (nom, fichier) in enumerate(etapes, 1):
    print()
    print("[" + str(i) + "/" + str(total) + "] --- " + nom + " ---")
    try:
        resultat = subprocess.run(
            [sys.executable, fichier],
            capture_output=True,
            text=True,
            timeout=120
        )
        if resultat.returncode == 0:
            print(resultat.stdout)
            reussis += 1
        else:
            print("ERREUR dans", fichier)
            print(resultat.stderr[:500])
            echoues += 1
    except subprocess.TimeoutExpired:
        print("TIMEOUT dans", fichier)
        echoues += 1
    except FileNotFoundError:
        print("Fichier introuvable :", fichier)
        echoues += 1

print()
print("=" * 60)
print("   Cycle NEXORA termine")
print("=" * 60)
print("Agents reussis :", reussis, "/", total)
print("Agents echoues :", echoues)
print()

