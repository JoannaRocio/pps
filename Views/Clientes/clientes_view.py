import datetime
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from io import BytesIO
from PIL import Image
from tkinter import filedialog
from Views.Home.home_view import HomeView

class ClientesView:
    def __init__(self, root, cliente_model, compania_model, vencimiento_model, vehiculo_model, siniestros_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vehiculo_model = vehiculo_model
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
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model, self.vehiculo_model, self.siniestros_model)

    def load_clients(self):
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla
        clientes = self.cliente_model.obtener_clientes()  # Asegúrate de que este método retorna clientes ordenados
        for cliente in sorted(clientes, key=lambda x: (x[1], x[2])):  # Ordenar por nombre y apellido
            self.tree.insert('', 'end', values=cliente)

    def view_client(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]  # Cambiado de 'id_cliente' a 'id'
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
            client_id = self.tree.item(selected_item, 'values')[0]  # Cambiado de 'id_cliente' a 'id'
            self.client_form_window("Editar Cliente", client_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

    def client_form_window(self, title, client_id):
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.config(bg='#2b2b2b')

        # Campos del formulario (sin cambios)
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
        
        ctk.CTkLabel(form_window, text="Código Postal", fg_color='#2b2b2b', text_color='white').grid(row=4, column=0, padx=10, pady=10)
        cp_entry = ctk.CTkEntry(form_window)
        cp_entry.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Email", fg_color='#2b2b2b', text_color='white').grid(row=5, column=0, padx=10, pady=10)
        email_entry = ctk.CTkEntry(form_window)
        email_entry.grid(row=5, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Fecha de vencimiento", fg_color='#2b2b2b', text_color='white').grid(row=6, column=0, padx=10, pady=10)
        vencimiento_entry = DateEntry(form_window, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        vencimiento_entry.grid(row=6, column=1, padx=10, pady=10)
        
        # ctk.CTkLabel(form_window, text="Fecha vencimiento", fg_color='#2b2b2b', text_color='white').grid(row=4, column=0, padx=10, pady=10)
        # vencimiento_entry = ctk.CTkEntry(form_window)
        # vencimiento_entry.grid(row=4, column=1, padx=10, pady=10)

        # Botones para cargar imágenes de DNI y Licencia
        dni_foto_button = ctk.CTkButton(form_window, text="Cargar Foto DNI", command=self.cargar_dni_foto)
        dni_foto_button.grid(row=7, column=0, padx=10, pady=10)

        licencia_foto_button = ctk.CTkButton(form_window, text="Cargar Foto Licencia", command=self.cargar_foto_licencia)
        licencia_foto_button.grid(row=7, column=1, padx=10, pady=10)

        # Cargar datos si es edición
        if client_id:
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)
            if cliente:
                name_entry.insert(0, cliente[1])
                surname_entry.insert(0, cliente[2])
                dni_entry.insert(0, cliente[3])
                email_entry.insert(0, cliente[4])
                phone_entry.insert(0, cliente[5])
                cp_entry.insert(0, cliente[6])
                address_entry.insert(0, cliente[7])
                vencimiento_entry.insert(0, cliente[8])
                # dob_entry.set_date(cliente[9])

        # Botón de guardar
        save_button = ctk.CTkButton(
            form_window, text="Guardar",
            # nombre, apellido, dni, email, telefono, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado
            command=lambda: self.save_client(
                client_id, name_entry.get(), surname_entry.get(), dni_entry.get(), email_entry.get(), phone_entry.get(), cp_entry.get(),
                address_entry.get(), vencimiento_entry.get()
            )
        )
        save_button.grid(row=8, column=0, columnspan=2, padx=10, pady=20)

    def save_client(self, client_id, name, surname, dni, email, phone, cp, address, vencimiento_licencia):
        # Convertir imágenes a bytes
        dni_foto_data = self.convertir_imagen_a_bytes(self.dni_foto) if self.dni_foto else None
        foto_licencia_data = self.convertir_imagen_a_bytes(self.foto_licencia) if self.foto_licencia else None
        
        # vencimiento_licencia = "2000-01-02"

        
# nombre, apellido, dni, email, telefono, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia, estado
        # Guardar o actualizar el cliente
        if client_id:
            self.cliente_model.editar_cliente(client_id, name, surname, dni, email, phone, cp, address, vencimiento_licencia, dni_foto_data, foto_licencia_data)
        else:
            self.cliente_model.agregar_cliente(name, surname, phone, dni, email, phone, cp, address, vencimiento_licencia, dni_foto_data, foto_licencia_data)

        # Recargar lista y notificar
        self.load_clients()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")

    def convertir_imagen_a_bytes(self, imagen):
        if imagen:
            img = Image.open(imagen)
            byte_array = BytesIO()
            img.save(byte_array, format='PNG')  # o el formato que necesites
            return byte_array.getvalue()
        return None
    
    def cargar_dni_foto(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.dni_foto = Image.open(file_path)

    def cargar_foto_licencia(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.foto_licencia = Image.open(file_path)

    def convertir_imagen_a_bytes(self, imagen):
        byte_io = BytesIO()
        imagen.save(byte_io, format="JPEG")
        return byte_io.getvalue()
    
    def search_clients(self):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        clientes = self.cliente_model.obtener_clientes()
        for cliente in clientes:
            if search_term in cliente[1].lower() or search_term in cliente[2].lower():
                self.tree.insert('', 'end', values=cliente)
                
    def delete_client(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.cliente_model.eliminar_cliente(client_id)
            self.load_clients()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

