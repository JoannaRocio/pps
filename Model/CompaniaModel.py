class CompaniaModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_companias(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []
        
    def obtener_compania_por_id(self, compania_id):
        try:
            query = "SELECT * FROM companias WHERE id_compania = %s"
            params = (compania_id,)
            compania = self.db_connection.fetch_data(query, params)
            if compania:
                return compania[0]  # Retorna solo el primer resultado
            return None
        except Exception as e:
            print(f"Error al obtener compañía por ID: {str(e)}")
            return None
    
    def agregar_compania(self, nombre, sitio_web):
        try:
            query = "INSERT INTO companias (nombre, sitio_web) VALUES (%s, %s)"
            params = (nombre, sitio_web)
            self.db_connection.execute_query(query, params)
            print("Compañía agregada con éxito")
        except Exception as e:
            print(f"Error al agregar compañía: {str(e)}")

    def editar_compania(self, compania_id, nombre, sitio_web):
        try:
            query = "UPDATE companias SET nombre=%s, sitio_web=%s WHERE id_compania=%s"
            params = (nombre, sitio_web, compania_id)
            self.db_connection.execute_query(query, params)
            print("Compañía editada con éxito")
        except Exception as e:
            print(f"Error al editar compañía: {str(e)}")

    def deshabilitar_compania(self, compania_id):
        try:
            query = "UPDATE companias SET estado = 'inactivo' WHERE id_compania = %s"
            params = (compania_id,)
            self.db_connection.execute_query(query, params)
            print("Compañía deshabilitada con éxito")
        except Exception as e:
            print(f"Error al deshabilitar compañía: {str(e)}")
    
    def habilitar_compania(self, company_id):
        """Habilita una compañía en la base de datos"""
        try:
            query = "UPDATE companias SET estado = 'activo' WHERE id_compania = %s"
            params = (company_id,)
            self.db_connection.execute_query(query, params)
            print("Compañía habilitada con éxito")
        except Exception as e:
            print(f"Error al habilitar compañía: {str(e)}")



    def buscar_companias(self, search_query):
        try:
            query = "SELECT id_compania, nombre, sitio_web FROM companias WHERE nombre LIKE %s OR sitio_web LIKE %s"
            params = (f'%{search_query}%', f'%{search_query}%')
            return self.db_connection.fetch_data(query, params)
        except Exception as e:
            print(f"Error al buscar compañías: {str(e)}")
            return []
