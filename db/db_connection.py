import mysql.connector
from mysql.connector import Error
import os
import subprocess
from tkinter import messagebox
#
class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'  # Cambiar por la dirección de tu servidor MySQL
        self.database = 'gestion_seguros'
        self.user = 'root'
        self.password = '1920'
        self.port = 3306
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
                password=self.password,
                port=self.port
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
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión a la base de datos.")
            return

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
        if not self.connection or not self.connection.is_connected():
            print("Conexión perdida, intentando reconectar...")
            self.connect()  
        
        print("Conexión activa, ejecutando consulta...")
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

    def backup(self):
        print("entro")
        usuario = "root" 
        contrasena = "1234" 
        base_de_datos = "gestion_seguros" 
        ruta_respaldo = "C:/Users/RL/Desktop/coli/mi_db_backup.sql"
        
        if not os.path.exists(os.path.dirname(ruta_respaldo)):
            os.makedirs(os.path.dirname(ruta_respaldo))
    
        #comando = f"mysqldump -u {usuario} -p{contrasena} {base_de_datos} > {ruta_respaldo}"
        #comando = f"C:\Program^ Files\MySQL\MySQL^ Server^ 8.0\bin\mysqldump -u {usuario} -p{contrasena} {base_de_datos} > {ruta_respaldo}"
        comando = f'"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump" -u {usuario} -p{contrasena} {base_de_datos} > {ruta_respaldo}'

        try:
            # Ejecutar el comando
            subprocess.run(comando, shell=True, check=True)
            messagebox.showinfo("Éxito", "El respaldo se ha realizado con éxito.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Hubo un problema al hacer el respaldo: {e}")