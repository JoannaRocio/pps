import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView

class CompaniasView:
    def __init__(self, root, cliente_model, compania_model, siniestros_model, vehiculo_model, vencimiento_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.vehiculo_model = vehiculo_model
        self.siniestros_model = siniestros_model
        self.volver_menu_callback = volver_menu_callback

        self.root.geometry("900x600")
        self.root.title("Gestión de Compañías")
        self.root.config(bg='#2b2b2b')

        # Configuración de estilo para Treeview
        style = ttk.Style()
        style.configure("Treeview", foreground="black", background="white")  # Color por defecto para filas activas
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), foreground="white", background='#3b3b3b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Compañías", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')

        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.main_frame, textvariable=self.search_var, placeholder_text="Buscar compañía")
        search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        search_button = ctk.CTkButton(self.main_frame, text="🔍", command=self.search_companies, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.grid(row=1, column=3, padx=20, pady=10)

        # Tabla para mostrar las compañías
        self.columns = ('ID', 'Nombre', 'Sitio_web')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Sitio_web', text='Sitio web')
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky='nsew')

        # Configura el evento de doble clic después de definir `self.tree`
        self.tree.bind("<Double-1>", self.open_website_link)  # Evento de doble clic en la tabla

        # Botones de funcionalidad
        btn_add = ctk.CTkButton(self.main_frame, text="Agregar", command=self.open_add_company_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=3, column=0, padx=20, pady=10)

        btn_edit = ctk.CTkButton(self.main_frame, text="Editar", command=self.open_edit_company_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=3, column=1, padx=20, pady=10)

        btn_delete = ctk.CTkButton(self.main_frame, text="Deshabilitar", command=self.disable_company, fg_color='#3b3b3b', font=('Arial', 18))
        btn_delete.grid(row=3, column=2, padx=20, pady=10)

        btn_enable = ctk.CTkButton(self.main_frame, text="Habilitar", command=self.enable_company, fg_color='#3b3b3b', font=('Arial', 18))
        btn_enable.grid(row=3, column=3, padx=20, pady=10)


        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # Cargar las compañías al inicio
        self.obtener_companias()

    def obtener_companias(self):
        """Carga las compañías en la tabla"""
        self.tree.delete(*self.tree.get_children())
        
        # Configuración del estilo para compañías deshabilitadas
        self.tree.tag_configure('disabled', background='red', foreground='white')
        self.tree.tag_configure('enabled', background='white', foreground='black')

        companias = self.compania_model.obtener_companias()
        for compania in companias:
            # Verificar el estado y asignar el tag correspondiente
            estado = 'disabled' if compania[3] == 'inactivo' else 'enabled'  # compania[3] es el campo `estado`
            self.tree.insert('', 'end', values=compania[:3], tags=(estado,))


    def volver_menu(self):
        self.main_frame.pack_forget()  # Oculta el marco actual
        self.main_frame = None  # Limpia la referencia al marco actual

        # Crea y muestra la vista del HomeView en la misma ventana
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model, self.siniestros_model, self.vehiculo_model)

    def open_add_company_window(self):
        """Abre la ventana para agregar una nueva compañía"""
        self.company_form_window("Agregar Compañía", None)

    def open_edit_company_window(self):
        """Abre la ventana para editar una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            company_id = self.tree.item(selected_item, 'values')[0]
            self.company_form_window("Editar Compañía", company_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para editar.")

    def company_form_window(self, title, company_id):
        """Crea la ventana para agregar o editar una compañía"""
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.config(bg='#2b2b2b')

        # Campos del formulario
        ctk.CTkLabel(form_window, text="Nombre", fg_color='#2b2b2b', text_color='white').grid(row=0, column=0, padx=10, pady=10)
        name_entry = ctk.CTkEntry(form_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Sitio web", fg_color='#2b2b2b', text_color='white').grid(row=1, column=0, padx=10, pady=10)
        website_entry = ctk.CTkEntry(form_window)
        website_entry.grid(row=1, column=1, padx=10, pady=10)

        if company_id:
            compania = self.compania_model.obtener_compania_por_id(company_id)
            if compania:
                name_entry.insert(0, compania[1])
                website_entry.insert(0, compania[2])

        save_button = ctk.CTkButton(form_window, text="Guardar", command=lambda: self.save_company(company_id, name_entry.get(), website_entry.get()))
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def save_company(self, company_id, name, website):
        """Guarda la compañía en la base de datos (agregar o editar)"""
        if company_id:
            self.compania_model.editar_compania(company_id, name, website)
        else:
            self.compania_model.agregar_compania(name, website)
        self.obtener_companias()
        messagebox.showinfo("Éxito", "Compañía guardada correctamente.")
    

    def enable_company(self):
        """Habilita una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            company_id = self.tree.item(selected_item, 'values')[0]
            self.compania_model.habilitar_compania(company_id)
            self.obtener_companias()
            messagebox.showinfo("Éxito", "Compañía habilitada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para habilitar.")


    def disable_company(self):
        """Deshabilita una compañía seleccionada"""
        selected_item = self.tree.selection()
        if selected_item:
            company_id = self.tree.item(selected_item, 'values')[0]
            self.compania_model.deshabilitar_compania(company_id)
            self.obtener_companias()
            messagebox.showinfo("Éxito", "Compañía deshabilitada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para deshabilitar.")


    def search_companies(self):
        """Filtra las compañías según el término de búsqueda"""
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        companias = self.compania_model.buscar_companias(search_term)
        for compania in companias:
            estado = 'disabled' if compania[3] == 'inactivo' else 'enabled'  # compania[3] es el campo `estado`
            self.tree.insert('', 'end', values=compania[:3], tags=(estado,))
    
    
    def open_website_link(self, event):
        """Abre el sitio web de la compañía seleccionada en el navegador"""
        selected_item = self.tree.selection()
        if selected_item:
            sitio_web = self.tree.item(selected_item, 'values')[2]  # Obtiene la URL de la columna 'Sitio_web'
            
            # Verifica si el campo de sitio_web no está vacío
            if sitio_web:
                webbrowser.open(sitio_web)  # Abre la URL en el navegador
            else:
                messagebox.showinfo("Información", "Esta compañía no tiene un sitio web registrado.")