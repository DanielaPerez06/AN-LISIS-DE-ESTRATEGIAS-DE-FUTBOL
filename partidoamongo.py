import json
from datetime import datetime
from partido import Partido
#este .py exporta el archivo parseado de apipartido (el de apipartido esta sin parsear) a mongoDB
def parse_fixture(fixture):
    partido = Partido()
    partido.partidoid = fixture['fixture']['id']
    partido.fecha = datetime.strptime(fixture['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
    partido.estado_partido = fixture['fixture']['status']['short']
    partido.equipos = {
        'casa': {
            'id': fixture['teams']['home']['id'],
            'nombre': fixture['teams']['home']['name'],
            'ganador': fixture['teams']['home']['winner']
        },
        'afuera': {
            'id': fixture['teams']['away']['id'],
            'nombre': fixture['teams']['away']['name'],
            'ganador': fixture['teams']['away']['winner']
        }
    }
    partido.goles = {
        'casa': fixture['goals']['home'],
        'afuera': fixture['goals']['away']
    }
    return "Datos extraidos"

def export_to_mongodb(partidos):
    for partido in partidos:
        # Verificar si el partido ya existe en la base de datos
        if not Partido.objects(partidoid=partido.partidoid):
            partido.save()  # Guarda el partido si no existe
        else:
            print(f"Partido con ID {partido.partidoid} ya existe y no será añadido de nuevo.")

if __name__ == '__main__':
    # Cargar el JSON desde el archivo
    with open('C:/Users/Daniela/Desktop/SEMESTRE 2/Proyecto Progra 2/partidos.json', 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    
    # Parsear cada fixture
    partidos = [parse_fixture(fixture) for fixture in data_json['response']]
    
    # Exportar a MongoDB
    export_to_mongodb(partidos)
    print("Datos exportados a MongoDB con éxito.")