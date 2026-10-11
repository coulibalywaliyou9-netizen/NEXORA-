// NEXORA - Plan 3D panneau solaire
// Ville : Ouagadougou
// Temperature cellule : 56.8 C
// Rendement : 17.5 %
// Inclinaison : 15 degres

// Panneau principal
color([0.1, 0.1, 0.3])
cube([1.65, 1.00, 0.040]);

// Ailettes de refroidissement sous le panneau
color([0.7, 0.7, 0.7])
translate([0.1, 0.100, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.173, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.245, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.318, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.391, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.464, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.536, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.609, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.682, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.755, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.827, -0.050])
cube([1.45, 0.002, 0.050]);
translate([0.1, 0.900, -0.050])
cube([1.45, 0.002, 0.050]);

// Support incline
color([0.4, 0.2, 0.1])
translate([0.1, 0.1, -0.050])
rotate([-15, 0, 0])
cube([1.45, 0.80, 0.05]);

// Pieds du support
color([0.3, 0.3, 0.3])
translate([0.10, 0.10, -0.6])
cylinder(h=0.6, r=0.03);
translate([0.10, 0.85, -0.6])
cylinder(h=0.6, r=0.03);
translate([1.50, 0.10, -0.6])
cylinder(h=0.6, r=0.03);
translate([1.50, 0.85, -0.6])
cylinder(h=0.6, r=0.03);

// ---
// Vue de dessus recommandee dans OpenSCAD
// Pour exporter en STL : File > Export > Export as STL