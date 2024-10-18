import customtkinter as ctk
from tkinter import messagebox
from Model.ClienteModel import ClienteModel
from Model.UsuarioModel import UsuarioModel
from db.db_connection import DatabaseConnection
from View.cliente_view import ClienteView
from View.usuario_view import UsuarioView


def on_login_success():
    # Crear la ventana principal después del login
    root = ctk.CTk()  # Nueva ventana para el dashboard principal
    root.title("Gestión de Clientes")
    root.geometry("900x600")  # Ajustado al tamaño utilizado en ClienteView

    # Crear una instancia del modelo y de la vista principal
    cliente_model = ClienteModel(db_connection)
    app = ClienteView(root, cliente_model)

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
        login_view = UsuarioView(root, usuario_model, on_login_success)
        root.mainloop()  # Ejecutar la vista de login

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar la conexión al finalizar
        db_connection.close_connection()
        print("Conexión cerrada")


if __name__ == "__main__":
    main()
