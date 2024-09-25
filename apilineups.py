#apiluneups.py
import http.client
import json
from lineups import Lineups, Player

def fetch_lineups_statistics(fixture_id):
    """Realiza una llamada a la API para obtener estadísticas de un fixture específico."""
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "1c453c5885e690c921d07a52ab17b489"
    }
    url = f"/fixtures/lineups?fixture={fixture_id}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)

def parse_lineups(data, fixture_id):
    parsed_stats = []
    for item in data['response']:
        lineup = Lineups()
        lineup.partidoid = fixture_id
        lineup.equipo = item['team']['name']
        lineup.formacion = item['formation']
        lineup.titulares = [
            Player(
                nombre=player['player']['name'],
                numero=player['player']['number'],
                posicion=player['player']['pos']
            )
            for player in item['startXI']
        ]
        parsed_stats.append(lineup)
    return parsed_stats


def export_to_mongodb(lineups):
    """Guarda las estadísticas parseadas en MongoDB."""
    for line in lineups:
        line.save()

def load_fixture_ids():
    """Carga los IDs de los fixtures desde un archivo JSON."""
    with open('C:/Users/Daniel Dupleich/Downloads/proyectoprogra2/proyectofacha/partidos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        ids = [match['fixture']['id'] for match in data['response']]
        subids = ids[0:1]
        return subids

def main():
    fixture_ids = load_fixture_ids()
    for fixture_id in fixture_ids:
        data = fetch_lineups_statistics(fixture_id)
        parsed_lineups = parse_lineups(data, fixture_id)
        export_to_mongodb(parsed_lineups)
    print("Estadísticas de todos los lineups exportadas a MongoDB con éxito.")

if __name__ == '_main_':
    main()