class VencimientosModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def mostrar_vencimientos(self):
        try:
            query = "SELECT cliente_id, apellido, patente, vencimiento_licencia, vencimiento_poliza FROM vencimientos"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []
        
