import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.host = '127.0.0.1'  # Cambiar por la dirección de tu servidor MySQL
        self.database = 'gestion_seguros'
        # self.user = 'root'
        self.user = 'root'
        self.password = '1920'
        self.connection = None

    def connect(self):
        """
        Establece la conexión a la base de datos.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
        
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL y maneja los errores.
        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros opcionales para la consulta.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("Consulta ejecutada con éxito")
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            if cursor:
                cursor.close()

    def fetch_data(self, query, params=None):
        """
        Realiza una consulta SELECT y devuelve los resultados.
        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros opcionales para la consulta.
        :return: Resultados de la consulta.
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al obtener los datos: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")
