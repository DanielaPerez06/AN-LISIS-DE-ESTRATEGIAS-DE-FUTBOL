import json
from equipos import Equipos


# este .py exporta el archivo parseado de apipartido (el de apipartido esta sin parsear) a mongoDB
def parse_teams(team):
    equipo = Equipos()
    equipo.equipoid = team['id']
    equipo.nombre = team['name']
    equipo.logo = team['logo']
    return equipo


def export_to_mongodb(teams):
    for equipo in teams:
        # Verificar si el equipo ya existe en la base de datos
        if not Equipos.objects(equipoid=equipo.equipoid):
            equipo.save()  # Guarda el equipo si no existe
        else:
            print(f"Equipo con ID {equipo.equipoid} ya existe y no será añadido de nuevo.")

if __name__ == '__main__':
    # Cargar el JSON desde el archivo
    with open('C:/Users/Daniela/Desktop/SEMESTRE 2/Proyecto Progra 2/equipos.json', 'r', encoding='utf-8') as f:
        data_json = json.load(f)

    # Parsear cada equipo
    equipos = [parse_teams(team['team']) for team in data_json['response']]

    # Exportar a MongoDB
    export_to_mongodb(equipos)
    print("Datos de equipos exportados a MongoDB con éxito.")