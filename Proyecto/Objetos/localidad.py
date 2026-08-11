class Localidad:
    """
    Representa un punto geográfico especifico, sector o parroquia dentro de un municipio.
    Atributos:
        nombre (string): Nombre de la localidad
        latitud (float o None): Coordenada de latitud (Puede ser None si falta en la base de datos)
        longitud (float o None): Coordenada de longitud (Puede ser None si falta en la base de datos)
    """
    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """
        Verifica si la localidad posee coordenadas geograficas validas asignadas.
        Retorna:
            variable booleana: Verdadero la latitud y la longitud tienen un valor diferente de None, Falso en caso contrario.
        """
        return self.latitud is not None and self.longitud is not None