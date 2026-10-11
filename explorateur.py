import json
import requests
import time

with open(".groq_key", "r") as f:
    cle = f.read().strip()

with open("rapport.json", "r", encoding="utf-8") as f:
    r = json.load(f)

T_chaud = r["temperature_cellule"]
T_froid = 25

carnot = 1 - (T_froid + 273.15) / (T_chaud + 273.15)

question = f"""Tu es un physicien specialise en conversion d'energie et thermoelectriques.

CONTEXTE :
- Panneau solaire a {r['ville']}
- Temperature cellule : {T_chaud} C
- Temperature ambiante : {T_froid} C
- Perte thermique actuelle : {r['perte_pct']} %
- Rendement de Carnot theorique a cet ecart : {round(carnot*100, 2)} %

OBJECTIF :
Explorer les technologies qui pourraient CONVERTIR cette chaleur en ELECTRICITE (pas seulement la dissiper).

Pour chaque piste, donne :
1) Le nom de la technologie
2) Le principe physique en 1 phrase
3) Le rendement attendu a cette temperature (realiste, pas theorique)
4) Le cout estime pour un module de 300 W
5) La faisabilite locale au Burkina Faso
6) La maturite : aujourd'hui / 5 ans / 10 ans

Pistes a explorer obligatoirement :
- Generateurs thermoelectriques (TEG)
- Cycle Organique de Rankine (ORC) miniaturise
- Cellules photovoltaiques tandem (perovskite + silicium)
- Piezoelectriques thermiques
- Materiaux a changement de phase couples a un generateur
- Antennes rectenna infrarouge

Puis compare ces pistes avec le refroidissement passif.
Reponds de facon honnete : dis clairement ce qui est realiste aujourd'hui et ce qui releve de la recherche.
Termine par une recommandation strategique : que doit explorer NEXORA en priorite pour rester a la pointe ?"""

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {cle}", "Content-Type": "application/json"}
data = {"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": question}]}

resultat = None
for essai in range(3):
    try:
        reponse = requests.post(url, headers=headers, json=data, timeout=60)
        resultat = reponse.json()
        break
    except Exception as e:
        print("Tentative", essai + 1, "echouee")
        time.sleep(3)

print("=" * 50)
print("   NEXORA - Explorateur de ruptures")
print("=" * 50)
print()
print("Ecart de temperature :", T_chaud - T_froid, "C")
print("Rendement de Carnot :", round(carnot*100, 2), "%")
print()

if resultat is None:
    print("ERREUR : impossible de contacter l'API")
elif "choices" in resultat:
    print(resultat["choices"][0]["message"]["content"])
else:
    print("ERREUR API :", resultat)
