from partido import Partido
from stats import Stats
from lineups import Lineups
import os
import io
import matplotlib.image as mpimg
import urllib.request
from PIL import Image
from equipos import Equipos
from statsequipos import EstadisticasEquipo
class ControladorUsuario:
    def obtener_partidos(self):
        resultados = []
        for partido in Partido.objects:
            fecha_formateada = partido.fecha.strftime('%d/%m/%y')
            datos_partido = {
                'ID partido': partido.partidoid,
                'Fecha': fecha_formateada,
                'Equipo Casa': partido.equipos['casa']['nombre'],
                'Equipo Visitante': partido.equipos['afuera']['nombre'],
                'Goles Casa': partido.goles['casa'],
                'Goles Visitante': partido.goles['afuera']
            }
            resultados.append(datos_partido)
        return resultados

    def obtener_stats(self, partidoid):
        resultados = []
        for estadistica in Stats.objects(partidoid=partidoid):
            stats_partido = {
                'ID del Partido': estadistica.partidoid,
                'Equipo': estadistica.equipo,
                'Tiros al arco': estadistica.estadisticas.get('Shots on Goal', 'No disponible'),
                'Tiros desviados': estadistica.estadisticas.get('Shots off Goal', 'No disponible'),
                'Total de tiros': estadistica.estadisticas.get('Total Shots', 'No disponible'),
                'Tiros bloqueados': estadistica.estadisticas.get('Blocked Shots', 'No disponible'),
                'Tiros dentro del área': estadistica.estadisticas.get('Shots insidebox', 'No disponible'),
                'Tiros fuera del área': estadistica.estadisticas.get('Shots outsidebox', 'No disponible'),
                'Faltas': estadistica.estadisticas.get('Fouls', 'No disponible'),
                'Córners': estadistica.estadisticas.get('Corner Kicks', 'No disponible'),
                'Posesión del balón': estadistica.estadisticas.get('Ball Possession', 'No disponible'),
                'Tarjetas amarillas': estadistica.estadisticas.get('Yellow Cards', 'No disponible'),
                'Tarjetas rojas': estadistica.estadisticas.get('Red Cards', 'No disponible'),
                'Fueras de juego': estadistica.estadisticas.get('Offsides', 'No disponible'),
                'Paradas del portero': estadistica.estadisticas.get('Goalkeeper Saves', 'No disponible'),
                'Pases totales': estadistica.estadisticas.get('Total passes', 'No disponible'),
                'Pases completados': estadistica.estadisticas.get('Passes accurate', 'No disponible'),
                'Porcentaje de pases': estadistica.estadisticas.get('Passes %', 'No disponible'),
                'Goles esperados': estadistica.estadisticas.get('expected_goals', 'No disponible'),
                'Goles prevenidos': estadistica.estadisticas.get('goals_prevented', 'No disponible'),
            }
            resultados.append(stats_partido)
        return resultados

    def obtener_lineups(self, partidoid):
        resultados = []
        for lineup in Lineups.objects(partidoid=partidoid):
            titulares = []
            for titular in lineup.titulares:
                jugador_info = {
                    'Nombre': titular.nombre,
                    'Numero': titular.numero,
                    'Posicion': titular.posicion,
                    'Posición en gráfico': titular.grid,
                }
                titulares.append(jugador_info)
            lineuppartido = {
                'Partido ID': lineup.partidoid,
                'Equipo': lineup.equipo,
                'Formacion': lineup.formacion,
                'Jugadores': titulares
            }
            resultados.append(lineuppartido)
        return resultados

    def obtener_equipos(self):
        resultados = []
        for equipo in Equipos.objects:
            datos_equipo = {
                'ID del Equipo': equipo.equipoid,
                'Nombre': equipo.nombre,
                'Logo': equipo.logo
            }
            resultados.append(datos_equipo)
        return resultados

    def obtener_estadisticas_equipo(self, equipoid):
        resultados = []
        for estadistica in EstadisticasEquipo.objects(equipoid=equipoid):
            datos_equipo = {
                'ID del Equipo': estadistica.equipoid,
                'Nombre': estadistica.nombre,
                'Partidos Jugados': {
                    'Total': estadistica.partidos_jugados.total,
                    'En Casa': estadistica.partidos_jugados.home,
                    'Fuera': estadistica.partidos_jugados.away
                },
                'Partidos Ganados': {
                    'Total': estadistica.partidos_ganados.total,
                    'En Casa': estadistica.partidos_ganados.home,
                    'Fuera': estadistica.partidos_ganados.away
                },
                'Empates': {
                    'Total': estadistica.empates.total,
                    'En Casa': estadistica.empates.home,
                    'Fuera': estadistica.empates.away
                },
                'Partidos Perdidos': {
                    'Total': estadistica.partidos_perdidos.total,
                    'En Casa': estadistica.partidos_perdidos.home,
                    'Fuera': estadistica.partidos_perdidos.away
                },
                'Goles Totales': {
                    'Total': estadistica.goles_totales.total,
                    'En Casa': estadistica.goles_totales.home,
                    'Fuera': estadistica.goles_totales.away
                }
            }
            resultados.append(datos_equipo)
        return resultados

    def obtener_partido_por_id(self, partidoid):
        print(f"Buscando partido con ID: {partidoid}")  # Mensaje de depuración
        partido = Partido.objects(partidoid=partidoid).first()
        
        if partido:
            print(f"Partido encontrado: {partido}")  # Mostrar el partido encontrado para depuración
            return {
                'equipos': {
                    'casa': {
                        'nombre': partido.equipos['casa']['nombre'],
                        'logo': partido.equipos['casa'].get('logo', '')  # Obtener logo del equipo casa
                    },
                    'afuera': {
                        'nombre': partido.equipos['afuera']['nombre'],
                        'logo': partido.equipos['afuera'].get('logo', '')  # Obtener logo del equipo visitante
                    }
                },
                'goles': {
                    'casa': partido.goles['casa'],
                    'afuera': partido.goles['afuera']
                }
            }
        else:
            print(f"No se encontró el partido con ID: {partidoid}")  # Mensaje si no se encuentra el partido
        return None
    