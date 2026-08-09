import json
import os 
from Objetos.consulta import *
from Objetos.municipio import *
from Objetos.localidad import *

DIRECTORIO = './Basededatos/'

def asegurar_directorio():
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
    asegurar_directorio()
    ruta_historial = os.path.join(DIRECTORIO, 'historial_consultas.json')
    try:
        with open(ruta_historial, 'w', encoding='utf-8') as file:
            file.write("[\n")
            
            for i, registro in enumerate(historial_consultas):
                linea = (
                    f'    {{'
                    f'        "municipio": "{registro.municipio}",'
                    f'        "localidad": "{registro.localidad}",'
                    f'        "temperatura": {registro.temperatura},'
                    f'        "humedad": {registro.humedad},'
                    f'        "viento": {registro.viento},'
                    f'        "clima": "{registro.clima}",'
                    f'        "fecha_hora": "{registro.fecha_hora}"'
                    f'    }}'
                )
                
                if i < len(historial_consultas) - 1:
                    linea += ","
                linea += "\n"
                file.write(linea)
                
            file.write("]\n")
            
        print("Historial guardado")
    except Exception as e:
        print(f"Error al intentar guardar el historial: {e}")
