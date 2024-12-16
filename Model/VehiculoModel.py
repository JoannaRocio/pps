import mysql.connector

class VehiculoModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_vehiculos_por_cliente(self, cliente_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehiculos WHERE cliente_id = %s", (cliente_id,))
        return cursor.fetchall()
    
    def obtener_compania(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            companias = self.db_connection.fetch_data(query)
            
            nombres_companias = [compania[1] for compania in companias]  # compania[1] es el nombre
            
            return nombres_companias
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []


    def agregar_vehiculo(self, marca, modelo, anio, patente, compania_id, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza):
        
        query = """ INSERT INTO vehiculos ( marca, modelo, anio, patente, compania_id, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
        valores = (marca, modelo, anio, patente, compania_id, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza)
        
        self.db_connection.execute_query(query, valores)
        print("ok")
