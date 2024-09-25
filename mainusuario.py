from ControladorUsuario import ControladorUsuario
from visualizaciones import (
    visualize_lineups,
    graficar_comparacion_tiros_posesion,
    graficar_distribucion_pases,
    graficar_xg_vs_goles,
    graficar_estadisticas_defensivas,
    graficar_distribucion_pases_visitante,
    graficar_estadisticas_equipo
    )
from datetime import datetime
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)  # Inicializa colorama para resetear los estilos automáticamente

def menu_principal():
    controller = ControladorUsuario()
    while True:
        print(Fore.GREEN + Style.BRIGHT + "\n⚽ -- Menú Principal de Gestión Deportiva -- ⚽")
        print(Fore.YELLOW + "1. 🏟 Ver todos los partidos")
        print(Fore.YELLOW + "2. 📊 Ver estadísticas de un partido")
        print(Fore.YELLOW + "3. 📋 Ver alineaciones de un partido")
        print(Fore.YELLOW + "4. 🏆 Ver todos los equipos")
        print(Fore.YELLOW + "5. 📈 Ver estadísticas de un equipo")
        print(Fore.YELLOW + "6. 🎨 Mostrar visualizaciones de un partido")
        print(Fore.RED + "7. 🚪 Salir")

        opcion = input(Fore.CYAN + "Seleccione una opción: ")

        if opcion == '1':
            mostrar_partidos(controller)
        elif opcion == '2':
            id_partido = obtener_id_valido_partido("partido")
            if id_partido:
                mostrar_estadisticas(controller, id_partido)
        elif opcion == '3':
            id_partido = obtener_id_valido_partido("partido")
            if id_partido:
                mostrar_alineaciones(controller, id_partido)
        elif opcion == '4':
            mostrar_equipos(controller)
        elif opcion == '5':
            id_equipo = obtener_id_valido_equipo("equipo")
            if id_equipo:
                mostrar_estadisticas_equipo(controller, id_equipo)
        elif opcion == '6':
            id_partido = obtener_id_valido_partido("partido")
            if id_partido:
                mostrar_visualizaciones(controller, id_partido)
        elif opcion == '7':
            print(Fore.RED + "Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opción no válida, intente nuevamente.")


def obtener_id_valido_partido(tipo):
    while True:
        id_input = input(f"Ingrese el ID del {tipo}: ")
        if id_input.isdigit() and len(id_input) == 7:
            return id_input
        print(f"Error: El ID del {tipo} debe ser un número entero y de 7 digitos. Intente nuevamente.")

def obtener_id_valido_equipo(tipo):
    while True:
        id_input = input(f"Ingrese el ID del {tipo}: ")
        if id_input.isdigit() and len(id_input) == 3:
            return id_input
        print(f"Error: El ID del {tipo} debe ser un número entero y de 3 digitos. Intente nuevamente.")

# Submenu
def mostrar_texto_submenu():
    print(Fore.GREEN + Style.BRIGHT + "\n⚽ -- Submenú de Visualización de Partidos -- ⚽")
    print(Fore.YELLOW + "1. 📏 Comparar tiros y posesión")
    print(Fore.YELLOW + "2. 🔄 Distribución de pases")
    print(Fore.YELLOW + "3. 🎯 xG vs Goles reales")
    print(Fore.YELLOW + "4. 🛡 Estadísticas defensivas")
    print(Fore.YELLOW + "5. 👕 Visualizar alineaciones")
    print(Fore.RED + "6. 🚪 Salir")

def ejecutar_submenu(partidoid, equipo1, equipo2, stats1, stats2, xg_values, goles_casa, goles_visita, faltas, intercepciones, tarjetas):
    while True:
        mostrar_texto_submenu()
        try:
            opcion = int(input(Fore.CYAN + "Elige una opción (1-6): "))
            if opcion == 1:
                graficar_comparacion_tiros_posesion(equipo1, equipo2, stats1, stats2)
            elif opcion == 2:
                graficar_distribucion_pases(stats1)
                graficar_distribucion_pases_visitante(stats2)
            elif opcion == 3:
                graficar_xg_vs_goles([equipo1, equipo2], xg_values, [goles_casa, goles_visita])
            elif opcion == 4:
                graficar_estadisticas_defensivas([equipo1, equipo2], faltas, intercepciones, tarjetas)
            elif opcion == 5:
                visualize_lineups(partidoid)
            elif opcion == 6:
                print(Fore.RED + "Saliendo del menú.")
                break
            else:
                print(Fore.RED + "Por favor, elige una opción válida.")
        except ValueError:
            print(Fore.RED + "Entrada no válida. Intente de nuevo.")



def mostrar_visualizaciones(controller, partidoid):
    
    # Obtiene los datos necesarios para las visualizaciones
    partido = controller.obtener_partido_por_id(partidoid) 
    estadisticas = controller.obtener_stats(partidoid)
    alineaciones = controller.obtener_lineups(partidoid)
    
    if not partido or not estadisticas or len(estadisticas) < 2 or not alineaciones:
        print(f"No se encontraron suficientes datos para el partido con ID {partidoid}.")
        return

    # Nombres de los equipos
    equipo1 = partido['equipos']['casa']['nombre']
    equipo2 = partido['equipos']['afuera']['nombre']
    
    # Estadísticas
    stats1 = estadisticas[0]
    stats2 = estadisticas[1]

     # Obtener los goles desde la estructura 'goles'
    goles_casa = int(partido['goles']['casa'])
    goles_visita = int(partido['goles']['afuera'])
    
    # Extraer los valores de expected_goals
    xg_values = []
    for i in range(2):
        # Verificar si 'Goles esperados' está en las estadísticas y convertirlo a float
        xg_str = estadisticas[i].get('Goles esperados', '0')
        print(f"Goles Esperados (raw) equipo {i + 1}: {xg_str}")
        try:
            # Convertir el valor a flotante si es posible
            xg_value = float(xg_str)
        except ValueError:
            # Manejar errores de conversión
            print(f"Error al convertir Goles esperados: {xg_str}")
            xg_value = 0.0
        xg_values.append(xg_value)
         # Gráfico de barras para estadísticas defensivas
    faltas = [stats1.get('Faltas', 0), stats2.get('Faltas', 0)]
    intercepciones = [stats1.get('Interceptions', 0), stats2.get('Interceptions', 0)]
    
    # Asegurarnos de que si hay un valor None, lo tratamos como 0
    tarjetas_amarillas_1 = stats1.get('Tarjetas amarillas', 0) or 0
    tarjetas_rojas_1 = stats1.get('Tarjetas rojas', 0) or 0
    tarjetas_amarillas_2 = stats2.get('Tarjetas amarillas', 0) or 0
    tarjetas_rojas_2 = stats2.get('Tarjetas rojas', 0) or 0
    
    tarjetas = [
        tarjetas_amarillas_1 + tarjetas_rojas_1,
        tarjetas_amarillas_2 + tarjetas_rojas_2
    ]

    ejecutar_submenu(partidoid,equipo1, equipo2, stats1, stats2,xg_values,goles_casa,goles_visita,faltas, intercepciones, tarjetas)
    
def mostrar_partidos(controller):
    # Get filter inputs from user
    equipo_filtro = input("Ingrese el nombre del equipo para filtrar (o presione Enter para ver todos): ").strip().title()
    fecha_filtro = input("Ingrese la fecha desde la cual mostrar partidos (dd/mm/yy) (o presione Enter para ver todos): ").strip()

    # Validate date input
    fecha_desde = None
    if fecha_filtro:
        try:
            fecha_desde = datetime.strptime(fecha_filtro, "%d/%m/%y")
        except ValueError:
            print("Formato de fecha inválido. Se mostrarán todos los partidos.")

    partidos = controller.obtener_partidos()
    if not partidos:
        print("No se encontraron partidos.")
        return

    print("\n-- Lista de Partidos --")
    partidos_filtrados = []
    for partido in partidos:
        # Apply team filter
        if equipo_filtro and equipo_filtro.title() not in partido['Equipo Casa'].title() and equipo_filtro.title() not in partido['Equipo Visitante'].title():
            continue

        # Apply date filter
        if fecha_desde:
            fecha_partido = datetime.strptime(partido['Fecha'], "%d/%m/%y")
            if fecha_partido < fecha_desde:
                continue

        partidos_filtrados.append(partido)

    if not partidos_filtrados:
        print("No se encontraron partidos que cumplan con los filtros especificados.")
        return

    for partido in partidos_filtrados:
        print(f"ID partido: {partido['ID partido']}  Fecha: {partido['Fecha']}  "
              f"Equipo Casa: {partido['Equipo Casa']}  Goles Casa: {partido['Goles Casa']}  "
              f"Equipo Visitante: {partido['Equipo Visitante']}  Goles Visitante: {partido['Goles Visitante']}")

def mostrar_estadisticas(controller, id_partido):
    estadisticas = controller.obtener_stats(id_partido)
    if not estadisticas:
        print(f"No se encontraron estadísticas para el partido con ID {id_partido}.")
        return
    print("\n-- Estadísticas del Partido --")
    for stats in estadisticas:
        for key, value in stats.items():
            if key != 'ID del Partido':
                print(f"{key}: {value}")
        print("\n" + "-" * 60 + "\n")

def mostrar_alineaciones(controller, id_partido):
    alineaciones = controller.obtener_lineups(id_partido)
    if not alineaciones:
        print(f"No se encontraron alineaciones para el partido con ID {id_partido}.")
        return
    print("\n-- Alineaciones del Partido --")
    for lineup in alineaciones:
        print(f"Partido ID: {lineup['Partido ID']}, Equipo: {lineup['Equipo']}, Formación: {lineup['Formacion']}")
        print("Jugadores:")
        for jugador in lineup['Jugadores']:
            print(f"  - Nombre: {jugador['Nombre']}, Número: {jugador['Numero']}, "
                  f"Posición: {jugador['Posicion']}, Posición en gráfico: {jugador['Posición en gráfico']}")
        print("\n")

def mostrar_equipos(controller):
    equipos = controller.obtener_equipos()
    if not equipos:
        print("No se encontraron equipos.")
        return
    print("\n-- Lista de Equipos --")
    for equipo in equipos:
        print(f"ID del Equipo: {equipo['ID del Equipo']}")
        print(f"Nombre: {equipo['Nombre']}")
        print(f"Logo: {equipo['Logo']}")
        print("\n" + "-" * 60 + "\n")

def mostrar_estadisticas_equipo(controller, id_equipo):
    estadisticas_equipo = controller.obtener_estadisticas_equipo(id_equipo)
    if not estadisticas_equipo:
        print(f"No se encontraron estadísticas para el equipo con ID {id_equipo}.")
        return
    print("\n-- Estadísticas del Equipo --")
    for estadistica in estadisticas_equipo:
        print(f"ID del Equipo: {estadistica['ID del Equipo']}")
        print(f"Nombre: {estadistica['Nombre']}")
        for key, value in estadistica.items():
            if key not in ['ID del Equipo', 'Nombre']:
                print(f"{key} - Total: {value['Total']}, En Casa: {value['En Casa']}, Fuera: {value['Fuera']}")
        print("\n" + "-" * 60 + "\n")
    graficar_estadisticas_equipo(estadisticas_equipo[0])
if __name__ == "__main__":
    menu_principal()











