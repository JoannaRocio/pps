import customtkinter as ctk
from tkinter import messagebox
from Model.SiniestrosModel import SiniestrosModel
from Model.CompaniaModel import CompaniaModel
from Model.ClienteModel import ClienteModel
from Model.UsuarioModel import UsuarioModelo
from Model.VencimientoModel import VencimientosModel
from Model.VehiculoModel import VehiculoModel
from db.db_connection import DatabaseConnection
from Views.Login.login_view import UsuarioView
from Views.Home.home_view import HomeView
from Controller.LoginController import LoginController


import bcrypt
#este es para crear un usuario inicial con usuario y contraseña hasheada
"""def insertar_usuario_inicial(db_connection):
    cursor = db_connection.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:  # Si no hay usuarios en la tabla
        hashed_contrasena = bcrypt.hashpw("1234".encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (usuario, contrasena, primer_ingreso) VALUES (%s, %s, %s)", 
                       ("admin", hashed_contrasena, True))
        db_connection.connection.commit()
        print("Usuario inicial creado.")"""

def on_login_success(id):
    
    root = ctk.CTk()  
    root.title("Sistema de Gestión de Clientes")
    print(f"Login exitoso. ID del usuario: {id}")

    root.update_idletasks()


    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

   
    window_width = 900 
    window_height = 600

    # Calcula la posición x e y para centrar la ventana
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Establece la geometría de la ventana centrada
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Crear la instancia de la conexión a la base de datos y los modelos
    cliente_model = ClienteModel(db_connection)
    compania_model = CompaniaModel(db_connection)
    vencimiento_model = VencimientosModel(db_connection)
    siniestros_model = SiniestrosModel(db_connection)
    vehiculo_model = VehiculoModel(db_connection)       
    

    vista_principal = HomeView(root, cliente_model, compania_model, vencimiento_model, siniestros_model, vehiculo_model)
    
    root.mainloop()


def main():
    global db_connection
    db_connection = DatabaseConnection()
    try:
        db_connection.connect()
        if db_connection.connection and db_connection.connection.is_connected():
            print("Conexión exitosa a la base de datos")

            
            root = ctk.CTk()

            
            usuario_model = UsuarioModelo(db_connection)
            
           # insertar_usuario_inicial(db_connection)

           
            login_controller = LoginController(usuario_model, None, on_login_success)

         
            login_view = UsuarioView(root, login_controller,on_login_success)

        
            login_controller.set_view(login_view)

           
            login_controller.set_view(login_view)

            root.mainloop()  
        else:
            print("No se pudo conectar a la base de datos. Revisa la configuración.")
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    finally:
        if db_connection.connection and db_connection.connection.is_connected():
            db_connection.close_connection()
            print("Conexión cerrada")

if __name__ == "__main__":
    main()
