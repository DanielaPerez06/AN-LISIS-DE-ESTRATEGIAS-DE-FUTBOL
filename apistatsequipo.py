import http.client
import json
from statsequipos import EstadisticasEquipo, PartidosStat, GolesStat

def fetch_teams_statistics(team_id):
    """Realiza una llamada a la API para obtener estadísticas de un fixture específico."""
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "1c453c5885e690c921d07a52ab17b489"
    }
    url = f"/teams/statistics?league=140&season=2024&team={team_id}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    return json.loads(data)


def parse_statistics(data):
    teamstats = data['response']
    
    # Verificamos si 'response' es una lista y accedemos al primer elemento
    if isinstance(teamstats, list):
        teamstats = teamstats[0]

    estadisticas = EstadisticasEquipo()
    estadisticas.equipoid = teamstats['team']['id']
    estadisticas.nombre = teamstats['team']['name']
    estadisticas.partidos_jugados = PartidosStat(
        total=teamstats['fixtures']['played']['total'],
        home=teamstats['fixtures']['played']['home'],
        away=teamstats['fixtures']['played']['away']
    )
    estadisticas.partidos_ganados = PartidosStat(
        total=teamstats['fixtures']['wins']['total'],
        home=teamstats['fixtures']['wins']['home'],
        away=teamstats['fixtures']['wins']['away']
    )
    estadisticas.empates = PartidosStat(
        total=teamstats['fixtures']['draws']['total'],
        home=teamstats['fixtures']['draws']['home'],
        away=teamstats['fixtures']['draws']['away']
    )
    estadisticas.partidos_perdidos = PartidosStat(
        total=teamstats['fixtures']['loses']['total'],
        home=teamstats['fixtures']['loses']['home'],
        away=teamstats['fixtures']['loses']['away']
    )
    estadisticas.goles_totales = GolesStat(
        total=teamstats['goals']['for']['total']['total'],
        home=teamstats['goals']['for']['total']['home'],
        away=teamstats['goals']['for']['total']['away']
    )
    # Si necesitas extraer más datos, asegúrate de acceder a ellos correctamente según la estructura mostrada
    return estadisticas

def export_to_mongodb(statistic):
    """Guarda las estadísticas parseadas en MongoDB."""
    statistic.save()

def load_team_ids():
    """Carga los IDs de los equipos desde un archivo JSON."""
    with open('C:/Users/Daniela/Desktop/SEMESTRE 2/Proyecto Progra 2/equipos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        ids = [team['team']['id'] for team in data['response']]
        subids = ids[10:20]
        return subids

def main():
    team_ids = load_team_ids()
    for team_id in team_ids:
        data = fetch_teams_statistics(team_id)
        estadisticas_equipo = parse_statistics(data)
        print(estadisticas_equipo)
        export_to_mongodb(estadisticas_equipo)
    print("Estadísticas de todos los equipos exportadas a MongoDB con éxito.")

if __name__ == '__main__':
    main()
