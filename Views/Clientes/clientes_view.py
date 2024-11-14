import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView

class ClientesView:
    def __init__(self, root, cliente_model, compania_model, siniestros_model, vencimiento_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.volver_menu_callback = volver_menu_callback  # Guarda la referencia del método

        self.root.geometry("900x600")
        self.root.title("Gestión de Clientes")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Gestión de Clientes", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.main_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        search_button = ctk.CTkButton(self.main_frame, text="🔍", command=self.search_clients, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.grid(row=1, column=3, padx=20, pady=10)

        # Tabla para mostrar los clientes
        self.columns = ('ID', 'Nombre', 'Apellido', 'Teléfono', 'DNI')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('DNI', text='DNI')
        self.tree.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky='nsew')

        # Botones de funcionalidad
        btn_view = ctk.CTkButton(self.main_frame, text="Ver Cliente", command=self.view_client, fg_color='#3b3b3b', font=('Arial', 18))
        btn_view.grid(row=3, column=0, padx=20, pady=10)

        btn_add = ctk.CTkButton(self.main_frame, text="Agregar Cliente", command=self.open_add_client_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=3, column=1, padx=20, pady=10)

        btn_edit = ctk.CTkButton(self.main_frame, text="Editar Cliente", command=self.open_edit_client_window, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=3, column=2, padx=20, pady=10)

        btn_delete = ctk.CTkButton(self.main_frame, text="Eliminar Cliente", command=self.delete_client, fg_color='#3b3b3b', font=('Arial', 18))
        btn_delete.grid(row=3, column=3, padx=20, pady=10)

        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # Cargar los clientes al inicio
        self.load_clients()

    def volver_menu(self):
        self.main_frame.pack_forget()  # Oculta el marco actual
        self.main_frame = None  # Limpia la referencia al marco actual

        # Crea y muestra la vista del HomeView en la misma ventana
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model, self.siniestros_model)

    def load_clients(self):
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla
        clientes = self.cliente_model.obtener_clientes()  # Asegúrate de que este método retorna clientes ordenados
        for cliente in sorted(clientes, key=lambda x: (x[1], x[2])):  # Ordenar por nombre y apellido
            self.tree.insert('', 'end', values=cliente)

    def view_client(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)

            if cliente:
                detail_window = Toplevel(self.root)
                detail_window.title("Detalles del Cliente")
                detail_window.config(bg='#2b2b2b')

                ctk.CTkLabel(detail_window, text="Detalles del Cliente", font=('Arial', 18), text_color='white').pack(pady=10)

                keys = ['Nombre', 'Apellido', 'Teléfono', 'DNI', 'Dirección', 'Email', 'Fecha de Nacimiento']
                for key, value in zip(keys, cliente):
                    ctk.CTkLabel(detail_window, text=f"{key}: {value}", fg_color='#2b2b2b', text_color='white').pack(pady=5)
            else:
                messagebox.showerror("Error", "Cliente no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para ver.")

    def open_add_client_window(self):
        self.client_form_window("Agregar Cliente", None)

    def open_edit_client_window(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.client_form_window("Editar Cliente", client_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

    def client_form_window(self, title, client_id):
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.config(bg='#2b2b2b')

        # Campos del formulario
        ctk.CTkLabel(form_window, text="Nombre", fg_color='#2b2b2b', text_color='white').grid(row=0, column=0, padx=10, pady=10)
        name_entry = ctk.CTkEntry(form_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Apellido", fg_color='#2b2b2b', text_color='white').grid(row=1, column=0, padx=10, pady=10)
        surname_entry = ctk.CTkEntry(form_window)
        surname_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Teléfono", fg_color='#2b2b2b', text_color='white').grid(row=2, column=0, padx=10, pady=10)
        phone_entry = ctk.CTkEntry(form_window)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="DNI", fg_color='#2b2b2b', text_color='white').grid(row=3, column=0, padx=10, pady=10)
        dni_entry = ctk.CTkEntry(form_window)
        dni_entry.grid(row=3, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Dirección", fg_color='#2b2b2b', text_color='white').grid(row=4, column=0, padx=10, pady=10)
        address_entry = ctk.CTkEntry(form_window)
        address_entry.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Email", fg_color='#2b2b2b', text_color='white').grid(row=5, column=0, padx=10, pady=10)
        email_entry = ctk.CTkEntry(form_window)
        email_entry.grid(row=5, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Fecha de Nacimiento", fg_color='#2b2b2b', text_color='white').grid(row=6, column=0, padx=10, pady=10)
        dob_entry = DateEntry(form_window, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        dob_entry.grid(row=6, column=1, padx=10, pady=10)

        if client_id:  # Si es edición, cargar datos existentes
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)
            if cliente:  # Verifica que el cliente existe
                name_entry.insert(0, cliente[1])  # Asumiendo que los índices corresponden a los datos
                surname_entry.insert(0, cliente[2])
                phone_entry.insert(0, cliente[3])
                dni_entry.insert(0, cliente[4])
                address_entry.insert(0, cliente[5])
                email_entry.insert(0, cliente[6])
                dob_entry.set_date(cliente[7])  # Fecha de nacimiento

        save_button = ctk.CTkButton(form_window, text="Guardar", command=lambda: self.save_client(client_id, name_entry.get(), surname_entry.get(), phone_entry.get(), dni_entry.get(), address_entry.get(), email_entry.get(), dob_entry.get()))
        save_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

    def save_client(self, client_id, name, surname, phone, dni, address, email, dob):
        if client_id:  # Si existe, actualizar
            self.cliente_model.editar_cliente(client_id, name, surname, phone, dni, address, email, dob)
        else:  # Si no, crear nuevo
            self.cliente_model.agregar_cliente(name, surname, phone, dni, address, email, dob)
        self.load_clients()  # Recargar la lista de clientes
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")

    def delete_client(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.cliente_model.eliminar_cliente(client_id)
            self.load_clients()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

    def search_clients(self):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        clientes = self.cliente_model.obtener_clientes()
        for cliente in clientes:
            if search_term in cliente[1].lower() or search_term in cliente[2].lower():
                self.tree.insert('', 'end', values=cliente)
