class VencimientosModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def mostrar_vencimientos(self):
        try:        
            query = "SELECT c.nombre, c.apellido, v.patente, c.vencimiento_licencia, v.vencimiento_poliza FROM clientes c JOIN  vehiculos v ON c.id = v.cliente_id"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []
        
    def buscar_clientes(self, search_query):
        try:
            # La consulta SQL busca tanto en la tabla clientes (nombre y apellido)
            # como en la tabla vehiculos (patente). Usamos un JOIN para combinarlas.
            query = """
            SELECT c.id_cliente, c.nombre, c.apellido, c.telefono, c.dni, v.patente
            FROM clientes c
            LEFT JOIN vehiculos v ON c.id_cliente = v.id_cliente
            WHERE c.nombre LIKE %s OR c.apellido LIKE %s OR v.patente LIKE %s
        """
            # Parametros para la búsqueda: nombre, apellido, patente
            params = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
        
            # Ejecutamos la consulta y obtenemos los datos
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al buscar clientes y vehículos: {str(e)}")
            return []
