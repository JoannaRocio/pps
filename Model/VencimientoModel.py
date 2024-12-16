import mysql.connector

class VencimientosModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def mostrar_vencimientos(self):
        query = """
        SELECT 
            cli.nombre AS cliente_nombre, 
            cli.apellido AS cliente_apellido, 
            cli.vencimiento_licencia, 
            ve.patente AS vehiculo_patente,
            ve.vencimiento_poliza,  
            c.nombre AS compania_nombre,
            c.sitio_web  
        FROM 
            clientes AS cli
        JOIN 
            vencimientos AS ven ON cli.id = ven.cliente_id
        JOIN 
            vehiculos AS ve ON cli.id = ve.cliente_id
        JOIN 
            companias AS c ON ve.compania_id = c.id_compania
        ORDER BY
            ve.vencimiento_poliza ASC
        LIMIT 1000;
        """
        return self.db_connection.fetch_data(query)


    def obtener_companias(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []
