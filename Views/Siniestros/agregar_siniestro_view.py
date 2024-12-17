import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry


class AgregarSiniestroView:
    def __init__(self, root, volver_func, controller, siniestro_model, cliente_model, vehiculo_model):
        self.root = root
        self.volver_func = volver_func
        self.controller = controller
        self.siniestro_model = siniestro_model
        self.cliente_model = cliente_model
        self.vehiculo_model = vehiculo_model
        
        self.cliente_data = {}
        self.vehiculo_data = {}
        self.imagenes_var = []
        self.archivo_pdf = None

        
        
        self.agregar_siniestro()
        
    def agregar_siniestro(self):
        self.top = ctk.CTkToplevel(self.root)
        self.top.title("Agregar Siniestro")
        self.top.geometry("600x600")  
        
        frame = ctk.CTkFrame(self.top)
        frame.pack(fill="both", expand=True, padx=30, pady=30)  

        # Buscador de cliente
        self.search_cliente_var = ctk.StringVar()
        ctk.CTkEntry(frame, textvariable=self.search_cliente_var, placeholder_text="Buscar Cliente por DNI").pack(pady=10)  # Añadir espaciado
        ctk.CTkButton(frame, text="Buscar Cliente", command=self.buscar_cliente).pack(pady=10)  

        # Dropdown de clientes
        self.cliente_dropdown = ctk.CTkComboBox(frame, values=[], state="readonly")
        self.cliente_dropdown.pack(pady=10)  

        # Botón para cargar vehículos
        ctk.CTkButton(frame, text="Cargar Vehículos", command=self.cargar_vehiculos).pack(pady=10)  
        self.vehiculo_dropdown = ctk.CTkComboBox(frame, values=[], state="readonly")
        self.vehiculo_dropdown.pack(pady=10)  

        # Descripción del siniestro
        self.descripcion_entry = ctk.CTkEntry(frame, placeholder_text="Descripción del Siniestro")
        self.descripcion_entry.pack(pady=10)  

        # Fecha de inicio
        self.fecha_inicio_var = ctk.StringVar()
        DateEntry(frame, textvariable=self.fecha_inicio_var, date_pattern='yyyy-mm-dd').pack(pady=10)  

        # Botón para cargar PDF
        ctk.CTkButton(frame, text="Cargar PDF", command=self.cargar_pdf).pack(pady=10)  

        # Botón para guardar siniestro
        ctk.CTkButton(frame, text="Guardar", command=self.guardar_siniestro).pack(pady=20)  

    def buscar_cliente(self):
        search_term = self.search_cliente_var.get()
        clientes = self.controller.buscar_clientes(search_term)
        if clientes:
            cliente_textos = [f"{c[1]} {c[2]} ({c[3]})" for c in clientes]
            self.cliente_data = {f"{c[1]} {c[2]} ({c[3]})": c[0] for c in clientes}
            self.cliente_dropdown.configure(values=cliente_textos)
        else:
            messagebox.showinfo("Error", "No se encontraron clientes.")

    def cargar_vehiculos(self):
        cliente_id = self.cliente_data.get(self.cliente_dropdown.get())
        vehiculos = self.controller.cargar_vehiculos(cliente_id)
        if vehiculos:
            vehiculo_textos = [f"{v[1]} - {v[2]}" for v in vehiculos]
            self.vehiculo_data = {f"{v[1]} - {v[2]}": v[0] for v in vehiculos}
            self.vehiculo_dropdown.configure(values=vehiculo_textos)
        else:
            messagebox.showinfo("Error", "No se encontraron vehículos.")

    def cargar_pdf(self):
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        with open(pdf_file, 'rb') as pdf:
            self.archivo_pdf = pdf.read()

    def guardar_siniestro(self):
        cliente_nombre = self.cliente_dropdown.get()
        vehiculo_id = self.vehiculo_data.get(self.vehiculo_dropdown.get())
        descripcion = self.descripcion_entry.get()
        fecha_inicio = self.fecha_inicio_var.get()
        estado = "Pendiente"

        from Controller.SiniestrosController import SiniestroController
        
        self.controller = SiniestroController(self.siniestro_model, self.cliente_model, self.vehiculo_model, self)
        
        self.controller.guardar_siniestro(cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, b''.join(self.imagenes_var), self.archivo_pdf)
        messagebox.showinfo("Éxito", "Siniestro guardado correctamente.")
        self.top.destroy()
