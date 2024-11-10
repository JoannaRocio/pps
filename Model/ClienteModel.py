class ClienteModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_clientes(self):
        try:
            query = "SELECT id_cliente, nombre, apellido, telefono, dni FROM clientes"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener clientes: {str(e)}")
            return []

    def obtener_cliente_por_id(self, client_id):
        try:
            query = "SELECT * FROM clientes WHERE id_cliente = %s"
            params = (client_id,)
            cliente = self.db_connection.fetch_data(query, params)
            if cliente:
                return cliente[0]  # Retorna solo el primer resultado
            return None
        except Exception as e:
            print(f"Error al obtener cliente por ID: {str(e)}")
            return None

    def agregar_cliente(self, nombre, apellido, telefono, dni, direccion, email, fecha_nacimiento):
        try:
            query = "INSERT INTO clientes (nombre, apellido, telefono, dni, direccion, email, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            params = (nombre, apellido, telefono, dni, direccion, email, fecha_nacimiento)
            self.db_connection.execute_query(query, params)
            print("Cliente agregado con éxito")
        except Exception as e:
            print(f"Error al agregar cliente: {str(e)}")

    def editar_cliente(self, client_id, nombre, apellido, telefono, dni, direccion, email, fecha_nacimiento):
        try:
            query = "UPDATE clientes SET nombre=%s, apellido=%s, telefono=%s, dni=%s, direccion=%s, email=%s, fecha_nacimiento=%s WHERE id_cliente=%s"
            params = (nombre, apellido, telefono, dni, direccion, email, fecha_nacimiento, client_id)
            self.db_connection.execute_query(query, params)
            print("Cliente editado con éxito")
        except Exception as e:
            print(f"Error al editar cliente: {str(e)}")

    def eliminar_cliente(self, client_id):
        try:
            query = "DELETE FROM clientes WHERE id_cliente = %s"
            params = (client_id,)
            self.db_connection.execute_query(query, params)
            print("Cliente eliminado con éxito")
        except Exception as e:
            print(f"Error al eliminar cliente: {str(e)}")

    def buscar_clientes(self, search_query):
        try:
            query = "SELECT id_cliente, nombre, apellido, telefono, dni FROM clientes WHERE nombre LIKE %s OR apellido LIKE %s"
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