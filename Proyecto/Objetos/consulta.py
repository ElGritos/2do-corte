class RegistroConsulta:
    def __init__(self, municipio, localidad, temperatura, humedad, viento, clima, fecha_hora):
        self.municipio = municipio
        self.localidad = localidad
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.clima = clima
        self.fecha_hora = fecha_hora

class RespuestaAPIActual:
    def __init__(self, temperatura, humedad, viento, codigo_clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima