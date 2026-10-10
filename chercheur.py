import requests

requete = "photovoltaic passive cooling"
url = f"https://api.crossref.org/works?query={requete.replace(' ', '+')}&rows=3&select=title,abstract,URL,published"

print("Recherche Crossref :", requete)
print()

reponse = requests.get(url, timeout=20)
if reponse.status_code == 200:
    data = reponse.json()
    articles = data.get("message", {}).get("items", [])
    if len(articles) == 0:
        print("Aucun article trouve.")
    for i, a in enumerate(articles, 1):
        print(f"--- Article {i} ---")
        titres = a.get("title", ["N/A"])
        print("Titre :", titres[0] if titres else "N/A")
        annee = a.get("published", {}).get("date-parts", [["N/A"]])[0][0]
        print("Annee :", annee)
        resume = a.get("abstract", "Pas de resume disponible")
        if resume and resume != "Pas de resume disponible":
            resume = resume.replace("<jats:p>", "").replace("</jats:p>", "")[:300]
        print("Resume :", resume, "...")
        print("Lien :", a.get("URL", "N/A"))
        print()
else:
    print("Erreur :", reponse.status_code)
