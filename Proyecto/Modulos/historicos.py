def buscar_o_crear_grupo(lista_grupos, etiqueta):
    for grupo in lista_grupos:
        if grupo.etiqueta == etiqueta:
            return grupo
            
    nuevo_grupo = GrupoHistorico(etiqueta)
    lista_grupos.append(nuevo_grupo)
    return nuevo_grupo

def procesar_y_mostrar_historico(lista_diaria):
    lista_meses = []
    lista_anos = []
    
    for registro in lista_diaria:
        mes_str = registro.fecha[:7] 
        ano_str = registro.fecha[:4]
        
        grupo_mes = buscar_o_crear_grupo(lista_meses, mes_str)
        grupo_mes.agregar_registro(registro)
        
        grupo_ano = buscar_o_crear_grupo(lista_anos, ano_str)
        grupo_ano.agregar_registro(registro)
        
    print("RESUMEN MENSUAL DEL PERÍODO ")    
    for mes in lista_meses:
        print(f"Mes: {mes.etiqueta}")
        print(f"Temp promedio: {mes.prom_temp()} °C")
        print(f"Humedad promedio: {mes.prom_hum()} %")
        print(f"Precipitación total: {mes.suma_prec()} mm")
        print(f"Viento promedio: {mes.prom_viento()} km/h")

    if not lista_anos:
        return lista_anos, lista_meses

    ano_mas_caluroso = lista_anos[0]
    ano_mas_fresco = lista_anos[0]
    ano_mas_lluvioso = lista_anos[0]
    ano_mas_humedo = lista_anos[0]

    for ano in lista_anos:
        if ano.prom_temp() > ano_mas_caluroso.prom_temp(): ano_mas_caluroso = ano
        if ano.prom_temp() < ano_mas_fresco.prom_temp(): ano_mas_fresco = ano
        if ano.suma_prec() > ano_mas_lluvioso.suma_prec(): ano_mas_lluvioso = ano
        if ano.prom_hum() > ano_mas_humedo.prom_hum(): ano_mas_humedo = ano

    print("RECORDS ANUALES DEL PERIODO ")
    print(f"Año más caluroso: {ano_mas_caluroso.etiqueta} ({ano_mas_caluroso.prom_temp()} °C)")
    print(f"Año más fresco: {ano_mas_fresco.etiqueta} ({ano_mas_fresco.prom_temp()} °C)")
    print(f"Año con mayor precipitación: {ano_mas_lluvioso.etiqueta} ({ano_mas_lluvioso.suma_prec()} mm)")
    print(f"Año con mayor humedad: {ano_mas_humedo.etiqueta} ({ano_mas_humedo.prom_hum()} %)")

    return lista_anos, lista_meses

def graficar_evolucion(lista_anos, lista_meses):
    if not lista_anos:
        print("No hay datos para graficar.")
        return

    if len(lista_anos) == 1:
        lista_a_graficar = lista_meses
        tipo_grafico = "Mensual"
    else:
        lista_a_graficar = lista_anos
        tipo_grafico = "Anual"

    etiquetas = []
    prom_temps = []
    prom_hums = []
    total_precs = []
    prom_vientos = []

    for grupo in lista_a_graficar:
        etiquetas.append(grupo.etiqueta)
        prom_temps.append(grupo.prom_temp())
        prom_hums.append(grupo.prom_hum())
        total_precs.append(grupo.suma_prec())
        prom_vientos.append(grupo.prom_viento())

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Evolución {tipo_grafico} de Variables Meteorológicas', fontsize=16)

    axs[0, 0].plot(etiquetas, prom_temps, marker='o', color='tab:red', linewidth=2)
    axs[0, 0].set_title('Temperatura Promedio (°C)')
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)

    axs[0, 1].plot(etiquetas, prom_hums, marker='s', color='tab:blue', linewidth=2)
    axs[0, 1].set_title('Humedad Relativa Promedio (%)')
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)

    axs[1, 0].plot(etiquetas, total_precs, marker='^', color='tab:green', linewidth=2)
    axs[1, 0].set_title('Precipitación Acumulada (mm)')
    axs[1, 0].grid(True, linestyle='--', alpha=0.7)

    axs[1, 1].plot(etiquetas, prom_vientos, marker='D', color='tab:orange', linewidth=2)
    axs[1, 1].set_title('Velocidad del Viento Promedio (km/h)')
    axs[1, 1].grid(True, linestyle='--', alpha=0.7)

    if len(lista_anos) == 1:
        for ax in axs.flat:
            ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def ejecutar_modulo_historicos(localidad_obj):
    if not localidad_obj.tiene_coordenadas():
        print("Error: Esta localidad no posee coordenadas válidas.")
        return

    print("CONFIGURACIÓN DE BÚSQUEDA HISTORICA")
    print("Formato de fecha requerido: AAAA-MM-DD (Ej: 2021-01-01)")
    fecha_inicio = input("Ingrese la fecha de INICIO: ")
    fecha_fin = input("Ingrese la fecha de FIN: ")

    lista_diaria = consultar_api_historica(localidad_obj, fecha_inicio, fecha_fin)

    if lista_diaria:
        lista_anos, lista_meses = procesar_y_mostrar_historico(lista_diaria)
        
        print("Generando gráfica comparativa (Cierre la ventana del gráfico para continuar)")
        graficar_evolucion(lista_anos, lista_meses)