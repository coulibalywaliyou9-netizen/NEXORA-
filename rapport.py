import requests, json
url = "https://api.open-meteo.com/v1/forecast?latitude=12.37&longitude=-1.52&current=temperature_2m,wind_speed_10m"
d = requests.get(url).json()
Ta = d["current"]["temperature_2m"]
v = d["current"]["wind_speed_10m"]/3.6
T = Ta + 25*(1-5/100*v)
r = 1 - 4/1000*(T-25)
rapport = {
    "ville": "Ouagadougou",
    "temperature_air": round(Ta, 1),
    "temperature_cellule": round(T, 1),
    "rendement_relatif_pct": round(r*100, 1),
    "rendement_absolu_pct": round(0.20 * r * 100, 1),
    "perte_pct": round((1-r)*100, 1)
}
print(json.dumps(rapport, indent=2, ensure_ascii=False))
with open("rapport.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)
