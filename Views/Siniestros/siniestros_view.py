import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView
import tkinter as tk
from tkinter import *
from tkinter import ttk

class SiniestrosView:
    def __init__(self, root, cliente_model, compania_model, vencimiento_model, volver_menu_callback):
        
        # Mock de datos
        mock_data = [
            ("ABC123", "Toyota Corolla", "García", "Juan", "12345678", "Pendiente"),
            ("DEF456", "Ford Fiesta", "López", "María", "87654321", "Resuelto"),
            ("GHI789", "Chevrolet Onix", "Pérez", "Carlos", "11223344", "Pendiente"),
            ("JKL012", "Renault Clio", "Martínez", "Ana", "44332211", "Resuelto")
        ]

        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.volver_menu_callback = volver_menu_callback

        self.root.geometry("900x600")
        self.root.title("Gestión de Siniestros")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Siniestros", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')

        # Tabla para mostrar los Siniestros
        self.columns = ('Patente', 'Vehículo', 'Apellido', 'Nombre', 'DNI', 'Estado')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('Patente', text='Patente')
        self.tree.heading('Vehículo', text='Vehículo')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Estado', text='Estado')
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky='nsew')

        # Cambia el ancho según sea necesario
        self.tree.column('Patente', minwidth=50, width=100)  
        self.tree.column('Vehículo', minwidth=50, width=150) 
        self.tree.column('Apellido', minwidth=50, width=100)  
        self.tree.column('Nombre', minwidth=50, width=100)   
        self.tree.column('DNI', minwidth=50, width=80)
        self.tree.column('Estado', minwidth=50, width=100)  
        
        # Configurar los tags para colores para los estados
        self.tree.tag_configure('Pendiente', background='white', foreground='red')
        self.tree.tag_configure('Resuelto', background='white', foreground='green')

        # Insertar los datos mock en la tabla y aplicar colores
        for item in mock_data:
            estado = item[5]  # El estado está en la posición 5 del array
            if estado == "Pendiente":
                self.tree.insert("", "end", values=item, tags=('Pendiente',))
            elif estado == "Resuelto":
                self.tree.insert("", "end", values=item, tags=('Resuelto',))
            else:
                self.tree.insert("", "end", values=item)  # Sin etiqueta de color
        
        # # Crear la tabla (usar grid para organizarlos)
        # self.show_table(mock_data)

        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)
        
    def show_table(self, mock_data):
        # Crear la tabla (usar grid para organizarlos)
        for r, item in enumerate(mock_data):
            for c, value in enumerate(item):
                if c == 5:  # Columna "Estado"
                    # Si el estado es "Pendiente", color rojo; si "Resuelto", verde
                    color = 'red' if value == 'Pendiente' else 'green'
                    b = Entry(self.root, text=value, foreground=color, width=20)
                    b.grid(row=r, column=c)
                else:
                    # Las demás celdas tendrán el color por defecto
                    b = Entry(self.root, text=value, width=20)
                    b.grid(row=r, column=c)
        
                # Tabla para mostrar los Siniestros
        self.columns = ('Patente', 'Vehículo', 'Apellido', 'Nombre', 'DNI', 'Estado')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('Patente', text='Patente')
        self.tree.heading('Vehículo', text='Vehículo')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Estado', text='Estado')
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=20, sticky='nsew')

        # Cambia el ancho según sea necesario
        self.tree.column('Patente', minwidth=50, width=100)  
        self.tree.column('Vehículo', minwidth=50, width=150) 
        self.tree.column('Apellido', minwidth=50, width=100)  
        self.tree.column('Nombre', minwidth=50, width=100)   
        self.tree.column('DNI', minwidth=50, width=80)
        self.tree.column('Estado', minwidth=50, width=100)  
        
        # Configurar los tags para colores para los estados
        self.tree.tag_configure('Pendiente', foreground='red')
        self.tree.tag_configure('Resuelto', foreground='green')


    def volver_menu(self):
        self.main_frame.pack_forget()  # Oculta el marco actual
        self.main_frame = None  # Limpia la referencia al marco actual

        # Crea y muestra la vista del HomeView en la misma ventana
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model)