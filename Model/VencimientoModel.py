import mysql.connector

class VencimientosModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def mostrar_vencimientos(self):
        query = """
        SELECT 
            cli.nombre, 
            cli.apellido, 
            cli.vencimiento_licencia, 
            ve.vencimiento_poliza,  
            c.sitio_web  
        FROM 
            clientes AS cli
        JOIN 
            vencimientos AS ven ON cli.id = ven.cliente_id
        JOIN 
            vehiculos AS ve ON ve.cliente_id = ven.cliente_id
        JOIN 
            companias AS c ON c.id_compania = ve.compania_id
        LIMIT 0, 1000;
        """
        return self.db_connection.fetch_data(query)

    def obtener_companias(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []
