"""
Modulo que define la entidad Municipio.
"""
class Municipio:
    """
    Representa una entidad administrativa territorial que agrupa localidades
    Atributos:
        nombre (string): Nombre oficial del municipio
        localidades (list): Lista de objetos de tipo Localidad que pertenecen a este municipio
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        """
        Añade una nueva instancia de Localidad a la lista interna del municipio
        Variables:
            localidad (Localidad): Objeto de tipo Localidad que se desea vincular al municipio
        """
        self.localidades.append(localidad)
        