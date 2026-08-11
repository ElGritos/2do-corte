"""
Modulo para la consulta y visualización de datos
Este modulo se conecta a la api para obtener datos historicos de una localidad especifica, 
los agrupa por mes y año, calcula estadísticas y genera graficas de evolución utilizando matlibplot.
"""
import requests
import matplotlib.pyplot as plt

class RegistroHistoricoDiario:
    """
    Representa un registro meteorológico para un día específico
    Atributos:
        fecha (string con fecha del registro en formato)
        temperatura (float temperatura promedio del día en °C)
        humedad (float de humedad relativa promedio del día en %)
        precipitacion (float de la suma total de precipitación del día en mm)
        viento (float de velocidad maxima del viento del día en km/h)
    """
    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento

class GrupoHistorico:
    """
    Agrupa los registros historicos diarios bajo una etiqueta comun para calcular estadisticas
    Atributos:
        etiqueta (string nombre o identificador del grupo)
        registros (Lista de objetos RegistroHistoricoDiario)
    """
    def __init__(self, etiqueta):
        """
        Inicializa el grupo con su etiqueta y crea la lista vacia para los registros
        """
        self.etiqueta = etiqueta
        self.registros = []

    def agregar_registro(self, registro_diario):
        """
        Agrega un nuevo registro diario a la lista interna del grupo
        """
        self.registros.append(registro_diario)

    def prom_temp(self):
        """
        Calcula y retorna la temperatura promedio de todos los registros
        """
        if not self.registros: return 0.0
        suma = sum(r.temperatura for r in self.registros if r.temperatura is not None)
        return suma / len(self.registros)

    def prom_hum(self):
        """
        Calcula y retorna el porcentaje de humedad promedio
        """
        if not self.registros: return 0.0
        suma = sum(r.humedad for r in self.registros if r.humedad is not None)
        return suma / len(self.registros)

    def suma_prec(self):
        """
        Suma y retorna la precipitacion total acumulada en el grupo
        """
        if not self.registros: return 0.0
        return sum(r.precipitacion for r in self.registros if r.precipitacion is not None)

    def prom_viento(self):
        """
        Calcula y retorna la velocidad promedio del viento
        """
        if not self.registros: return 0.0
        suma = sum(r.viento for r in self.registros if r.viento is not None)
        return suma / len(self.registros)

def consultar_api_historica(localidad_obj, fecha_inicio, fecha_fin):
    """
    Consulta la api para obtener datos meteorologicos historicos.
    localidad_obj (Localidad del objeto con los atributos 'nombre', 'latitud' y 'longitud')
    fecha_inicio (string con la fecha de inicio de la consulta)
    fecha_fin (string con la fecha de fin)
    Retorna una lista de objetos RegistroHistoricoDiario con los datos obtenidos. Retorna una lista vacia si ocurre un error.
    """
    print(f"Consultando historicos para {localidad_obj.nombre}")
    url = (f"https://archive-api.open-meteo.com/v1/archive?"
           f"latitude={localidad_obj.latitud}&longitude={localidad_obj.longitud}&"
           f"start_date={fecha_inicio}&end_date={fecha_fin}&"
           f"daily=temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max&"
           f"timezone=America%2FCaracas")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
        lista_diaria = []
        tiempos = datos["daily"]["time"]
        temps = datos["daily"]["temperature_2m_mean"]
        hums = datos["daily"]["relative_humidity_2m_mean"]
        precs = datos["daily"]["precipitation_sum"]
        vientos = datos["daily"]["wind_speed_10m_max"]
        
        for i in range(len(tiempos)):
            registro = RegistroHistoricoDiario(
                fecha=tiempos[i],
                temperatura=temps[i],
                humedad=hums[i],
                precipitacion=precs[i],
                viento=vientos[i])
            lista_diaria.append(registro)
            
        print("Datos historicos obtenidos con exito")
        return lista_diaria
        
    except Exception as e:
        print(f"Error al consultar la API Historica: {e}")
        return []

def buscar_o_crear_grupo(lista_grupos, etiqueta):
    """
    Busca un GrupoHistorico en una lista si no existe lo crea y lo añade
    Variables:
        lista_grupos (Lista actual de objetos GrupoHistorico)
        etiqueta (Nombre del grupo a buscar o crear).
    Retorna el GrupoHistorico el grupo encontrado o el recien creado.
    """
    for grupo in lista_grupos:
        if grupo.etiqueta == etiqueta:
            return grupo
            
    nuevo_grupo = GrupoHistorico(etiqueta)
    lista_grupos.append(nuevo_grupo)
    return nuevo_grupo

def procesar_y_mostrar_historico(lista_diaria):
    """
    Procesa una lista de registros diarios agrupandolos por mes y por año
    Imprime un resumen mensual y determina los records anuales del periodo
    Variables: lista_diaria (Lista de objetos RegistroHistoricoDiario)
    Retorna: lista_anos, lista_meses (ambas listas contienen objetos GrupoHistorico)
    """
    lista_meses = []
    lista_anos = []
    
    for registro in lista_diaria:
        mes_str = registro.fecha[:7] 
        ano_str = registro.fecha[:4]
        grupo_mes = buscar_o_crear_grupo(lista_meses, mes_str)
        grupo_mes.agregar_registro(registro)
        grupo_ano = buscar_o_crear_grupo(lista_anos, ano_str)
        grupo_ano.agregar_registro(registro)
        
    print("RESUMEN MENSUAL DEL PERIODO")    
    for mes in lista_meses:
        print(f"Mes: {mes.etiqueta}")
        print(f"Temp promedio: {mes.prom_temp()} °C")
        print(f"Humedad promedio: {mes.prom_hum()} %")
        print(f"Precipitacion total: {mes.suma_prec()} mm")
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
    print(f"Año mas caluroso: {ano_mas_caluroso.etiqueta} ({ano_mas_caluroso.prom_temp()} °C)")
    print(f"Año mas fresco: {ano_mas_fresco.etiqueta} ({ano_mas_fresco.prom_temp()} °C)")
    print(f"Año con mayor precipitacion: {ano_mas_lluvioso.etiqueta} ({ano_mas_lluvioso.suma_prec()} mm)")
    print(f"Año con mayor humedad: {ano_mas_humedo.etiqueta} ({ano_mas_humedo.prom_hum()} %)")

    return lista_anos, lista_meses

def graficar_evolucion(lista_anos, lista_meses):
    """
    Genera y muestra una matriz de 4 gráficos (temperatura, humedad, lluvia, viento)
    utilizando Matlibplot. Si se consulta un solo año, grafica por mes si son varios,
    grafica por año.
    Variables:
        lista_anos (Lista de objetos GrupoHistorico agrupados por año)
        lista_meses (Lista de objetos GrupoHistorico agrupados por mes)
    """
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
    fig.suptitle(f'Evolucion {tipo_grafico} de Variables Meteorologicas', fontsize=16)

    axs[0, 0].plot(etiquetas, prom_temps, marker='o', color='tab:red', linewidth=2)
    axs[0, 0].set_title('Temperatura Promedio (°C)')
    axs[0, 0].grid(True, linestyle='--', alpha=0.7)

    axs[0, 1].plot(etiquetas, prom_hums, marker='s', color='tab:blue', linewidth=2)
    axs[0, 1].set_title('Humedad Relativa Promedio (%)')
    axs[0, 1].grid(True, linestyle='--', alpha=0.7)

    axs[1, 0].plot(etiquetas, total_precs, marker='^', color='tab:green', linewidth=2)
    axs[1, 0].set_title('Precipitacion Acumulada (mm)')
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
    """
    Punto de entrada principal para ejecutar el modulo historico.
    Valida las coordenadas, solicita fechas al usuario y ejecuta las consultas
    Variables: localidad_obj (Localidad)
    """
    if not localidad_obj.tiene_coordenadas():
        print("Error, la localidad no posee coordenadas validas")
        return
    print("CONFIGURACION DE BUSQUEDA HISTORICA")
    print("Formato de fecha requerido: AAAA-MM-DD (Ej: 2021-01-01)")
    fecha_inicio = input("Ingrese la fecha de inicio: ")
    fecha_fin = input("Ingrese la fecha de fin: ")
    lista_diaria = consultar_api_historica(localidad_obj, fecha_inicio, fecha_fin)
    if lista_diaria:
        lista_anos, lista_meses = procesar_y_mostrar_historico(lista_diaria)
        graficar_evolucion(lista_anos, lista_meses)