import mysql.connector
from io import BytesIO
from PIL import Image

class ClienteModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def obtener_clientes(self):
        try:
            query = "SELECT id, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, estado FROM clientes"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []

    def obtener_cliente_por_id(self, client_id):
        try:
            query = "SELECT * FROM clientes WHERE id = %s"
            params = (client_id,)
            cliente = self.db_connection.fetch_data(query, params)
            
            if cliente:
                return cliente[0]  # Retorna la primera tupla de la lista
            return None
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

            if dni_foto == None:
                dni_foto = cliente_actual[10]

            if foto_licencia == None:
                foto_licencia = cliente_actual[11]

            if not cliente_actual:
                print(f"No se encontró el cliente con ID {client_id}.")
                return

           

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
        try:
            query = """SELECT id, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia 
                    FROM clientes 
                    WHERE estado = 'activo' AND (nombre LIKE %s OR apellido LIKE %s OR dni LIKE %s)"""
            params = (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al buscar clientes: {str(e)}")
            return []


    def agregar_cliente(self, nombre, apellido, dni, email, telefono, fecha_nacimiento, 
                        cp, domicilio, vencimiento_licencia="2000-02-03", dni_foto=None, 
                        foto_licencia=None, estado="activo"):
        try:
            # Insertar cliente
            query_cliente = """INSERT INTO clientes 
                            (nombre, apellido, dni, email, telefono, fecha_nacimiento, 
                                cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores_cliente = (nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, 
                            domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado)
            self.db_connection.execute_query(query_cliente, valores_cliente)
            print("Cliente agregado exitosamente.")
            
            # Obtener el último cliente_id insertado
            query_last_id = "SELECT LAST_INSERT_ID()"
            last_inserted_id = self.db_connection.fetch_data(query_last_id)
            
            if last_inserted_id:
                last_inserted_id = last_inserted_id[0][0]
                print(f"Último cliente_id insertado: {last_inserted_id}")
                
                # Insertar vencimiento asociado al cliente
                query_vencimiento = """INSERT INTO vencimientos (cliente_id) 
                                    VALUES (%s)"""
                self.db_connection.execute_query(query_vencimiento, (last_inserted_id,))
                print("Registro de vencimiento agregado exitosamente.")
            else:
                print("No se pudo obtener el último cliente_id insertado.")
            
        except Exception as e:
            print(f"Error al agregar el cliente o el vencimiento: {str(e)}")



    def convertir_imagen_a_bytes(self, imagen):
        """Convierte una imagen de PIL a bytes para almacenar en la base de datos."""
        try:
            byte_array = BytesIO()
            imagen.save(byte_array, format='PNG')  # Cambia 'PNG' si necesitas otro formato
            return byte_array.getvalue()
        except Exception as e:
            print(f"Error al convertir imagen: {str(e)}")
            return None
    
    def deshabilitar_cliente(self, client_id):
        try:
            query = "UPDATE clientes SET estado = 'inactivo' WHERE id = %s"
            params = (client_id,)
            self.db_connection.execute_query(query, params)
            print("Cliente deshabilitado con éxito")
        except Exception as e:
            print(f"Error al deshabilitar cliente: {str(e)}")
    
    def habilitar_cliente(self, client_id):
        try:
            query = "UPDATE clientes SET estado = 'activo' WHERE id = %s"
            params = (client_id,)
            self.db_connection.execute_query(query, params)
            print("Cliente habilitado con éxito")
        except Exception as e:
            print(f"Error al habilitar cliente: {str(e)}")

    def obtener_clientes_sinestro(self, search_term=None):
        try:
            # Modificar la consulta para usar el search_term si está presente
            query = "SELECT id, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, estado FROM clientes"
            
            # Si se proporciona un término de búsqueda, se añade a la consulta
            if search_term:
                query += " WHERE nombre LIKE %s OR apellido LIKE %s OR dni LIKE %s"
                params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
            else:
                params = ()
            
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []
