def calcular_estadisticas_consultas(historial):
    if not historial:
        print("No hay suficientes datos estadísticos")
        print("Realiza algunas consultas de clima actual primero")
        return

    suma_temp = 0
    suma_hum = 0
    suma_viento = 0
    total_consultas = len(historial)
    consulta_mas_calurosa = historial[0]
    consulta_mas_fresca = historial[0]

    for registro in historial:
        suma_temp += registro.temperatura
        suma_hum += registro.humedad
        suma_viento += registro.viento

        if registro.temperatura > consulta_mas_calurosa.temperatura:
            consulta_mas_calurosa = registro
        
        if registro.temperatura < consulta_mas_fresca.temperatura:
            consulta_mas_fresca = registro

    prom_temp = suma_temp / total_consultas
    prom_hum = suma_hum / total_consultas
    prom_viento = suma_viento / total_consultas

    print("ESTADISTICAS DE LA SESION ACTUAL ")
    print(f"Total de consultas realizadas: {total_consultas}")
    print(f"Temperatura promedio consultada: {prom_temp} °C")
    print(f"Humedad promedio consultada: {prom_hum} %")
    print(f"Velocidad del viento promedio: {prom_viento} km/h")
    
    print("RANKING DE LA SESION:")
    print(f"Lugar más caluroso: Municipio {consulta_mas_calurosa.municipio}, Localidad {consulta_mas_calurosa.localidad} ({consulta_mas_calurosa.temperatura} °C)")
    print(f"Lugar más fresco: Municipio {consulta_mas_fresca.municipio}, Localidad {consulta_mas_fresca.localidad} ({consulta_mas_fresca.temperatura} °C)")


def mostrar_localidades_sin_coordenadas(db_municipios):
    localidades_faltantes = []

    for municipio in db_municipios:
        for localidad in municipio.localidades:
            if not localidad.tiene_coordenadas():
                localidades_faltantes.append((municipio.nombre, localidad.nombre))

    print("REPORTE DE DATOS FALTANTES")
    if not localidades_faltantes:
        print("Todas las localidades tienen coordenadas válidas")
    else:
        print(f"Se encontraron {len(localidades_faltantes)} localidades sin coordenadas:\n")
        municipio_actual = ""
        for mun, loc in localidades_faltantes:
            if mun != municipio_actual:
                print(f"Municipio {mun}:")
                municipio_actual = mun
            print(f"   - {loc}")
            
def ejecutar_modulo_estadisticas(historial, db_municipios):
    calcular_estadisticas_consultas(historial)
    mostrar_localidades_sin_coordenadas(db_municipios)