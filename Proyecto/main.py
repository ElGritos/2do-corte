import sys

class App:
    def __init__(self):
        self.db_municipios = []
        self.historial_consultas = []

    def run(self):
        # MENÚ PRINCIPAL
        while True:
            print('SISTEMA DE MONITOREO DEL CLIMA - CARACAS')
            option = input('''
            Ingrese el número correspondiente a la acción que desea realizar:
            1. Consultar clima en tiempo real
            2. Consultar datos históricos y gráficos
            3. Ver reportes y estadísticas
            4. Cerrar sistema
            >>> ''')
            
            if option == '1': # REQUERIMIENTO 2
                pass
            elif option == '2': # REQUERIMIENTO 4
                pass
            elif option == '3': # REQUERIMIENTO 3
                pass
            elif option == '4':
                print('Guardando datos de la sesión...')
                print('Ha salido del sistema con éxito. ¡Hasta luego!')
                break
            else:
                print('Ingreso inválido. Por favor intente de nuevo.')

    def menu_clima_actual(self):
        while True:
            print('CONSULTA DE CLIMA EN TIEMPO REAL')
            option = input('''
            Seleccione el método de búsqueda:
            1. Buscar por Municipio y Localidad (Lista desplegable)
            2. Búsqueda directa por nombre de Localidad
            3. Volver al menú principal
            >>> ''')
            
            if option == '1':
                pass
            elif option == '2':
                pass
            elif option == '3':
                print('Regresando al menú principal...')
                break
            else:
                print('Ingreso inválido!!!')

    def menu_historico(self):
        print('CONSULTA DE DATOS HISTÓRICOS Y GRÁFICOS')
        pass
        print("(Módulo en construcción...)")
        input("Presione ENTER para volver al menú principal...")

    def menu_estadisticas(self):
        while True:
            print('MÓDULO DE REPORTES Y ESTADÍSTICAS')
            option = input('''
            Ingrese el número correspondiente al reporte:
            1. Ranking de Temperatura (Localidad más cálida y fría de la sesión)
            2. Cobertura Geográfica (Localidades sin coordenadas registradas)
            3. Promedio General de temperatura (De las consultas de hoy)
            4. Volver al menú principal
            >>> ''')
            
            if option == '1':
                pass
            elif option == '2':
                pass
            elif option == '3':
                pass
            elif option == '4':
                print('Regresando al menú principal...')
                break
            else:
                print('Ingreso inválido!!!')

if __name__ == '__main__':
    app = App()
    app.run()