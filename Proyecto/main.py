class App:
    def __init__(self):
        self.db_municipios = []

    def run(self):
        print("Iniciando Sistema de Monitoreo del Clima - Caracas")

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
                pass
                
            elif option == '3': 
                pass
                
            elif option == '4': 
                pass
                
            elif option == '5':
                print('Guardando datos de la sesion')
                pass
                print('Ha salido del sistema con exito')
                break
            else:
                print('Ingreso invalido, por favor intente de nuevo')

    def mostrar_reporte_carga(self):
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
            print(f"d. Porcentaje con coordenadas: {porcentaje}%\n")
            
        input("Presione enter para continuar")

if __name__ == '__main__':
    app = App()
    app.run()