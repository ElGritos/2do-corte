import requests
from datetime import datetime
from Objetos.consulta import RegistroConsulta

class RespuestaAPIActual:
    def __init__(self, temperatura, humedad, viento, codigo_clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima

def buscar_localidad(db_municipios):
    print("SELECCION DE UBICACIÓN")
    print("Municipios disponibles:")

    for i, mun in enumerate(db_municipios):
        print(f"  {i + 1}. {mun.nombre}")
    
    try:
        opcion_mun = int(input("Seleccione el número del municipio: ")) - 1
        if 0 <= opcion_mun < len(db_municipios):
            municipio_seleccionado = db_municipios[opcion_mun]
            print(f"Localidades en el municipio {municipio_seleccionado.nombre}:")
            for j, loc in enumerate(municipio_seleccionado.localidades):
                print(f"  {j + 1}. {loc.nombre}")   
            opcion_loc = int(input("Seleccione el número de la localidad: ")) - 1
            if 0 <= opcion_loc < len(municipio_seleccionado.localidades):
                localidad_seleccionada = municipio_seleccionado.localidades[opcion_loc]
                return municipio_seleccionado, localidad_seleccionada
            else:
                print("Opción de localidad inválida.")
                return None, None
        else:
            print("Opción de municipio inválida.")
            return None, None
    except ValueError:
        print("Error: Por favor, ingrese un numero valido.")
        return None, None

def buscar_localidad_por_nombre(db_municipios):
    print("BÚSQUEDA DIRECTA POR NOMBRE")
    termino = input("ingrese el nombre (o parte de el) de la localidad: ").strip().lower()
    resultados = []

    if not termino:
        print("El término de busqueda no puede estar vacio")
        return None, None
    for municipio in db_municipios:
        for localidad in municipio.localidades:
            if termino in localidad.nombre.lower():
                if localidad.tiene_coordenadas():
                    resultados.append((municipio, localidad))  

    if not resultados:
        print(f"No se encontraron localidades con coordenadas válidas que coincidan con '{termino}'.")
        return None, None
    print(f"Se encontraron {len(resultados)} coincidencias:")
    for i, (mun, loc) in enumerate(resultados):
        print(f"{i + 1}. {loc.nombre} (Municipio: {mun.nombre})")
        
    while True:
        seleccion = input("Seleccione el número de la localidad deseada (0 para cancelar): ")
        if seleccion == '0':
            print("Busqueda cancelada")
            return None, None
        if seleccion.isdigit():
            indice = int(seleccion) - 1
            if 0 <= indice < len(resultados):
                return resultados[indice] 
            else:
                print("Opción fuera de rango. Intente nuevamente")
        else:
            print("Ingrese un número válido")

def interpretar_codigo_clima(codigo):
    if codigo == 0: return "Cielo despejado"
    elif codigo == 1: return "Mayormente despejado"
    elif codigo == 2: return "Parcialmente nublado"
    elif codigo == 3: return "Nublado"
    elif codigo == 45: return "Niebla"
    elif codigo == 51: return "Llovizna ligera"
    elif codigo == 61: return "Lluvia leve"
    elif codigo == 63: return "Lluvia moderada"
    elif codigo == 65: return "Lluvia fuerte"
    elif codigo == 80: return "Chubascos leves"
    elif codigo == 95: return "Tormenta eléctrica"
    else: return f"Código {codigo} (Desconocido)"

def consultar_api_meteo(localidad_obj): 
    if not localidad_obj.tiene_coordenadas():
        print("Esta localidad no tiene coordenadas válidas para consultar el clima")
        return None
    print(f"Consultando clima para {localidad_obj.nombre}")
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={localidad_obj.latitud}&longitude={localidad_obj.longitud}&"
           f"current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&"
           f"timezone=America%2FCaracas")
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        datos = response.json()
        clima_actual = datos["current"]
        resultado_obj = RespuestaAPIActual(
            temperatura=clima_actual["temperature_2m"],
            humedad=clima_actual["relative_humidity_2m"],
            viento=clima_actual["wind_speed_10m"],
            codigo_clima=clima_actual["weather_code"])
        print('Información meteorológica actualizada exitosamente')
        return resultado_obj
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Open-Meteo: {e}")
        return None

def ejecutar_modulo_clima_actual(db_municipios, historial, modo="lista"):
    if modo == "lista":
        mun_obj, loc_obj = buscar_localidad(db_municipios)
    elif modo == "directa":
        mun_obj, loc_obj = buscar_localidad_por_nombre(db_municipios)
    else:
        return

    if loc_obj:
        datos_clima_obj = consultar_api_meteo(loc_obj)
        if datos_clima_obj:
            descripcion_clima = interpretar_codigo_clima(datos_clima_obj.codigo_clima)
            print(f"Reporte Actual: {loc_obj.nombre.upper()} ")
            print(f"Temperatura: {datos_clima_obj.temperatura} °C")
            print(f"Humedad:     {datos_clima_obj.humedad} %")
            print(f"Viento:      {datos_clima_obj.viento} km/h")
            print(f"Condición:   {descripcion_clima}")
            nuevo_registro = RegistroConsulta(
                municipio=mun_obj.nombre,
                localidad=loc_obj.nombre,
                temperatura=datos_clima_obj.temperatura,
                humedad=datos_clima_obj.humedad,
                viento=datos_clima_obj.viento,
                clima=descripcion_clima,
                fecha_hora=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            historial.append(nuevo_registro)
            print("Consulta guardada en el historial de la sesión para las estadísticas")