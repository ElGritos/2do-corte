class Municipio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        self.localidades.append(localidad)