"""
Modulo para el manejo de información y persistencia de datos, se encarga de verificar la existencia 
de los directorios necesarios, leer los archivos json locales y transformar dichos datos en
listas de objetos guardandolos en el historial
"""

import json
import os 
from Objetos.consulta import *
from Objetos.municipio import *
from Objetos.localidad import *

DIRECTORIO = './Proyecto/Basededatos/'

def asegurar_directorio():
    """
    Verifica la existencia del directorio base para la base de datos y lo crea si no existe.
    Esta funcion garantiza que las operaciones de lectura y escritura de archivos no fallen por falta de la carpeta de destino. Retorna:None
    """
    if not os.path.exists(DIRECTORIO):
        os.makedirs(DIRECTORIO)

def read_files():
    """
    Lee los archivos de la base de datos, y transforma los datos en objetos (los archivos zonas_caracas.json y historial_consultas.json).
    Incluye manejo de excepciones para evitar el cierre abrupto del programa si los archivos no existen.
    Retorna:db_municipios y db_historial (Lista de objetos con la informacion obtenida de la funcion).
    """
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
        print("No se encontro zonas_caracas.json en la carpeta Basededatos")

    try:
        if os.path.exists(ruta_historial):
            with open(ruta_historial, 'r') as file:
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
        db_historial = []

    return db_municipios, db_historial

def guardar_historial(historial_consultas):
    """
    Guarda la lista de objetos de consultas recientes en un archivo (historial_consultas.json)
    Extrae los atributos de cada objeto RegistroConsulta en la lista recibida y escribe en el archivo historial_consultas.json. 
    Tiene manejo de errores para advertir al usuario en caso de fallos de escritura.
    Parametros: historial_consultas (Lista de objetos)
    Retorna: None
    """
    asegurar_directorio()
    ruta_historial = os.path.join(DIRECTORIO, 'historial_consultas.json')
    try:
        with open(ruta_historial, 'w', encoding='utf-8') as file:
            file.write("[\n")
            for i, registro in enumerate(historial_consultas):
                linea = f"""    {{
                        "municipio": "{registro.municipio}",
                        "localidad": "{registro.localidad}",
                        "temperatura": {registro.temperatura},
                        "humedad": {registro.humedad},
                        "viento": {registro.viento},
                        "clima": "{registro.clima}",
                        "fecha_hora": "{registro.fecha_hora}"
                        }}"""
                if i < len(historial_consultas) - 1:
                    linea += ","
                linea += "\n"
                file.write(linea)
            file.write("]\n")
        print("Historial guardado")
    except Exception as e:
        print(f"Error al intentar guardar el historial: {e}")

