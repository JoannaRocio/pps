import customtkinter as ctk
from tkinter import messagebox

class UsuarioView:
    def __init__(self, root, usuario_model, on_login_success):
        self.root = root
        self.usuario_model = usuario_model
        self.on_login_success = on_login_success
        self.root.title("Iniciar Sesión")
        self.root.geometry("400x300")
        self.center_window()
        
        # Campos de inicio de sesión
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Usuario")
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", self.on_enter_pressed) #acepta el enter
        
        self.password_entry = ctk.CTkEntry(self.root, show='*', placeholder_text="Contraseña")
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", self.on_enter_pressed) #acepta el enter
        
        login_button = ctk.CTkButton(self.root, text="Iniciar Sesión", command=self.login)
        login_button.pack(pady=20)
        
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 400  # Ancho de la ventana
        window_height = 300  # Alto de la ventana

        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
        
    def on_enter_pressed(self, event):
        # Llama a la función de login cuando se presiona Enter en cualquiera de los campos
        self.login()
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.usuario_model.verificar_credenciales(username, password):
            self.root.destroy() # Cierra la ventana de login
            self.on_login_success()  # Llama a la función de éxito
            # self.root.destroy()  # Cierra la ventana de login
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")
