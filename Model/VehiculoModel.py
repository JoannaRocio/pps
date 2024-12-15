import mysql.connector

class VehiculoModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_vehiculos_por_cliente(self, cliente_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehiculos WHERE cliente_id = %s", (cliente_id,))
        return cursor.fetchall()

    def agregar_vehiculo(self, cliente_id, marca, modelo, anio, tipo_vehiculo, tipo_categoria, vencimiento_poliza, patente, compania_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO vehiculos (cliente_id, marca, modelo, anio, tipo_vehiculo, tipo_categoria, vencimiento_poliza, patente, compania_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (cliente_id, marca, modelo, anio, tipo_vehiculo, tipo_categoria, vencimiento_poliza, patente, compania_id))
        self.connection.commit()
