import requests
import time

API_KEY = 'fbb59607-773a-4f02-947a-0b049b09224b'

def geocodificar(ciudad):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": ciudad,
        "format": "json",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, headers={'User-Agent': 'GeoApp'})
        if response.status_code == 200 and response.json():
            datos = response.json()[0]
            return f"{datos['lat']},{datos['lon']}"
        else:
            print(f"❌ No se pudo geocodificar '{ciudad}'.")
            return None
    except Exception as e:
        print(f"❌ Error durante geocodificación: {e}")
        return None

def convertir_distancia(metros):
    km = metros / 1000
    millas = metros / 1609.34
    return round(km, 2), round(millas, 2)

def convertir_duracion(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    return f"{horas}h {minutos}min"

def obtener_ruta(origen_coord, destino_coord, transporte):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [origen_coord, destino_coord],
        "vehicle": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        path = data["paths"][0]

        km, millas = convertir_distancia(path["distance"])
        duracion = convertir_duracion(path["time"] / 1000)

        print("\n📍 Resultados del viaje:")
        print(f"• Distancia: {km} km / {millas} millas")
        print(f"• Duración estimada: {duracion}")
        print("\n🗺️ Narrativa del viaje:")
        for paso in path["instructions"]:
            print(f"- {paso['text']} ({round(paso['distance'], 1)} m)")

    else:
        print(f"\n❌ Error al obtener la ruta.")
        print(f"→ Código HTTP: {response.status_code}")
        try:
            print(f"→ Mensaje: {response.json().get('message', 'Sin mensaje detallado')}")
        except Exception:
            print("→ No se pudo interpretar el mensaje de error.")

def menu():
    print("🧭 Bienvenido al Calculador de Distancias Chile–Perú")

    while True:
        ciudad_origen = input("\nCiudad de origen (o 's' para salir): ")
        if ciudad_origen.lower() == 's':
            break

        ciudad_destino = input("Ciudad de destino (o 's' para salir): ")
        if ciudad_destino.lower() == 's':
            break

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

        print(f"\n🛰️ Buscando coordenadas...")
        origen_coord = geocodificar(ciudad_origen)
        destino_coord = geocodificar(ciudad_destino)

        if origen_coord and destino_coord:
            print(f"\n🧭 Calculando ruta entre {ciudad_origen} y {ciudad_destino}...\n")
            time.sleep(1)  # Para evitar bloqueos por uso de API
            obtener_ruta(origen_coord, destino_coord, transporte)
        else:
            print("⚠️ No se pudo continuar por error de geocodificación.")

if __name__ == "__main__":
    menu()
