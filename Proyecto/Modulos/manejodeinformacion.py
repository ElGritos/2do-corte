import json
import os 
from Objetos.consulta import RegistroConsulta
from Objetos.municipio import Municipio
from Objetos.localidad import Localidad

DIRECTORIO = './Basededatos/'

def asegurar_directorio():
    """ 
    Verifica que la carpeta de la base de datos exista. 
    Si no existe, la crea automáticamente.
    """
    if not os.path.exists(DIRECTORIO):
        os.makedirs(DIRECTORIO)

def read_files(): 
    asegurar_directorio()
    ruta_zonas = os.path.join(DIRECTORIO, 'zonas_caracas.json')
    ruta_historial = os.path.join(DIRECTORIO, 'historial_consultas.json')
    
    db_municipios = []
    db_historial = []

    try:
        with open(ruta_zonas, 'r', encoding='utf-8') as file:
            datos_zonas = json.load(file)
            
            for nombre_municipio, lista_localidades in datos_zonas.items():
                nuevo_municipio = Municipio(nombre_municipio)
                
                for loc in lista_localidades:
                    nueva_localidad = Localidad(
                        nombre=loc.get("localidad"), 
                        latitud=loc.get("latitud"), 
                        longitud=loc.get("longitud")
                    )
                    nuevo_municipio.agregar_localidad(nueva_localidad)
                
                db_municipios.append(nuevo_municipio)
                
    except FileNotFoundError:
        print("Error crítico: No se encontró 'zonas_caracas.json' en la carpeta Basededatos.")
        print("Por favor, asegúrate de colocar el archivo entregado por el profesor allí.")

    try:
        if os.path.exists(ruta_historial):
            with open(ruta_historial, 'r', encoding='utf-8') as file:
                datos_historial = json.load(file)
                
                for reg in datos_historial:
                    consulta = RegistroConsulta(
                        municipio=reg.get("municipio"),
                        localidad=reg.get("localidad"),
                        temperatura=reg.get("temperatura"),
                        humedad=reg.get("humedad"),
                        viento=reg.get("viento"),
                        clima=reg.get("clima"),
                        fecha_hora=reg.get("fecha_hora")
                    )
                    db_historial.append(consulta)
    except Exception as e:
        print(f"Hubo un problema leyendo el historial previo: {e}")

    return db_municipios, db_historial