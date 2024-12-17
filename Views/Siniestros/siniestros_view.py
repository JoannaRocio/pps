import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk
from Controller.SiniestrosController import SiniestroController
from PIL import Image, ImageTk
import io

from Views.Siniestros.agregar_siniestro_view import AgregarSiniestroView
from Views.Siniestros.detalle_siniestro_view import DetalleSiniestroView


class SiniestrosView:
    def __init__(self, root, cliente_model, compania_model, vencimiento_model, siniestros_model, vehiculo_model, volver_menu):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.vehiculo_model = vehiculo_model
        self.controller = SiniestroController(siniestros_model,cliente_model,vehiculo_model, self)
        self.volver_menu = volver_menu
        
        self.selected_siniestro_id = None
        
        
        # Configuración de la ventana principal
        self.root.geometry("1200x700")
        self.root.title("Gestión de Siniestros")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

         # Título
        title = ctk.CTkLabel(self.main_frame, text="Siniestro", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=6, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='w')
        
         # Campo de búsqueda y botones
        search_frame = ctk.CTkFrame(self.main_frame, fg_color='#2b2b2b')
        search_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10, sticky='ew')

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        search_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)

        search_button = ctk.CTkButton(search_frame, text="🔍", command=self.buscarCliente, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.pack(side='left', padx=(0, 10))

        """Crea botones para funcionalidades: Agregar, Editar y Cambiar Estado."""
        btn_add = ctk.CTkButton(self.main_frame, text="Agregar", command=self.agregar_siniestro, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=3, column=0, padx=20, pady=10)

        btn_edit = ctk.CTkButton(self.main_frame, text="Editar", command=self.editar_siniestro, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=3, column=1, padx=20, pady=10)

        btn_estado = ctk.CTkButton(self.main_frame, text="Cambiar Estado", command=self.cambiar_estado_siniestro, fg_color='#3b3b3b', font=('Arial', 18))
        btn_estado.grid(row=3, column=2, padx=20, pady=10)
        
        btn_estado = ctk.CTkButton(self.main_frame, text="Ver Detalle", command=self.ver_detalle_siniestro, fg_color='#3b3b3b', font=('Arial', 18))
        btn_estado.grid(row=3, column=2, padx=20, pady=10)

     # Creamos la tabla de vencimientos (Treeview)
        self.treeview = ttk.Treeview(self.main_frame, columns=("id","Patente", "Vehículo",  "Apellido","Nombre", "DNI", "Sitio Web", "Estado"), show="headings")

        # Configura las columnas
        self.treeview.heading("id", text="id")
        self.treeview.heading("Patente", text="Patente")
        self.treeview.heading("Vehículo", text="Vehículo")
        self.treeview.heading("Apellido", text="Apellido")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("DNI", text="DNI")
        self.treeview.heading("Sitio Web", text="Sitio Web")
        self.treeview.heading("Estado", text="Estado")

        # Configura el tamaño de las columnas
        self.treeview.column("id", width=30)
        self.treeview.column("Patente", width=100)
        self.treeview.column("Vehículo", width=150)
        self.treeview.column("Apellido", width=100)
        self.treeview.column("Nombre", width=100)
        self.treeview.column("DNI", width=120)
        self.treeview.column("Sitio Web", width=200)
        self.treeview.column("Estado", width=120)

        # Coloca el treeview en la interfaz
        self.treeview.grid(row=2, column=0, columnspan=7, padx=20, pady=20, sticky="nsew")

        # Configuración de la fila y columnas para que el treeview se expanda
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(7):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(6):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.treeview.bind("<Double-1>", self.abrir_sitio_web)
        self.treeview.bind("<ButtonRelease-1>", self.seleccionar_siniestro)
        
        self.controller.mostrar_siniestros()
     
     
     
 # ------------------------------ buscador de Siniestro------------------------------
    def buscarCliente(self):
        """Lógica para buscar clientes."""
        search_term = self.search_var.get().lower()
        print(f"Buscar cliente: {search_term}")
        

 # ------------------------------ Cargar las tablas Siniestro------------------------------        
    def actualizar_siniestro(self, siniestros):
            """
            Actualiza los siniestros en el Treeview.
            :param siniestros: Lista de siniestros como tuplas.
            """
            self.treeview.delete(*self.treeview.get_children())  

            for siniestro in siniestros:
                # Inserta cada siniestro como una fila en el Treeview
                self.treeview.insert('', 'end', values=(
                    siniestro[0],
                    siniestro[8],  # vehiculo_patente
                    siniestro[9],  # vehiculo_nombre
                    siniestro[10], #clietne nombre
                    siniestro[11], #cliente apellido
                    siniestro[12],  # cliente_dni
                    siniestro[14],  # compania_nombre
                    siniestro[2]   # siniestro_estado
                ))

    # ------------------------------ es para ver detalle Siniestro------------------------------
    def seleccionar_siniestro(self, event):
        """Método para capturar el siniestro seleccionado en el treeview."""
        selected_item = self.treeview.selection()  
        if selected_item:
            siniestro_id = self.treeview.item(selected_item[0])["values"][0]  
            self.selected_siniestro_id = siniestro_id  
            print(f"Siniestro seleccionado con ID: {siniestro_id}")
            

    def ver_detalle_siniestro(self):
        """Abre una ventana emergente para ver los detalles del siniestro seleccionado."""
        if not self.selected_siniestro_id:
            messagebox.showinfo("Error", "Debe seleccionar un siniestro.")
            return
        
        # Llamamos al controlador para obtener los detalles del siniestro
        siniestro = self.controller.obtener_detalle_siniestro(self.selected_siniestro_id)

        if siniestro:
            # Crear la vista de detalle con el siniestro seleccionado
            DetalleSiniestroView(self.root, siniestro, self.volver_menu)
        else:
            messagebox.showinfo("Error", "No se encontró el siniestro con ID seleccionado.")
            
            
            
     # ------------------------------ Agregar siniestro------------------------------   
    def agregar_siniestro (self):

        self.controller.mostrar_agregar_siniestro(self.root, self.volver_menu)




    def editar_siniestro(self):
        """Permite editar el siniestro seleccionado."""
        print("Editar siniestro seleccionado.")
        # Lógica para editar un siniestro


    def cambiar_estado_siniestro(self):
        """Cambia el estado del siniestro seleccionado."""
        print("Cambiar estado del siniestro.")
        # Lógica para cambiar el estado y actualizar la tabla


    def abrir_sitio_web(self, event):
        """Abre el sitio web asociado al siniestro (doble clic en la tabla)."""
        print("Abrir sitio web asociado al siniestro.")
        # Lógica para abrir URL del sitio web


    def volver_menu(self):
        self.volver_menu()  
        self.main_frame.pack_forget()  
        
        
if __name__ == "__main__":
    root = ctk.CTk()
    cliente_model = None  
    
    siniestro_view = SiniestrosView(root, cliente_model, None, None, None, None, lambda: print("Volviendo al menú principal"))
    root.mainloop()
