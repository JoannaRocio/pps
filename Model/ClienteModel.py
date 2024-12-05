import mysql.connector
from io import BytesIO
from PIL import Image

class ClienteModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_clientes(self):
        """Obtiene todos los clientes activos con datos básicos."""
        try:
            query = """SELECT id, nombre, apellido, dni, email, telefono, 
                              fecha_nacimiento, cp, domicilio, vencimiento_licencia 
                       FROM clientes WHERE estado = 'activo'"""
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []

    def obtener_cliente_por_id(self, client_id):
        """Obtiene todos los datos de un cliente específico por su ID."""
        try:
            query = "SELECT * FROM clientes WHERE id = %s"
            params = (client_id,)
            cliente = self.db_connection.fetch_data(query, params)
            # Asegúrate de que se devuelve como un diccionario
            return cliente[0] if cliente else None
        except Exception as e:
            print(f"Error al obtener cliente por ID: {str(e)}")
            return None

    def editar_cliente(self, client_id, nombre, apellido, dni, email, telefono,
                    fecha_nacimiento, cp, domicilio, vencimiento_licencia,
                    dni_foto=None, foto_licencia=None):
        """Edita los datos de un cliente, incluyendo imágenes opcionales."""
        try:
            # Obtener los datos actuales del cliente
            cliente_actual = self.obtener_cliente_por_id(client_id)

            if not cliente_actual:
                print(f"No se encontró el cliente con ID {client_id}.")
                return

            # Usar las imágenes actuales si no se proporcionan nuevas
            dni_foto = dni_foto if dni_foto is not None else cliente_actual['dni_foto']
            foto_licencia = foto_licencia if foto_licencia is not None else cliente_actual['foto_licencia']

            # Query para actualizar los datos del cliente
            query = """
            UPDATE clientes 
            SET nombre=%s, apellido=%s, dni=%s, email=%s, telefono=%s, 
                fecha_nacimiento=%s, cp=%s, domicilio=%s, vencimiento_licencia=%s,
                dni_foto=%s, foto_licencia=%s 
            WHERE id=%s
            """
            params = (
                nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, 
                domicilio, vencimiento_licencia, dni_foto, foto_licencia, client_id
            )
            self.db_connection.execute_query(query, params)
            print("Cliente editado con éxito, incluyendo imágenes.")
        except Exception as e:
            print(f"Error al editar cliente: {str(e)}")

    def eliminar_cliente(self, client_id):
        """Deshabilita a un cliente estableciendo su estado como 'inactivo'."""
        try:
            query = "UPDATE clientes SET estado = 'inactivo' WHERE id = %s"
            params = (client_id,)
            self.db_connection.execute_query(query, params)
            print("Cliente deshabilitado con éxito.")
        except Exception as e:
            print(f"Error al deshabilitar cliente: {str(e)}")

    def buscar_clientes(self, search_query):
        """Busca clientes activos por nombre o apellido."""
        try:
            query = """SELECT nombre, apellido 
                       FROM clientes 
                       WHERE estado = 'activo' AND (nombre LIKE %s OR apellido LIKE %s)"""
            params = (f'%{search_query}%', f'%{search_query}%')
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al buscar clientes: {str(e)}")
            return []

    def agregar_cliente(self, nombre, apellido, dni, email, telefono, fecha_nacimiento, 
                        cp, domicilio, vencimiento_licencia="2000-02-03", dni_foto=None, 
                        foto_licencia=None, estado="activo"):
        """Agrega un cliente nuevo, incluyendo imágenes opcionales."""
        try:
            query = """INSERT INTO clientes 
                       (nombre, apellido, dni, email, telefono, fecha_nacimiento, 
                        cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, 
                       domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado)
            self.db_connection.execute_query(query, valores)
            print("Cliente agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar el cliente: {str(e)}")

    def convertir_imagen_a_bytes(self, imagen):
        """Convierte una imagen de PIL a bytes para almacenar en la base de datos."""
        try:
            byte_array = BytesIO()
            imagen.save(byte_array, format='PNG')  # Cambia 'PNG' si necesitas otro formato
            return byte_array.getvalue()
        except Exception as e:
            print(f"Error al convertir imagen: {str(e)}")
            return None