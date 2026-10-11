import json

with open("sahel.json", "r", encoding="utf-8") as f:
    villes = json.load(f)

# Coordonnees GPS des villes
coords = {
    "Ouagadougou": [12.37, -1.52],
    "Bobo-Dioulasso": [11.18, -4.30],
    "Niamey": [13.51, 2.11],
    "Bamako": [12.65, -8.00],
    "N'Djamena": [12.11, 15.05]
}

# Construire les donnees JS
points = []
for v in villes:
    nom = v["ville"]
    if nom in coords:
        lat, lon = coords[nom]
        points.append({
            "nom": nom,
            "lat": lat,
            "lon": lon,
            "rend": v["rendement_absolu_pct"],
            "temp": v["temperature_cellule"]
        })

points_js = json.dumps(points)

html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NEXORA - Cartographe 3D</title>
<style>
  body { margin: 0; background: #0a0a0a; color: #e0e0e0; font-family: system-ui, sans-serif; overflow: hidden; }
  #info { position: absolute; top: 20px; left: 20px; z-index: 10; }
  h1 { color: #ff6b35; font-size: 1.5rem; margin: 0; }
  p { color: #888; font-size: 0.85rem; margin: 5px 0; }
  #legende { position: absolute; bottom: 20px; left: 20px; z-index: 10; font-size: 0.8rem; color: #aaa; }
  .point { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #ff6b35; margin-right: 8px; vertical-align: middle; }
</style>
</head>
<body>
<div id="info">
  <h1>NEXORA</h1>
  <p>Sahel - 5 villes analysees</p>
</div>
<div id="legende">
  <div><span class="point"></span>Ville (taille = rendement solaire)</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const points = ''' + points_js + ''';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 3;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Globe en fil de fer
const globeGeo = new THREE.SphereGeometry(1, 32, 32);
const globeMat = new THREE.MeshBasicMaterial({ color: 0x2a2a2a, wireframe: true, transparent: true, opacity: 0.4 });
const globe = new THREE.Mesh(globeGeo, globeMat);
scene.add(globe);

// Convertir lat/lon en position 3D
function latLonToXYZ(lat, lon, radius) {
  const phi = (90 - lat) * Math.PI / 180;
  const theta = (lon + 180) * Math.PI / 180;
  return {
    x: -radius * Math.sin(phi) * Math.cos(theta),
    y: radius * Math.cos(phi),
    z: radius * Math.sin(phi) * Math.sin(theta)
  };
}

// Ajouter les villes
points.forEach(p => {
  const pos = latLonToXYZ(p.lat, p.lon, 1.02);
  const taille = 0.02 + (p.rend / 100) * 0.08;
  const geo = new THREE.SphereGeometry(taille, 16, 16);
  const mat = new THREE.MeshBasicMaterial({ color: 0xff6b35 });
  const sphere = new THREE.Mesh(geo, mat);
  sphere.position.set(pos.x, pos.y, pos.z);
  scene.add(sphere);

  // Ligne vers le centre
  const lineGeo = new THREE.BufferGeometry().setFromPoints([
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(pos.x, pos.y, pos.z)
  ]);
  const lineMat = new THREE.LineBasicMaterial({ color: 0xff6b35, transparent: true, opacity: 0.3 });
  scene.add(new THREE.Line(lineGeo, lineMat));
});

// Rotation automatique
function animate() {
  requestAnimationFrame(animate);
  globe.rotation.y += 0.002;
  scene.children.forEach(c => {
    if (c.type === "Mesh" && c.geometry.type === "SphereGeometry" && c !== globe) {
      c.rotation.y = globe.rotation.y;
    }
  });
  renderer.render(scene, camera);
}
animate();

// Interaction tactile
let mouseDown = false, mouseX = 0;
document.addEventListener("mousedown", e => { mouseDown = true; mouseX = e.clientX; });
document.addEventListener("mouseup", () => mouseDown = false);
document.addEventListener("mousemove", e => {
  if (mouseDown) {
    globe.rotation.y += (e.clientX - mouseX) * 0.01;
    mouseX = e.clientX;
  }
});
document.addEventListener("touchstart", e => { mouseX = e.touches[0].clientX; });
document.addEventListener("touchmove", e => {
  globe.rotation.y += (e.touches[0].clientX - mouseX) * 0.01;
  mouseX = e.touches[0].clientX;
});

// Redimensionnement
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>'''

with open("cartographe3d.html", "w", encoding="utf-8") as f:
    f.write(html)

print("=" * 50)
print("   NEXORA - Cartographe 3D")
print("=" * 50)
print()
print("Villes cartographiees :", len(points))
for p in points:
    print("  " + p["nom"] + " : " + str(p["rend"]) + " %")
print()
print("Fichier genere : cartographe3d.html")
print("Ouvre-le dans ton navigateur.")
print()
print("=" * 50)

