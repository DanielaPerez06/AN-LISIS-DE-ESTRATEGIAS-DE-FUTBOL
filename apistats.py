#apistats.py
import http.client
import json
from stats import Stats  # Importar la clase Stats desde stats.py

def fetch_fixture_statistics(fixture_id):
    """Realiza una llamada a la API para obtener estadísticas de un fixture específico."""
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "4daf2bf859774911ea3da63998071a7b"
    }
    url = f"/fixtures/statistics?fixture={fixture_id}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)

def parse_statistics(data, fixture_id):
    """Parsea las estadísticas del partido y las prepara para la base de datos."""
    parsed_stats = []
    for item in data['response']:
        stats = Stats()
        stats.partidoid = fixture_id
        stats.equipo = item['team']['name']
        stats.estadisticas = {stat['type']: stat['value'] for stat in item['statistics']}
        parsed_stats.append(stats)
    return parsed_stats

def export_to_mongodb(statistics):
    """Guarda las estadísticas parseadas en MongoDB."""
    for stat in statistics:
        stat.save()

def load_fixture_ids():
    """Carga los IDs de los fixtures desde un archivo JSON."""
    with open('/proyectofacha/partidos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        ids = [match['fixture']['id'] for match in data['response']]
        subids = ids[30:40]
        return subids

def main():
    fixture_ids = load_fixture_ids()
    for fixture_id in fixture_ids:
        data = fetch_fixture_statistics(fixture_id)
        parsed_statistics = parse_statistics(data, fixture_id)
        export_to_mongodb(parsed_statistics)
    print("Estadísticas de todos los fixtures exportadas a MongoDB con éxito.")

if __name__ == '_main_':
    main()