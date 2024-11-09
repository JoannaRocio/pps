class CompaniaModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def obtener_companias(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web FROM companias"
            return self.db_connection.fetch_data(query)
        except Exception as e:
            print(f"Error al obtener compañias: {str(e)}")
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
            print(f"Error al obtener compañia por ID: {str(e)}")
            return None