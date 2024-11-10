import customtkinter as ctk
from tkinter import messagebox

class UsuarioView:
    def __init__(self, root, usuario_model, on_login_success):
        self.root = root
        self.usuario_model = usuario_model
        self.on_login_success = on_login_success
        self.root.title("Iniciar Sesión")
        self.root.geometry("400x300")

        # Campos de inicio de sesión
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="Usuario")
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", self.on_enter_pressed) #acepta el enter
        
        self.password_entry = ctk.CTkEntry(self.root, show='*', placeholder_text="Contraseña")
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", self.on_enter_pressed) #acepta el enter
        login_button = ctk.CTkButton(self.root, text="Iniciar Sesión", command=self.login)
        login_button.pack(pady=20)
        
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
