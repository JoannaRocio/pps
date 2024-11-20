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
        
