import requests

API_KEY = 'fbb59607-773a-4f02-947a-0b049b09224b'

CIUDADES = {
    'santiago': '-33.4489,-70.6693',
    'valparaiso': '-33.0472,-71.6127',
    'lima': '-12.0464,-77.0428',
    'arequipa': '-16.4090,-71.5375',
    'iquique': '-20.2307,-70.1357',
    'arica': '-18.4783,-70.3126',
    'tacna': '-18.0066,-70.2463',
    'cusco': '-13.5250,-71.9722'
}

def convertir_distancia(metros):
    km = metros / 1000
    millas = metros / 1609.34
    return round(km, 2), round(millas, 2)

def convertir_duracion(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    return f"{horas}h {minutos}min"

def obtener_ruta(origen, destino, transporte):
    try:
        url = "https://graphhopper.com/api/1/route"
        params = {
            "point": [origen, destino],
            "vehicle": transporte,
            "locale": "es",
            "instructions": "true",
            "calc_points": "true",
            "key": API_KEY
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        path = data["paths"][0]

        km, millas = convertir_distancia(path["distance"])
        duracion = convertir_duracion(path["time"] / 1000)

        print("\nResultados del viaje:")
        print(f"• Distancia: {km} km / {millas} millas")
        print(f"• Duración estimada: {duracion}")
        print("\n🗺️ Narrativa del viaje:")

        for paso in path["instructions"]:
            print(f"- {paso['text']} ({round(paso['distance'], 1)} m)")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error al conectar con el servicio de mapas: {str(e)}")
    except (KeyError, IndexError):
        print("\n⚠️ No se pudo calcular la ruta. Verifica los nombres de las ciudades.")

def mostrar_ciudades_disponibles():
    print("\nCiudades disponibles:")
    for ciudad in sorted(CIUDADES.keys()):
        print(f"- {ciudad.capitalize()}")

def menu():
    print("\nBienvenido al Calculador de Distancias Chile–Perú")
    mostrar_ciudades_disponibles()
    
    while True:
        ciudad_origen = input("\nCiudad de origen (o 's' para salir): ").lower()
        if ciudad_origen == 's':
            break

        if ciudad_origen not in CIUDADES:
            print("Ciudad no reconocida. Intenta con una de la lista.")
            mostrar_ciudades_disponibles()
            continue

        ciudad_destino = input("Ciudad de destino (o 's' para salir): ").lower()
        if ciudad_destino == 's':
            break

        if ciudad_destino not in CIUDADES:
            print("Ciudad no reconocida. Intenta con una de la lista.")
            mostrar_ciudades_disponibles()
            continue

        print("\nSeleccione el tipo de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. A pie")

        opcion = input("Opción (1/2/3): ")
        if opcion.lower() == 's':
            break

        transporte = {
            '1': 'car',
            '2': 'bike',
            '3': 'foot'
        }.get(opcion, 'car')

        print(f"\nCalculando ruta entre {ciudad_origen} y {ciudad_destino}...")
        obtener_ruta(CIUDADES[ciudad_origen], CIUDADES[ciudad_destino], transporte)

if __name__ == "__main__":
    menu()