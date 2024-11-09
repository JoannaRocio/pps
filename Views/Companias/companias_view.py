import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView

class CompaniasView:
    def __init__(self, root, cliente_model, compania_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.volver_menu_callback = volver_menu_callback

        self.root.geometry("900x600")
        self.root.title("Gestión de Compañías")
        self.root.config(bg='#2b2b2b')

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

        # Botones de funcionalidad
        btn_add = ctk.CTkButton(self.main_frame, text="Agregar Compañía", command=self.open_add_company_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=3, column=0, padx=20, pady=10)

        btn_edit = ctk.CTkButton(self.main_frame, text="Editar Compañía", command=self.open_edit_company_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=3, column=1, padx=20, pady=10)

        btn_delete = ctk.CTkButton(self.main_frame, text="Eliminar Compañía", command=self.delete_company, fg_color='#3b3b3b', font=('Arial', 18))
        btn_delete.grid(row=3, column=2, padx=20, pady=10)

        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # Cargar las compañías al inicio
        self.obtener_companias()

    def obtener_companias(self):
        self.tree.delete(*self.tree.get_children())
        companias = self.compania_model.obtener_companias()
        print(companias)
        for compania in companias:
            self.tree.insert('', 'end', values=compania)

    def volver_menu(self):
        self.root.destroy()
        main_window = ctk.CTk()
        menu = HomeView(main_window, self.compania_model, self.cliente_model)
        main_window.mainloop()

    def open_add_company_window(self):
        self.company_form_window("Agregar Compañía", None)

    def open_edit_company_window(self):
        selected_item = self.tree.selection()
        if selected_item:
            company_id = self.tree.item(selected_item, 'values')[0]
            self.company_form_window("Editar Compañía", company_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para editar.")

    def company_form_window(self, title, company_id):
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
        if company_id:
            self.compania_model.editar_compania(company_id, name, website)
        else:
            self.compania_model.agregar_compania(name, website)
        self.load_companies()
        messagebox.showinfo("Éxito", "Compañía guardada correctamente.")

    def delete_company(self):
        selected_item = self.tree.selection()
        if selected_item:
            company_id = self.tree.item(selected_item, 'values')[0]
            self.compania_model.eliminar_compania(company_id)
            self.load_companies()
            messagebox.showinfo("Éxito", "Compañía eliminada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para eliminar.")

    def search_companies(self):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        companias = self.compania_model.obtener_companias()
        for compania in companias:
            if search_term in compania[1].lower() or search_term in compania[2].lower():
                self.tree.insert('', 'end', values=compania)
