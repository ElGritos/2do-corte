"""
Modulo que define la estructura para almacenar las respuestas de la api de clima en tiempo real
"""
class RegistroConsulta:
    """
    Representa un registro historico de una consulta de clima realizada por el usuario.
    Se utiliza para guardar y leer la informacion en el historial de la sesion.
    Atributos:
        municipio (string): Nombre del municipio consultado.
        localidad (string): Nombre de la localidad consultada.
        temperatura (float): Temperatura registrada durante la consulta (en °C).
        humedad (float): Porcentaje de humedad registrado.
        viento (float): Velocidad del viento.
        clima (string): Descripcion textual del estado del clima.
        fecha_hora (string): Fecha y hora exacta en la que se realizo la consulta.
    """
    def __init__(self, municipio, localidad, temperatura, humedad, viento, clima, fecha_hora):
        self.municipio = municipio
        self.localidad = localidad
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.clima = clima
        self.fecha_hora = fecha_hora

class RespuestaAPIActual:
    """
    Representa los datos meteorologicos actuales devueltos por la api
    Ayuda a manejar la informacion forma de objeto
    Atributos:
        temperatura (float): Temperatura actual en grados celsius.
        humedad (float): Humedad relativa actual en porcentaje.
        viento (float): Velocidad actual del viento en km/h.
        codigo_clima (int): Codigo numerico de la api que representa el estado del clima.
    """
    def __init__(self, temperatura, humedad, viento, codigo_clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima