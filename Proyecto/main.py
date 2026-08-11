"""
Modulo principal de la aplicacion.
Este codigo inicializa la clase app. Nos da una interfaz 
de linea de comandos con menus interactivos para acceder a los 
distintos modulos del programa.
"""
from Modulos.manejodeinformacion import *
from Modulos.climaactual import *
from Modulos.estadistica import *
from Modulos.historicos import *

class App:
    """
    Clase principal que gestiona el estado y la navegación del sistema.
    Variables:
        db_municipios (Lista que almacena los objetos Municipio cargados)
        historial_consultas (Lista que almacena el historial de consultas de la sesion).
    """
    def __init__(self):
        """Inicializa las estructuras de datos vacias para la aplicacion"""
        self.db_municipios = [] 
        self.historial_consultas = []

    def run(self):
        """
        Inicia la ejecucion del sistema.
        Carga los datos iniciales desde los archivos locales y muestra el menu principal, 
        manteniendo un bucle hasta que el usuario decida salir y guardar.
        """
        print("Iniciando Sistema de Monitoreo del Clima - Caracas")
        self.db_municipios, self.historial_consultas = read_files()

        if not self.db_municipios:
            print("No se pudieron cargar los municipios")
            return
        
        while True:
            print('SISTEMA DE MONITOREO DEL CLIMA - CARACAS')
            option = input('''
            Seleccione el requerimiento que desea ejecutar:
            1. Reporte de Carga de Datos inicial
            2. Consulta del clima en tiempo real
            3. Reportes y Estadísticas
            4. Históricos (Consulta por período y gráficos)
            5. Guardar y Cerrar sistema
            >>> ''')
            
            if option == '1':
                self.mostrar_reporte_carga()
                
            elif option == '2':
                self.menu_clima_actual()
                
            elif option == '3':
                self.menu_estadisticas()
                
            elif option == '4':
                self.menu_historico()
                
            elif option == '5':
                print('Guardando datos de la sesion')
                guardar_historial(self.historial_consultas)
                print('Ha salido del sistema con exito')

                break
            else:
                print('Ingreso invalido, por favor intente de nuevo')

    def mostrar_reporte_carga(self):
        """
        Calcula y muestra la informacion de la base de datos
        Por cada municipio detalla la cantidad de localidades, cuantas de
        ellas poseen coordenadas geograficas validas y su porcentaje de cobertura.
        """
        print('REPORTE DE CARGA DE DATOS')        

        for municipio in self.db_municipios:
            total_loc = len(municipio.localidades)
            con_coord = sum(1 for loc in municipio.localidades if loc.tiene_coordenadas())
            sin_coord = total_loc - con_coord
            porcentaje = (con_coord / total_loc * 100) if total_loc > 0 else 0
            print(f"Municipio: {municipio.nombre}")
            print(f"a. Localidades cargadas: {total_loc}")
            print(f"b. Con coordenadas geográficas: {con_coord}")
            print(f"c. Sin coordenadas geográficas: {sin_coord}")
            print(f"d. Porcentaje con coordenadas: {porcentaje}%")

    def menu_clima_actual(self):
        """
        Muestra el submenu para las consultas de clima en tiempo real
        Permite al usuario elegir entre buscar mediante una navegación por municipio o por busqueda directa escribiendo el nombre.
        """
        while True:
            print('CONSULTA DE CLIMA EN TIEMPO REAL')
            option = input('''
            Seleccione el método de búsqueda:
            1. Buscar por Municipio y Localidad (Lista desplegable)
            2. Búsqueda directa por nombre de Localidad
            3. Volver al menú principal
            >>> ''')
            
            if option == '1':
                ejecutar_modulo_clima_actual(self.db_municipios, self.historial_consultas, modo="lista")
            elif option == '2':
                ejecutar_modulo_clima_actual(self.db_municipios, self.historial_consultas, modo="directa")
            elif option == '3':
                print('Regresando al menú principal')
                break
            else:
                print('Ingreso inválido')

    def menu_estadisticas(self):
        """
        Muestra el submenu para la generacion de reportes y estadisticas.
        Ofrece opciones para ver rankings y promedios de la sesion,
        o para verificar la cobertura geografica (localidades sin coordenadas).
        """
        while True:
            print('MODULO DE REPORTES Y ESTADISTICAS')
            option = input('''
            Ingrese el número correspondiente al reporte:
            1. Ranking de Temperatura y Promedio General
            2. Cobertura Geografica 
            3. Volver al menu principal
            >>> ''')
            
            if option == '1':
                calcular_estadisticas_consultas(self.historial_consultas)
            elif option == '2':
                mostrar_localidades_sin_coordenadas(self.db_municipios)
            elif option == '3':
                print('Regresando al menu principal')
                break
            else:
                print('Ingreso invalido')

    def menu_historico(self):
        """
        Ejecuta lavisualizacion de datos historicos y graficos
        Inicia buscando la localidad deseada y luego transfiere el control
        al modulo de historicos para consultar la api y generar los graficos.
        """
        print('CONSULTA DE DATOS HISTORICOS Y GRAFICOS')
        mun_obj, loc_obj = buscar_localidad(self.db_municipios)
        if loc_obj:
            ejecutar_modulo_historicos(loc_obj)
        input("Presione enter para volver al menú principal")
        
if __name__ == '__main__':
    app = App()
    app.run()
