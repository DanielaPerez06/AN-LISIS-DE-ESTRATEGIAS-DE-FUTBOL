#apipartido.py
import http.client
import json

# Configuración inicial y creación de la conexión
conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "6e6664a36ba256acc1662fe2be9a48b2"
}
url = "/fixtures?league=140&season=2024&from=2024-08-15&to=2024-09-07"
conn.request("GET", url, headers=headers)

# Obteniendo la respuesta
res = conn.getresponse()
data = res.read()

# Cerrar la conexión
conn.close()

# Convertir los datos recibidos a formato JSON
try:
    data_json = json.loads(data.decode("utf-8"))
except json.JSONDecodeError:
    print("No se pudo decodificar la respuesta JSON")
    exit()

# Guardar los datos en un archivo JSON
filename = "partidos.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

print(f"Datos guardados exitosamente en {filename}")