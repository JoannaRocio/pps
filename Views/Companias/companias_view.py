import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView
from Model.CompaniaModel import CompaniaModel

class CompaniasView:
    def __init__(self, root, cliente_model, compania_model, siniestros_model, vehiculo_model, vencimiento_model, volver_menu):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.vehiculo_model = vehiculo_model
        self.siniestros_model = siniestros_model
        self.volver_menu = volver_menu

        self.root.geometry("900x600")
        self.root.title("Gestión de Compañías")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.ventana = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.ventana.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.ventana, text="Compañías", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        boton_volver = ctk.CTkButton(self.ventana, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        boton_volver.grid(row=0, column=0, padx=20, pady=20, sticky='ne')

        # Campo de búsqueda
        self.campo_busqueda = ctk.StringVar()
        campo_busqueda = ctk.CTkEntry(self.ventana, textvariable=self.campo_busqueda, placeholder_text="Buscar compañía")
        campo_busqueda.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        boton_busqueda = ctk.CTkButton(self.ventana, text="🔍", command=self.buscar_compañias, fg_color='#3b3b3b', font=('Arial', 18))
        boton_busqueda.grid(row=1, column=3, padx=20, pady=10)

        # Tabla para mostrar las compañías
        self.columns = ('ID', 'Nombre', 'Sitio_web')
        self.tree = ttk.Treeview(self.ventana, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Sitio_web', text='Sitio web')
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky='nsew')

        # Configura el evento de doble clic después de definir `self.tree`
        self.tree.bind("<Double-1>", self.link_url)  # Evento de doble clic en la tabla

        # Botones de funcionalidad
        boton_agregar = ctk.CTkButton(self.ventana, text="Agregar", command=self.cargar_nueva, fg_color='#3b3b3b', font=('Arial', 18))
        boton_agregar.grid(row=3, column=0, padx=20, pady=10)

        boton_editar = ctk.CTkButton(self.ventana, text="Editar", command=self.ventana_editar, fg_color='#3b3b3b', font=('Arial', 18))
        boton_editar.grid(row=3, column=1, padx=20, pady=10)

        boton_deshabilitar = ctk.CTkButton(self.ventana, text="Deshabilitar", command=self.deshabilitar, fg_color='#3b3b3b', font=('Arial', 18))
        boton_deshabilitar.grid(row=3, column=2, padx=20, pady=10)

        boton_habilitar = ctk.CTkButton(self.ventana, text="Habilitar", command=self.habilitar, fg_color='#3b3b3b', font=('Arial', 18))
        boton_habilitar.grid(row=3, column=3, padx=20, pady=10)


        # Configuración del estiramiento de las columnas
        self.ventana.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.ventana.grid_columnconfigure(i, weight=1)

        # Cargar las compañías al inicio
        self.obtener_companias()

    def obtener_companias(self):
        self.tree.delete(*self.tree.get_children())
        
        self.tree.tag_configure('disabled', background='red', foreground='white')
        self.tree.tag_configure('enabled', background='white', foreground='black')

        companias = self.compania_model.obtener_companias()
        for compania in companias:
            # Verificar el estado y asigna el tag correspondiente
            estado = 'disabled' if compania[3] == 'inactivo' else 'enabled'  # compania[3] es el campo `estado`
            self.tree.insert('', 'end', values=compania[:3], tags=(estado,))

    def cerrar_vista_companias(self):
        self.view.destroy()  # O eliminar la vista de alguna otra manera
        self.controller = None  # Eliminar controlador viejo

    def cerrar_conexion(self):
        self.db_connection.close()  # Asegúrate de cerrar la conexión

    
    def volver_menu(self):
        self.volver_menu()  
        self.ventana.pack_forget()  

    def cargar_nueva(self):
        """Abre la ventana para agregar una nueva compañía"""
        self.ventana_nueva_compania("Agregar Compañía", None)

    def ventana_editar(self):
        """Abre la ventana para editar una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            compania_id = self.tree.item(selected_item, 'values')[0]
            self.ventana_nueva_compania("Editar Compañía", compania_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para editar.")

    def ventana_nueva_compania(self, title, compania_id):
        """Crea la ventana para agregar o editar una compañía"""
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.config(bg='#2b2b2b')

        # Campos del formulario
        ctk.CTkLabel(form_window, text="Nombre", fg_color='#2b2b2b', text_color='white').grid(row=0, column=0, padx=10, pady=10)
        campo_nombre = ctk.CTkEntry(form_window)
        campo_nombre.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Sitio web", fg_color='#2b2b2b', text_color='white').grid(row=1, column=0, padx=10, pady=10)
        campo_url = ctk.CTkEntry(form_window)
        campo_url.grid(row=1, column=1, padx=10, pady=10)

        if compania_id:
            compania = self.compania_model.obtener_compania_por_id(compania_id)
            if compania:
                campo_nombre.insert(0, compania[1])
                campo_url.insert(0, compania[2])

        save_button = ctk.CTkButton(form_window, text="Guardar", command=lambda: self.guardar(form_window, compania_id, campo_nombre.get(), campo_url.get()))
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def guardar(self, form_window, compania_id, nombre, sitio_web):
        """Guarda la compañía en la base de datos (agregar o editar)"""
        if not nombre.strip() or not sitio_web.strip():
            messagebox.showerror("Error", "El nombre y el sitio web son obligatorios.")
            return
        
        if compania_id:
            self.compania_model.editar_compania(compania_id, nombre, sitio_web)
        else:
            self.compania_model.agregar_compania(nombre, sitio_web)
            
        form_window.destroy()
        self.obtener_companias()
        messagebox.showinfo("Éxito", "Compañía guardada correctamente.")
    

    def habilitar(self):
        """Habilita una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            compania_id = self.tree.item(selected_item, 'values')[0]
            self.compania_model.habilitar_compania(compania_id)
            self.obtener_companias()
            messagebox.showinfo("Éxito", "Compañía habilitada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para habilitar.")


    def deshabilitar(self):
        """Deshabilita una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            compania_id = self.tree.item(selected_item, 'values')[0]
            self.compania_model.deshabilitar_compania(compania_id)
            self.obtener_companias()
            messagebox.showinfo("Éxito", "Compañía deshabilitada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para deshabilitar.")


    def buscar_compañias(self):
        """Filtra las compañías según el término de búsqueda"""
        search_term = self.campo_busqueda.get().lower()
        self.tree.delete(*self.tree.get_children())
        companias = self.compania_model.buscar_companias(search_term)
        for compania in companias:
            estado = 'disabled' if compania[3] == 'inactivo' else 'enabled'  # compania[3] es el campo `estado`
            self.tree.insert('', 'end', values=compania[:3], tags=(estado,))
    
    
    def link_url(self, event):
        """Abre el sitio web de la compañía seleccionada en el navegador"""
        selected_item = self.tree.selection()
        if selected_item:
            sitio_web = self.tree.item(selected_item, 'values')[2]
            if sitio_web:
                webbrowser.open(sitio_web)  # Abre la URL en el navegador
            else:
                messagebox.showinfo("Información", "Esta compañía no tiene un sitio web registrado.")