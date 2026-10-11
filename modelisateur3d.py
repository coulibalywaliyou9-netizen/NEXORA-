import json
import os

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

T = r["temperature_cellule"]
rend = r["rendement_absolu_pct"]

# Parametres du panneau
L = 1.65   # longueur en metres
W = 1.0    # largeur en metres
H = 0.04   # epaisseur en metres

# Support incline a 15 degres (optimal pour Ouagadougou)
angle = 15

# Calculs
nb_ailettes = 12
epaisseur_ailette = 0.002
hauteur_ailette = 0.05

scad = []
scad.append("// NEXORA - Plan 3D panneau solaire")
scad.append("// Ville : " + r["ville"])
scad.append("// Temperature cellule : " + str(T) + " C")
scad.append("// Rendement : " + str(rend) + " %")
scad.append("// Inclinaison : " + str(angle) + " degres")
scad.append("")

# Panneau principal
scad.append("// Panneau principal")
scad.append("color([0.1, 0.1, 0.3])")
scad.append("cube([%.2f, %.2f, %.3f]);" % (L, W, H))
scad.append("")

# Ailettes de refroidissement (sous le panneau)
scad.append("// Ailettes de refroidissement sous le panneau")
scad.append("color([0.7, 0.7, 0.7])")
for i in range(nb_ailettes):
    y = 0.1 + i * (W - 0.2) / (nb_ailettes - 1)
    scad.append("translate([0.1, %.3f, -%.3f])" % (y, hauteur_ailette))
    scad.append("cube([%.2f, %.3f, %.3f]);" % (L - 0.2, epaisseur_ailette, hauteur_ailette))
scad.append("")

# Support incline
scad.append("// Support incline")
scad.append("color([0.4, 0.2, 0.1])")
scad.append("translate([0.1, 0.1, -%.3f])" % hauteur_ailette)
scad.append("rotate([-%d, 0, 0])" % angle)
scad.append("cube([%.2f, %.2f, 0.05]);" % (L - 0.2, W - 0.2))
scad.append("")

# Pieds
scad.append("// Pieds du support")
scad.append("color([0.3, 0.3, 0.3])")
for x in [0.1, L - 0.15]:
    for y in [0.1, W - 0.15]:
        scad.append("translate([%.2f, %.2f, -0.6])" % (x, y))
        scad.append("cylinder(h=0.6, r=0.03);")
scad.append("")

# Legende
scad.append("// ---")
scad.append("// Vue de dessus recommandee dans OpenSCAD")
scad.append("// Pour exporter en STL : File > Export > Export as STL")

contenu = "\n".join(scad)

with open("panneau_3d.scad", "w", encoding="utf-8") as f:
    f.write(contenu)

print("=" * 50)
print("   NEXORA - Modelisateur 3D")
print("=" * 50)
print()
print("Ville :", r["ville"])
print("Panneau : " + str(L) + " m x " + str(W) + " m x " + str(H) + " m")
print("Inclinaison :", angle, "degres")
print("Ailettes de refroidissement :", nb_ailettes)
print()
print("Fichier genere : panneau_3d.scad")
print("Taille :", len(contenu), "caracteres")
print()
print("Pour visualiser : ouvrir sur un PC avec OpenSCAD (gratuit)")
print("Sur mobile : coller le contenu sur https://openscad.cloud")
print()
print("=" * 50)

