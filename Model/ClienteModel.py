import mysql.connector
from io import BytesIO
from PIL import Image

class ClienteModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_clientes(self):
        try:
            query = "SELECT id, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia FROM clientes"
            # clientes = self.db_connection.fetch_data(query)
            # print("Clientes obtenidos:", clientes)
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []  # Devuelve una lista vacía si hay un error 


    def obtener_cliente_por_id(self, client_id):
        try:
            query = "SELECT * FROM clientes WHERE id = %s"
            params = (client_id,)
            cliente = self.db_connection.fetch_data(query, params)
            if cliente:
                return cliente[0]  # Retorna solo el primer resultado
            return None
        except Exception as e:
            print(f"Error al obtener cliente por ID: {str(e)}")
            return None

    def editar_cliente(self, client_id, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia,):
        try:
            query = "UPDATE clientes SET nombre=%s, apellido=%s, dni=%s,  email=%s, telefono=%s, fecha_nacimiento=%s, cp=%s, domicilio=%s, vencimiento_licencia=%s WHERE id=%s"
            params = (nombre, apellido,dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, client_id)
            self.db_connection.execute_query(query, params)
            print("Cliente editado con éxito")
        except Exception as e:
            print(f"Error al editar cliente: {str(e)}")

    def eliminar_cliente(self, client_id):
        try:
            query = "DELETE FROM clientes WHERE id = %s"
            params = (client_id,)
            self.db_connection.execute_query(query, params)
            print("Cliente eliminado con éxito")
        except Exception as e:
            print(f"Error al eliminar cliente: {str(e)}")

    def buscar_clientes(self, search_query):
        try:
            query = "SELECT nombre, apellido WHERE nombre LIKE %s OR apellido LIKE %s"
            params = (f'%{search_query}%', f'%{search_query}%')
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al buscar clientes: {str(e)}")
            return []

    def obtener_companias(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []

    def agregar_cliente(self, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado):
        dni_foto_data = dni_foto if dni_foto else None
        foto_licencia_data = foto_licencia if foto_licencia else None
        
        print('fecha', vencimiento_licencia)
        if vencimiento_licencia == "":
            vencimiento_licencia = '2000-02-03'
        
        print('fecha: ', vencimiento_licencia)
        
        # if estado == "": id_cliente
        estado = 'activo'
        
        print('estado: ', estado)
            
        sql = """INSERT INTO clientes (nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto_data, foto_licencia_data, estado)

        try:
            self.db_connection.execute_query(sql, valores)
            print("Cliente agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar el cliente: {str(e)}")
            
    def convertir_imagen_a_bytes(self, imagen):
        if imagen:
            img = Image.open(imagen)
            byte_array = BytesIO()
            img.save(byte_array, format='PNG')  # o el formato que necesites
            return byte_array.getvalue()
        return None
