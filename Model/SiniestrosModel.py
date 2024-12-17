

class SiniestrosModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    

    def obtener_vehiculos(self, cliente_id):
        """Obtiene los vehículos asociados a un cliente."""
        query = "SELECT id, patente, modelo FROM vehiculos WHERE cliente_id = ?"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (cliente_id,))
        vehiculos = cursor.fetchall()
        cursor.close()
        return vehiculos

        
    def guardar_siniestro(self, cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo):
        """Guardar el siniestro en la base de datos."""
        try:
            # Insertar siniestro en la tabla 'siniestros'
            query_siniestro = """INSERT INTO siniestros 
                                (nombre, vehiculo_id, estado, descripcion, fecha_inicio_siniestro, imagenes, archivo) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores_siniestro = (cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo)
            self.db_connection.execute_query(query_siniestro, valores_siniestro)
            print("Siniestro guardado exitosamente.")
            
            # Obtener el último siniestro_id insertado
            query_last_id = "SELECT LAST_INSERT_ID()"
            last_inserted_id = self.db_connection.fetch_data(query_last_id)
            
            if last_inserted_id:
                last_inserted_id = last_inserted_id[0][0]
                print(f"Último siniestro_id insertado: {last_inserted_id}")
                
                # Aquí podrías insertar más registros relacionados si es necesario
                # Por ejemplo, si hay otra tabla relacionada con el siniestro, podrías insertar datos relacionados.
                # Si no es necesario, este paso se puede omitir.

            else:
                print("No se pudo obtener el último siniestro_id insertado.")
                
        except Exception as e:
            print(f"Error al guardar el siniestro: {str(e)}")

    def obtener_siniestros(self):
        query = """
        SELECT 
            s.id AS siniestro_id,
            s.nombre AS siniestro_nombre,
            s.estado AS siniestro_estado,
            s.denuncia_de_siniestro AS siniestro_denuncia,
            s.imagenes AS siniestro_imagenes,
            s.archivo AS siniestro_archivo,
            s.link_url AS siniestro_link,
            v.id AS vehiculo_id,
            v.patente AS vehiculo_patente, 
            v.modelo AS vehiculo_nombre,
            c.nombre AS cliente_nombre,
            c.apellido AS cliente_apellido,
            c.dni AS cliente_dni,
            co.nombre AS compania_nombre,  -- Nombre de la compañía aseguradora
            co.sitio_web AS compania_sitio_web  -- Sitio web de la compañía aseguradora
        FROM 
            siniestros s
        JOIN 
            vehiculos v ON s.vehiculo_id = v.id
        JOIN 
            clientes c ON v.cliente_id = c.id
        JOIN 
            companias co ON v.compania_id = co.id_compania;  -- Relación correcta con id_compania en la tabla companias
      """
        return self.db_connection.fetch_data(query)
    
    def obtener_siniestro_por_id(self, siniestro_id):
        try:
            # Realiza la consulta para obtener el siniestro por ID, seleccionando todos los campos
            query = "SELECT * FROM siniestros WHERE id = %s"
            result = self.db_connection.fetch_data(query, (siniestro_id,))

            # Si se encontró el siniestro, convierte la tupla en un diccionario
            if result:
                # Suponiendo que la consulta devuelve solo un siniestro
                siniestro = result[0]  # Obtenemos la primera tupla

                # Convertimos la tupla en un diccionario con todos los campos del siniestro
                siniestro_dict = {
                    "id": siniestro[0],  
                    "nombre": siniestro[1],  
                    "estado": siniestro[2], 
                    "fecha_inicio_siniestro": siniestro[8],  
                    "descripcion": siniestro[9],  
                    "imagenes": siniestro[4],
                    "archivo": siniestro[5],
                    
                     
                    # Añadir otros campos según lo necesites
                }
                return siniestro_dict
            else:
                print(f"No se encontró el siniestro con ID: {siniestro_id}")
                return None
        except Exception as e:
            print(f"Error al obtener siniestro: {e}")
            return None

    