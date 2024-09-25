import matplotlib.pyplot as plt
import matplotlib.image as mpimg # Carga una imagen desde un archivo
from matplotlib.offsetbox import OffsetImage, AnnotationBbox #Off... Toma la imagen cargada y la escala al tamaño deseado, Annotation.. la posiciona
import pymongo
import numpy as np

def graficar_comparacion_tiros_posesion(equipo1, equipo2, estadisticas1, estadisticas2):
    # Claves originales de las estadísticas
    estadisticas_claves = ["Tiros al arco", "Tiros desviados", "Total de tiros", "Posesión del balón"]

    # Etiquetas a mostrar en el gráfico
    etiquetas_grafico = ["Tiros al arco", "Tiros desviados", "Total de tiros", "Posesión del balón (%)"]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Función para convertir los valores de posesión si contienen '%'
    convertir_valor = lambda val: float(val.replace('%', '')) if isinstance(val, str) and '%' in val else float(val or 0)

    # Extraemos y convertimos los valores de las estadísticas para ambos equipos
    valores1 = [convertir_valor(estadisticas1.get(stat, 0)) for stat in estadisticas_claves] #Busca cada estadística en el diccionario de estadísticas. Si no esta, usa 0 como valor 
    valores2 = [convertir_valor(estadisticas2.get(stat, 0)) for stat in estadisticas_claves]

    # Creación de gráfico
    indices = np.arange(len(estadisticas_claves))
    ax.barh(indices - 0.2, valores1, color='blue', label=f'{equipo1} (Local)', height=0.4)
    ax.barh(indices + 0.2, valores2, color='green', label=f'{equipo2} (Visitante)', height=0.4)

    # Etiquetas para el gráfico
    ax.set_yticks(indices)
    ax.set_yticklabels(etiquetas_grafico)  # Cambiamos las etiquetas mostradas
    ax.invert_yaxis()
    ax.set_xlabel('Estadísticas')
    ax.set_title(f'Comparación Tiros y Posesión del partido: {equipo1} vs {equipo2}')
    ax.legend()
    plt.show()

# Función 2: Gráfico Circular para la Distribución de Pases
def graficar_distribucion_pases(estadisticas):
    # Nombres de las claves correctas basadas en tus datos
    labels = ['Pases Completados', 'Pases Fallidos']
    
    # Acceso seguro a las estadísticas
    pases_completados = estadisticas.get('Pases completados', 0)  
    total_pases = estadisticas.get('Pases totales', 0)
    pases_fallidos = total_pases - pases_completados
    
    sizes = [pases_completados, pases_fallidos]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
    ax.set_title('Distribución de Pases Partido Local')
    plt.show()

# Función 3: Gráfico Circular para la Distribución de Pases Equipo Visitante
def graficar_distribucion_pases_visitante(estadisticas):
    # Nombres de las claves correctas basadas en tus datos
    labels = ['Pases Completados', 'Pases Fallidos']
    
    # Acceso seguro a las estadísticas
    pases_completados = estadisticas.get('Pases completados', 1)
    total_pases = estadisticas.get('Pases totales', 1)
    pases_fallidos = total_pases - pases_completados
    
    sizes = [pases_completados, pases_fallidos]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
    ax.set_title('Distribución de Pases Partido Visitante')
    plt.show()

# Función 4: Gráfico de Dispersión para xG (Expected Goals) vs Goles Reales (Opción 7)
def graficar_xg_vs_goles(equipos, xg_values, goles_reales):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Graficar puntos
    ax.scatter(xg_values, goles_reales, color='blue', s=100)
    
    # Añadir nombres de los equipos
    for i, equipo in enumerate(equipos):
        ax.text(xg_values[i], goles_reales[i], equipo, fontsize=9, ha='right')
    
    # Configurar límites del eje x para hacerlos más largos
    x_margin = 0.1  # Margen adicional para los límites del eje x
    ax.set_xlim(min(xg_values) - x_margin, max(xg_values) + x_margin)

    # Etiquetas y título
    ax.set_xlabel('Expected Goals (xG)')
    ax.set_ylabel('Goles Reales')
    ax.set_title('xG vs Goles Reales por Equipo')
    plt.show()

# Función 5: Gráfico de Barras para Estadísticas Defensivas
def graficar_estadisticas_defensivas(equipos, faltas, intercepciones, tarjetas):
    fig, ax = plt.subplots(figsize=(10, 6))

    indices = np.arange(len(equipos))
    bar_width = 0.3

    ax.bar(indices, faltas, bar_width, label='Faltas', color='blue')
    ax.bar(indices + bar_width, intercepciones, bar_width, label='Intercepciones', color='green')
    ax.bar(indices + 2 * bar_width, tarjetas, bar_width, label='Tarjetas', color='red')

    ax.set_xlabel('Equipos')
    ax.set_ylabel('Estadísticas Defensivas')
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(equipos)
    ax.legend()
    ax.set_title('Comparación de Estadísticas Defensivas por Equipo')
    plt.show()

# Rutas de las camisetas PNG
home_jersey_path = "C:/Users/Daniela/Downloads/1031436.png"   # Cambia esto por la ruta real de la camiseta local
away_jersey_path = "C:/Users/Daniela/Downloads/1031435.png"

def plot_soccer_field(ax):
    # Crear el campo sobre el objeto 'ax'
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Dibujar las líneas del campo
    ax.set_facecolor('#4CAF50')  # Fondo verde para el campo

    # Dibujar los bordes del campo y la línea de medio campo
    lw = 2  # Line width
    ax.plot([50, 50], [0, 100], color="white", lw=lw)  # Línea media
    ax.plot([0, 100], [0, 0], color="white", lw=lw)
    ax.plot([0, 0], [0, 100], color="white", lw=lw)
    ax.plot([100, 100], [0, 100], color="white", lw=lw)
    ax.plot([0, 100], [100, 100], color="white", lw=lw)

    # Área de penalti equipo local
    ax.plot([0, 16], [70, 70], color="white", lw=lw)
    ax.plot([0, 16], [30, 30], color="white", lw=lw)
    ax.plot([16, 16], [30, 70], color="white", lw=lw)

    # Área de penalti equipo visitante
    ax.plot([100, 84], [70, 70], color="white", lw=lw)
    ax.plot([100, 84], [30, 30], color="white", lw=lw)
    ax.plot([84, 84], [30, 70], color="white", lw=lw)

    # Área chica equipo local
    ax.plot([0, 6], [60, 60], color="white", lw=lw)
    ax.plot([0, 6], [40, 40], color="white", lw=lw)
    ax.plot([6, 6], [40, 60], color="white", lw=lw)

    # Área chica equipo visitante
    ax.plot([100, 94], [60, 60], color="white", lw=lw)
    ax.plot([100, 94], [40, 40], color="white", lw=lw)
    ax.plot([94, 94], [40, 60], color="white", lw=lw)

    # Círculo central
    center_circle = plt.Circle((50, 50), 10, color="white", fill=False, lw=lw)
    ax.add_artist(center_circle)

    # Punto central
    ax.scatter(50, 50, color="white", s=20)

def plot_players(ax, lineup_data, formation, is_home_team):
    # Convertir la formación a una lista de números enteros
    formation_split = list(map(int, formation.split('-')))
    total_players = sum(formation_split) + 1  # +1 para el arquero

    # Ajustar posiciones base, local:izquierda, visitante:derecha
    if is_home_team:
        base_x = 10
        end_x = 40
    else:
        base_x = 90
        end_x = 60
    #Distribuir las lineas de jugadores equitativamente 
    step_x = (end_x - base_x) / (len(formation_split) + 1)  # Espacio entre líneas, calcula la distancia horizontal entre cada línea de jugadores en el campo
    current_x = base_x  # Ajuste de línea, marca la posición actual en el eje x donde se colocarán los jugadores

    player_positions = []

    # Posición del arquero
    y_pos_goalkeeper = 50
    if is_home_team:
        player_positions.append((5, y_pos_goalkeeper))
    else:
        player_positions.append((95, y_pos_goalkeeper))

    # Posicionar jugadores según la formación
    for i, line_players in enumerate(formation_split):
        current_x += step_x
        
        # Ajustar la posición inicial de los jugadores de una línea (más margen para más jugadores)
        y_start = 100 / (line_players + 1)
        y_step = 100 / (line_players + 1)  # Ajustar espaciado vertical entre jugadores

        for j in range(line_players):
            y_pos = (j + 1) * y_step # posicion vertical de cada linea 
            # Ajuste correcto para el equipo visitante
            if not is_home_team:
                y_pos = 100 - y_pos
            player_positions.append((current_x, y_pos))

    # Dibujar jugadores y sus nombres
    for i, pos in enumerate(player_positions):
        x, y = pos
        image = mpimg.imread(home_jersey_path if is_home_team else away_jersey_path) #camisetas
        imagebox = OffsetImage(image, zoom=0.08) #se utiliza para crear un objeto de imagen que puede ser insertado en un gráfico, ajusta el tamaño
        ab = AnnotationBbox(imagebox, (x, y), frameon=False) #se usa para anclar el objeto de imagen (imagebox) a una ubicación específica en el gráfico
        ax.add_artist(ab)

        # Añadir nombre del jugador si existe en los datos
        if i < len(lineup_data):
            nombre_jugador = lineup_data[i]['nombre']  # Obtener el nombre del jugador
            ax.text(x, y - 3, nombre_jugador, fontsize=8, color='white', ha='center', va='top')

def visualize_lineups(partidoid):
    # Conectar con MongoDB y obtener las alineaciones del partido
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['futbol']
    
    # Asegúrate de que partidoid es un entero
    partidoid = int(partidoid)
    
    # Buscar alineaciones para ambos equipos del partido
    alineaciones = list(db['lineups'].find({'partidoid': partidoid}))

    if not alineaciones or len(alineaciones) != 2:
        print(f"No se encontraron alineaciones completas para el partido ID: {partidoid}")
        return

    # Identificar cuál es la alineación local y cuál es la visitante
    equipo_local = alineaciones[0]  # Primer equipo como local
    equipo_visitante = alineaciones[1]  # Segundo equipo como visitante
    
    # Obtener las formaciones
    formacion_local = equipo_local['formacion']
    formacion_visitante = equipo_visitante['formacion']

    # Obtener las listas de titulares
    titulares_local = equipo_local['titulares']
    titulares_visitante = equipo_visitante['titulares']

    # Plotear el campo
    fig, ax = plt.subplots(figsize=(10, 7))
    plot_soccer_field(ax)

    # Plotear los jugadores de cada equipo
    plot_players(ax, titulares_local, formacion_local, is_home_team=True)
    plot_players(ax, titulares_visitante, formacion_visitante, is_home_team=False)

    # Añadir etiquetas de equipo
    ax.text(20, 105, 'Equipo Local', color='red', fontsize=14, weight='bold', ha='center')
    ax.text(80, 105, 'Equipo Visitante', color='blue', fontsize=14, weight='bold', ha='center')

    # Mostrar gráfico
    plt.show()


def graficar_estadisticas_equipo(estadistica):
    if not estadistica:
        print("No se encontraron estadísticas para el equipo.")
        return

    nombre_equipo = estadistica['Nombre']
    estadisticas = {
        'Partidos Jugados': estadistica['Partidos Jugados'],
        'Partidos Ganados': estadistica['Partidos Ganados'],
        'Empates': estadistica['Empates'],
        'Partidos Perdidos': estadistica['Partidos Perdidos'],
        'Goles Totales': estadistica['Goles Totales']
    }

    # Crear listas para los datos
    categorias = list(estadisticas.keys())
    valores_totales = [estadisticas[stat].get('Total', 0) for stat in categorias]
    valores_en_casa = [estadisticas[stat].get('En Casa', 0) for stat in categorias]
    valores_fuera = [estadisticas[stat].get('Fuera', 0) for stat in categorias]


    # Configurar la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    indice_barras = range(len(categorias))
    ancho_barra = 0.25

    # Graficar barras
    ax.bar([i - ancho_barra for i in indice_barras], valores_totales, ancho_barra, label='Total')
    ax.bar(indice_barras, valores_en_casa, ancho_barra, label='En Casa')
    ax.bar([i + ancho_barra for i in indice_barras], valores_fuera, ancho_barra, label='Fuera')

    # Configuración adicional de la gráfica
    ax.set_xlabel('Categorías')
    ax.set_ylabel('Cantidad')
    ax.set_title(f'Estadísticas del Equipo: {nombre_equipo}')
    ax.set_xticks(indice_barras)
    ax.set_xticklabels(categorias)
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()