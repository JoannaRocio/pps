import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView

class VencimientosView:
    def __init__(self, root, cliente_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.volver_menu_callback = volver_menu_callback  # Guarda la referencia del método

        self.root.geometry("900x600")
        self.root.title("Gestión de Vencimientos")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Vencimientos", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')


        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)

    def volver_menu(self):
        # Cierra la ventana actual
        self.root.destroy()  
        # Crea una nueva instancia de la ventana principal
        main_window = ctk.CTk()  
        # Instancia del menú principal
        menu = HomeView(main_window, self.cliente_model)  # Asegúrate de pasar el cliente_model
        main_window.mainloop()  # Comienza el ciclo principal
