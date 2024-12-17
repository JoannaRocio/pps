import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class SiniestroAgregarView:
    def __init__(self, root, siniestro_model, controller):
        self.root = root
        
        self.siniestro_model = siniestro_model
        self.controller = controller
        

        self.top = ctk.CTkToplevel(self.root)
        self.top.geometry("800x600")
        self.top.title("Agregar Siniestro")
        self.top.config(bg='#2b2b2b')

        # Título
        title = ctk.CTkLabel(self.top, text="Agregar Siniestro", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Campo de búsqueda para el cliente
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.top, textvariable=self.search_var, placeholder_text="Buscar cliente por DNI, nombre o apellido")
        search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")
        search_entry.bind("<KeyRelease>", self.buscar_cliente)

        # Campo de texto para mostrar el cliente seleccionado
        self.cliente_label = ctk.CTkLabel(self.top, text="Cliente seleccionado:", font=('Arial', 14), text_color='white')
        self.cliente_label.grid(row=2, column=0, padx=20, pady=10)

        self.cliente_text = ctk.CTkEntry(self.top, state="readonly")
        self.cliente_text.grid(row=2, column=1, padx=20, pady=10)

        # Campo de texto para seleccionar el vehículo
        self.vehiculo_label = ctk.CTkLabel(self.top, text="Vehículo seleccionado:", font=('Arial', 14), text_color='white')
        self.vehiculo_label.grid(row=3, column=0, padx=20, pady=10)

        self.vehiculo_text = ctk.CTkEntry(self.top, state="readonly")
        self.vehiculo_text.grid(row=3, column=1, padx=20, pady=10)

        # Botón para guardar el siniestro
        guardar_button = ctk.CTkButton(self.top, text="Guardar", command=self.guardar_siniestro)
        guardar_button.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

        # Botón para cerrar la ventana
        close_button = ctk.CTkButton(self.top, text="Cerrar", command=self.top.destroy)
        close_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

    def buscar_cliente(self, event):
        search_term = self.search_var.get().lower()
        clientes = self.siniestro_model.buscar_cliente(search_term)
        
        if clientes:
            # Mostrar la lista de clientes en una lista emergente o en algún widget para selección
            cliente = clientes[0]  # Suponemos que seleccionas el primero
            self.cliente_text.configure(state="normal")
            self.cliente_text.delete(0, "end")
            self.cliente_text.insert(0, f"{cliente[1]} {cliente[2]} ({cliente[3]})")  # Nombre, Apellido, DNI
            self.cliente_text.configure(state="readonly")
            # Aquí podrías cargar los vehículos asociados con el cliente
            self.cargar_vehiculos(cliente[0])  # Asumiendo que el cliente[0] es el cliente_id
        else:
            messagebox.showinfo("Cliente no encontrado", "No se encontró el cliente.")

    def cargar_vehiculos(self, cliente_id):
        vehiculos = self.siniestro_model.obtener_vehiculos(cliente_id)
        # Aquí puedes cargar los vehículos asociados con el cliente
        if vehiculos:
            # Suponemos que el primer vehículo es el seleccionado
            vehiculo = vehiculos[0]
            self.vehiculo_text.configure(state="normal")
            self.vehiculo_text.delete(0, "end")
            self.vehiculo_text.insert(0, f"{vehiculo[1]} - {vehiculo[2]}")  # Vehículo - Patente
            self.vehiculo_text.configure(state="readonly")
        else:
            messagebox.showinfo("Vehículo no encontrado", "No se encontraron vehículos para este cliente.")

    def guardar_siniestro(self):
        cliente_info = self.cliente_text.get()
        vehiculo_info = self.vehiculo_text.get()

        if not cliente_info or not vehiculo_info:
            messagebox.showwarning("Campos incompletos", "Por favor, seleccione un cliente y un vehículo.")
            return

        # Llamar al controlador para guardar el siniestro
        self.controller.guardar_siniestro(cliente_info, vehiculo_info)
       
        self.top.destroy()  
       
   