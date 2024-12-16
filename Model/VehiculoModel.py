import mysql.connector

class VehiculoModel:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def obtener_compania(self):
        try:
            query = "SELECT id_compania, nombre, sitio_web, estado FROM companias"
            companias = self.db_connection.fetch_data(query)
            
            nombres_companias = [compania[1] for compania in companias]  # compania[1] es el nombre
            
            return nombres_companias
        except Exception as e:
            print(f"Error al obtener compañías: {str(e)}")
            return []

    def obtener_id(self,compania_id):
        try:
            # Definir la consulta SQL para obtener el id de la compañía por su nombre
            query = "SELECT id_compania FROM companias WHERE nombre = %s"
            
            # Ejecutar la consulta y obtener el resultado
            result = self.db_connection.fetch_data(query, (compania_id,))
            
            # Verificar si se encontró un resultado
            if result:
                return result[0][0]  # Retorna el primer resultado, que es el id_compania
            else:
                print(f"No se encontró la compañía con el nombre: {compania_id}")
                return None  # Si no se encuentra, retornar None

        except Exception as e:
            print(f"Error al obtener id_compania por nombre: {str(e)}")
            return None  # Si hay un error, retornar None


    def agregar_vehiculo(self,cliente_id, marca, modelo, anio, patente, compania_id, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza):
        
        compania = self.obtener_id(compania_id)
        
        try:
            query = """INSERT INTO vehiculos 
                       ( cliente_id, marca, modelo, anio, patente, compania_id, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = ( cliente_id, marca, modelo, anio, patente, compania, tipo_vehiculo, tipo_categoria, accesorios, vencimiento_poliza)
            self.db_connection.execute_query(query, valores)
            print("Cliente agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar el cliente: {str(e)}")
            
    def obtener_vehiculo(self, cliente_id):
        try: 
            # Consulta SQL mejorada con JOIN
            query = """
            SELECT 
                v.*,  -- Todos los campos de la tabla vehiculos
                c.nombre AS cliente_nombre,  -- Nombre del cliente
                cmp.nombre AS compania_nombre  -- Nombre de la compañía
            FROM vehiculos v
            JOIN clientes c ON v.cliente_id = c.id  -- Relaciona vehiculos con clientes
            JOIN companias cmp ON v.compania_id = cmp.id_compania  -- Relaciona vehiculos con companias
            WHERE v.cliente_id = %s
            """
            
            # Ejecutamos la consulta pasando cliente_id como parámetro
            resultado = self.db_connection.fetch_data(query, (cliente_id,))
            print(resultado)
            
            if resultado:
                return resultado[0]  # Retorna el primer registro de la consulta
            
            return None  # Si no hay resultados, retorna None
        
        except Exception as e:
            print(f"Error al obtener vehículo: {str(e)}")
            return None  # Si ocurre un error, retorna None
