import http.client
import json
#Llama solamente 1 vez a la API devolviendo un documento con todos equipos de la liga española

# Configuración inicial y creación de la conexión
conn = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "1c453c5885e690c921d07a52ab17b489"
}
url = "/teams?league=140&season=2024"
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
filename = "equipos.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)

print(f"Datos guardados exitosamente en {filename}")