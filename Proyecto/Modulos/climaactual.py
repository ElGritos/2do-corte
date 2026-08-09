import requests

class RespuestaAPIActual:
    def __init__(self, temperatura, humedad, viento, codigo_clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima

def consultar_api_meteo(localidad_obj): 
    """ 
    Consulta a la API de Open-Meteo en tiempo real.
    Convierte la respuesta directamente en un objeto RespuestaAPIActual.
    """
    if not localidad_obj.tiene_coordenadas():
        print("Esta localidad no tiene coordenadas válidas para consultar el clima")
        return None

    print(f"Consultando clima para {localidad_obj.nombre}")
    
    # Armado de URL como texto para evitar usar diccionarios en parámetros
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={localidad_obj.latitud}&longitude={localidad_obj.longitud}&"
           f"current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&"
           f"timezone=America%2FCaracas")
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        datos = response.json()
        
        clima_actual = datos["current"]
        
        # Guardamos en un objeto, no en diccionario
        resultado_obj = RespuestaAPIActual(
            temperatura=clima_actual["temperature_2m"],
            humedad=clima_actual["relative_humidity_2m"],
            viento=clima_actual["wind_speed_10m"],
            codigo_clima=clima_actual["weather_code"]
        )
        
        print('Información meteorológica actualizada exitosamente')
        return resultado_obj
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con Open-Meteo: {e}")
        return None