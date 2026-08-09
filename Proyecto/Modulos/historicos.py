import requests

class RegistroHistoricoDiario:
    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento

class GrupoHistorico:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.registros = []

    def agregar_registro(self, registro_diario):
        self.registros.append(registro_diario)

    def prom_temp(self):
        if not self.registros: return 0.0
        suma = sum(r.temperatura for r in self.registros if r.temperatura is not None)
        return suma / len(self.registros)

    def prom_hum(self):
        if not self.registros: return 0.0
        suma = sum(r.humedad for r in self.registros if r.humedad is not None)
        return suma / len(self.registros)

    def suma_prec(self):
        if not self.registros: return 0.0
        return sum(r.precipitacion for r in self.registros if r.precipitacion is not None)

    def prom_viento(self):
        if not self.registros: return 0.0
        suma = sum(r.viento for r in self.registros if r.viento is not None)
        return suma / len(self.registros)

def consultar_api_historica(localidad_obj, fecha_inicio, fecha_fin):
    print(f"Consultando históricos para {localidad_obj.nombre}")
    
    url = (f"https://archive-api.open-meteo.com/v1/archive?"
           f"latitude={localidad_obj.latitud}&longitude={localidad_obj.longitud}&"
           f"start_date={fecha_inicio}&end_date={fecha_fin}&"
           f"daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max&"
           f"timezone=America%2FCaracas")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
        
        lista_diaria = []
        tiempos = datos["daily"]["time"]
        temps = datos["daily"]["temperature_2m_mean"]
        hums = datos["daily"]["relative_humidity_2m_mean"]
        precs = datos["daily"]["precipitation_sum"]
        vientos = datos["daily"]["wind_speed_10m_max"]
        
        for i in range(len(tiempos)):
            registro = RegistroHistoricoDiario(
                fecha=tiempos[i],
                temperatura=temps[i],
                humedad=hums[i],
                precipitacion=precs[i],
                viento=vientos[i])
            lista_diaria.append(registro)
            
        print("Datos historicos obtenidos con exito")
        return lista_diaria
        
    except Exception as e:
        print(f"Error al consultar la API Histórica: {e}")
        return []