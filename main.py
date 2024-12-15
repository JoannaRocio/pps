import customtkinter as ctk
from tkinter import messagebox
from Model.SiniestrosModel import SiniestrosModel
from Model.CompaniaModel import CompaniaModel
from Model.ClienteModel import ClienteModel
from Model.UsuarioModel import UsuarioModel
from Model.VencimientosModel import VencimientosModel
from Model.vehiculo_model import VehiculoModel
from db.db_connection import DatabaseConnection
from Views.Login.login_view import UsuarioView
from Views.Home.home_view import HomeView


def on_login_success():
    # Crear la ventana principal después del login
    root = ctk.CTk()  # Nueva ventana para el dashboard principal
    root.title("Sistema de Gestión de Clientes")

    # Llama a update_idletasks para asegurar que se calcule correctamente el tamaño
    root.update_idletasks()

    # Obtén el ancho y alto de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Define el ancho y alto de la ventana
    window_width = 900  # o el tamaño que quieras
    window_height = 600

    # Calcula la posición x e y para centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establece la geometría de la ventana centrada
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Crear una instancia del modelo y de la vista principal
    
    cliente_model = ClienteModel(db_connection)
    compania_model = CompaniaModel(db_connection)
    vencimiento_model = VencimientosModel(db_connection)
    siniestros_model = SiniestrosModel(db_connection)
    vehiculo_model = VehiculoModel(db_connection)
    
    app = HomeView(root, cliente_model, compania_model, vencimiento_model, siniestros_model, vehiculo_model)

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()


def main():
    # Inicializar la conexión a la base de datos
    global db_connection
    db_connection = DatabaseConnection()
    try:
        db_connection.connect()
        print("Conexión exitosa a la base de datos")

        # Crear la ventana principal
        root = ctk.CTk()

        # Crear una instancia del modelo de usuario
        usuario_model = UsuarioModel()
        # Crear una instancia del login y esperar a que se loguee correctamente
        
        # despues descomentar esto asi inicia el login
        login_view = UsuarioView(root, usuario_model, on_login_success)
        
        # despues borrar esto
        # cliente_model = 1
        # app = HomeView(root, cliente_model)id
        # borrar lo que hay entre medio
        
        
        root.mainloop()  # Ejecutar la vista de login

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar la conexión al finalizar
        db_connection.close_connection()
        print("Conexión cerrada")
        
if __name__ == "__main__":
    main()
