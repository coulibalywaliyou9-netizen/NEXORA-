import requests
url = "https://api.open-meteo.com/v1/forecast?latitude=12.37&longitude=-1.52&current=temperature_2m,wind_speed_10m"
d = requests.get(url).json()
Ta = d["current"]["temperature_2m"]
print("Air:", Ta, "C")
v = d["current"]["wind_speed_10m"]/3.6
T = Ta + 25*(1-5/100*v)
r = 1 - 4/1000*(T-25)
print("Cellule:", round(T,1), "C | Rendement:", round(r*100,1), "%")




