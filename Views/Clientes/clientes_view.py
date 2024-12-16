import datetime
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from io import BytesIO
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from Views.Home.home_view import HomeView
from Views.Vehiculos.vehiculos_view import VehiculosView

class ClientesView:
    def __init__(self, root, cliente_model, compania_model,vencimiento_model,siniestros_model, vehiculo_model, volver_menu_callback):
        self.root = root
        self.dni_foto = None
        self.foto_licencia = None

        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.vehiculo_model = vehiculo_model
       
        
        self.volver_menu_callback = volver_menu_callback  # Guarda la referencia del método
        self.vehiculos_view = VehiculosView(self.root, self.cliente_model, self.vehiculo_model)

        self.root.geometry("1280x600")
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
        self.search_entry = ctk.CTkEntry(self.main_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        self.search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        search_button = ctk.CTkButton(self.main_frame, text="🔍", command=self.buscar_clientes, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.grid(row=1, column=3, padx=20, pady=10)

        # Tabla para mostrar los clientes
        self.columns = ('ID', 'Nombre', 'Apellido', 'DNI', 'Email', 'Teléfono', 'Fecha de Nacimiento', 'Codigo Postal', 'Domicilio', 'Vencimiento Licencia')
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings', style="Treeview")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Apellido', text='Apellido')
        self.tree.heading('DNI', text='DNI')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Fecha de Nacimiento', text='Fecha de Nacimiento')
        self.tree.heading('Codigo Postal', text='Codigo postal')
        self.tree.heading('Domicilio', text='Domicilio')
        self.tree.heading('Vencimiento Licencia', text='Vencimiento Licencia')
        self.tree.grid(row=2, column=0, columnspan=9, padx=20, pady=10, sticky='nsew')

        # Botones de funcionalidad
        btn_view = ctk.CTkButton(self.main_frame, text="Ver Cliente", command=self.ver_cliente, fg_color='#3b3b3b', font=('Arial', 18))
        btn_view.grid(row=3, column=0, padx=20, pady=10)

        btn_add = ctk.CTkButton(self.main_frame, text="Agregar Cliente", command=self.ventana_agregar, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=3, column=1, padx=20, pady=10)

        btn_edit = ctk.CTkButton(self.main_frame, text="Editar Cliente", command=self.ventana_editar, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=3, column=2, padx=20, pady=10)
        
        boton_carga = ctk.CTkButton(self.main_frame, text="Agregar Vehiculo", command=self.cargar_vehiculo, fg_color='#3b3b3b', font=('Arial', 18))
        boton_carga.grid(row=3, column=3, padx=20, pady=10)

        btn_disable = ctk.CTkButton(self.main_frame, text="Deshabilitar", command=self.deshabilitar_cliente, fg_color='#3b3b3b', font=('Arial', 18))
        btn_disable.grid(row=3, column=4, padx=20, pady=10)

        btn_enable = ctk.CTkButton(self.main_frame, text="Habilitar", command=self.habilitar_cliente, fg_color='#3b3b3b', font=('Arial', 18))
        btn_enable.grid(row=3, column=5, padx=20, pady=10)

        # Configuración del estiramiento de las columnas
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(5):
            self.main_frame.grid_columnconfigure(i, weight=1)

        # Cargar los clientes al inicio
        self.obtener_clientes()

    def cargar_vehiculo(self):
        cli_seleccionado = self.tree.selection()
        if cli_seleccionado:
            client_id = self.tree.item(cli_seleccionado, 'values')[0]  
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)

            if cliente:
                self.vehiculos_view.cargar_vehiculo()
        else:
            messagebox.showwarning("Advertencia", "Primero seleccione un cliente.")      

    
    def volver_menu(self):
        self.main_frame.pack_forget()  # Oculta el marco actual
        self.main_frame = None  # Limpia la referencia al marco actual

        # Crea y muestra la vista del HomeView en la misma ventana
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model, self.vehiculo_model, self.siniestros_model)

    def obtener_clientes(self):
        self.tree.delete(*self.tree.get_children())
        
        self.tree.tag_configure('deshabilitado', background='red', foreground='white')
        self.tree.tag_configure('habilitado', background='white', foreground='black')

        clientes = self.cliente_model.obtener_clientes()
        for cliente in clientes:
            estado = 'deshabilitado' if cliente[10] == 'inactivo' else 'habilitado'
            self.tree.insert('', 'end', values=cliente[:10], tags=(estado,))


    def centrar_ventana(self, ventana):
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = ventana.winfo_screenwidth()
        altura_pantalla = ventana.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        ancho_ventana = 400  # Puedes ajustar el tamaño según lo necesites
        altura_ventana = 550  # Igualmente, ajusta el tamaño de la ventana según lo necesites

        # Calcular las coordenadas para centrar la ventana
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (altura_pantalla - altura_ventana) // 2

        # Posicionar la ventana en el centro
        ventana.geometry(f'{ancho_ventana}x{altura_ventana}+{x}+{y}')


    def ver_cliente(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]  
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)

            if cliente:
                detail_window = Toplevel(self.root)
                detail_window.title("Datos del Cliente")
                detail_window.config(bg='#2b2b2b')
                self.centrar_ventana(detail_window)

                ctk.CTkLabel(detail_window, text="Datos del Cliente", font=('Arial', 18), text_color='white').pack(pady=10)

                keys = ['ID', 'NOMBRE', 'APELIIDO', 'DNI', 'EMAIL', 'TELÉFONO', 'FECHA DE NACIMIENTO', 'CODIGO POSTAL', 'DOMICILIO', 'VENCIMIENTO DE LICENCIA', ]
                for key, value in zip(keys, cliente):
                    ctk.CTkLabel(detail_window, text=f"{key}: {value}", fg_color='#2b2b2b', text_color='white').pack(pady=5)

                # Botón para ver la foto del DNI
                if cliente[10]: 
                    dni_button = ctk.CTkButton(detail_window, text="Ver Foto DNI", command=lambda: self.ver_foto_dni(cliente[10]))
                    dni_button.pack(pady=5)

                # Botón para ver la foto de la Licencia
                if cliente[11]:  
                    licencia_button = ctk.CTkButton(detail_window, text="Ver Foto Licencia", command=lambda: self.ver_foto_licencia(cliente[11]))
                    licencia_button.pack(pady=5)

            else:
                messagebox.showerror("Error", "Cliente no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para ver.")

    def ver_foto_dni(self, foto_dni_bytes):
        foto_dni_window = Toplevel(self.root)
        foto_dni_window.title("Foto del DNI")
        foto_dni_window.config(bg='#2b2b2b')

        dni_image = Image.open(BytesIO(foto_dni_bytes))
        dni_photo = ImageTk.PhotoImage(dni_image)

        dni_label = ctk.CTkLabel(foto_dni_window, image=dni_photo)
        dni_label.image = dni_photo 
        dni_label.pack(pady=10)

    def ver_foto_licencia(self, foto_licencia_bytes):
        foto_licencia_window = Toplevel(self.root)
        foto_licencia_window.title("Foto de la Licencia")
        foto_licencia_window.config(bg='#2b2b2b')

        licencia_image = Image.open(BytesIO(foto_licencia_bytes))
        licencia_photo = ImageTk.PhotoImage(licencia_image)

        licencia_label = ctk.CTkLabel(foto_licencia_window, image=licencia_photo)
        licencia_label.image = licencia_photo
        licencia_label.pack(pady=10)

    def ventana_agregar(self):
        self.ventana_cliente("Agregar Cliente", None)
        
    def ventana_editar(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.ventana_cliente("Editar Cliente", client_id)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

    def ventana_cliente(self, title, client_id):
        form_window = Toplevel(self.root)
        form_window.title(title)
        form_window.config(bg='#2b2b2b') 
        self.centrar_ventana(form_window)
        form_window.grab_set()
        
        # Campos del formulario (sin cambios)
        ctk.CTkLabel(form_window, text="Nombre", fg_color='#2b2b2b', text_color='white').grid(row=0, column=0, padx=10, pady=10)
        nombre = ctk.CTkEntry(form_window)
        nombre.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Apellido", fg_color='#2b2b2b', text_color='white').grid(row=1, column=0, padx=10, pady=10)
        apellido = ctk.CTkEntry(form_window)
        apellido.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="DNI", fg_color='#2b2b2b', text_color='white').grid(row=2, column=0, padx=10, pady=10)
        dni = ctk.CTkEntry(form_window)
        dni.grid(row=2, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_window, text="Email", fg_color='#2b2b2b', text_color='white').grid(row=3, column=0, padx=10, pady=10)
        email = ctk.CTkEntry(form_window)
        email.grid(row=3, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_window, text="Teléfono", fg_color='#2b2b2b', text_color='white').grid(row=4, column=0, padx=10, pady=10)
        telefono = ctk.CTkEntry(form_window)
        telefono.grid(row=4, column=1, padx=10, pady=10)

        ctk.CTkLabel(form_window, text="Fecha de nacimiento", fg_color='#2b2b2b', text_color='white').grid(row=5, column=0, padx=10, pady=10)
        fecha_nacimiento = DateEntry(form_window, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        fecha_nacimiento.grid(row=5, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_window, text="Código Postal", fg_color='#2b2b2b', text_color='white').grid(row=6, column=0, padx=10, pady=10)
        cp = ctk.CTkEntry(form_window)
        cp.grid(row=6, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_window, text="Domicilio", fg_color='#2b2b2b', text_color='white').grid(row=7, column=0, padx=10, pady=10)
        domicilio = ctk.CTkEntry(form_window)
        domicilio.grid(row=7, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(form_window, text="Vencimiento de Licencia", fg_color='#2b2b2b', text_color='white').grid(row=8, column=0, padx=10, pady=10)
        vencimiento_licencia = DateEntry(form_window, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        vencimiento_licencia.grid(row=8, column=1, padx=10, pady=10)

        # Botones para cargar imágenes de DNI y Licencia
        dni_foto_button = ctk.CTkButton(
            form_window, text="Cargar Foto DNI", 
            command=lambda: self.cargar_dni_foto(form_window)
        )
        dni_foto_button.grid(row=9, column=0, padx=10, pady=10)

        licencia_foto_button = ctk.CTkButton(
            form_window, text="Cargar Foto Licencia", 
            command=lambda: self.cargar_foto_licencia(form_window)
        )
        licencia_foto_button.grid(row=9, column=1, padx=10, pady=10)

        # Verificar si estamos editando un cliente existente (si client_id está disponible)
        if client_id:
            cliente = self.cliente_model.obtener_cliente_por_id(client_id)
            if cliente:
                nombre.insert(0, cliente[1])
                apellido.insert(0, cliente[2])
                dni.insert(0, cliente[3])
                email.insert(0, cliente[4])
                telefono.insert(0, cliente[5])
                fecha_nacimiento.insert(0, cliente[6])
                cp.insert(0, cliente[7])
                domicilio.insert(0, cliente[8])
                vencimiento_licencia.insert(0, cliente[9])

            # Verificar imágenes
            self.dni_foto = self.dni_foto if hasattr(self, 'dni_foto') else None
            self.foto_licencia = self.foto_licencia if hasattr(self, 'foto_licencia') else None

            # Cambiar el texto del botón a "Editar"
            boton_guardar = ctk.CTkButton(
                form_window, text="Editar",
                command=lambda: self.editar_cliente(
                    client_id,  # Pasar client_id aquí
                    form_window, nombre.get(), apellido.get(), dni.get(), email.get(), telefono.get(),
                    fecha_nacimiento.get_date(), cp.get(), domicilio.get(), vencimiento_licencia.get_date(),
                    self.dni_foto, self.foto_licencia
                )
            )
        else:
            # Si no hay client_id, el comportamiento será crear un nuevo cliente
            boton_guardar = ctk.CTkButton(
                form_window, text="Guardar",
                command=lambda: self.crear_cliente(
                    form_window, nombre.get(), apellido.get(), dni.get(), email.get(), telefono.get(),
                    fecha_nacimiento.get_date(), cp.get(), domicilio.get(), vencimiento_licencia.get_date(),
                    self.dni_foto, self.foto_licencia
                )
            )

        boton_guardar.grid(row=10, column=0, columnspan=2, pady=20)
        
    def crear_cliente(self, form_window, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia):
        """Crea un nuevo cliente y guarda los datos, incluyendo las fotos opcionales."""
        if not nombre or not apellido or not dni or not email or not telefono:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            # Validación de las fotos
            if dni_foto is None or foto_licencia is None:
                messagebox.showwarning("Advertencia", "Se agrego cliente sin fotos")

            # Convertir las imágenes a bytes si son objetos Image
            dni_foto_bytes = self.cliente_model.convertir_imagen_a_bytes(dni_foto) if isinstance(dni_foto, Image.Image) else dni_foto
            foto_licencia_bytes = self.cliente_model.convertir_imagen_a_bytes(foto_licencia) if isinstance(foto_licencia, Image.Image) else foto_licencia

            # Crear el cliente
            creado = self.cliente_model.agregar_cliente(
                nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto_bytes, foto_licencia_bytes
            )
            if creado:
                messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")

            form_window.destroy()  # Cerrar ventana
            self.obtener_clientes()  # Recargar clientes

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el cliente: {str(e)}")




    def editar_cliente(self, client_id, form_window, nombre, apellido, dni, email, telefono, fecha_nacimiento, cp, domicilio, vencimiento_licencia, dni_foto, foto_licencia):
        """Edita un cliente existente y actualiza sus datos, incluyendo las fotos opcionales."""
        if not nombre or not apellido or not dni or not email or not telefono:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos obligatorios.")
            return

        try:
            
             # Convertir las imágenes a bytes si son objetos Image
            dni_foto_bytes = self.cliente_model.convertir_imagen_a_bytes(dni_foto) if isinstance(dni_foto, Image.Image) else dni_foto
            foto_licencia_bytes = self.cliente_model.convertir_imagen_a_bytes(foto_licencia) if isinstance(foto_licencia, Image.Image) else foto_licencia

            # Llamar a la función de editar del modelo para actualizar el cliente
            self.cliente_model.editar_cliente(
                client_id=client_id,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                cp=cp,
                domicilio=domicilio,
                vencimiento_licencia=vencimiento_licencia,
                dni_foto=dni_foto_bytes,
                foto_licencia=foto_licencia_bytes,
            )
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")  # Mostrar mensaje siempre al editar

            form_window.destroy()  # Cerrar ventana
            self.obtener_clientes()  # Recargar clientes

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al editar el cliente: {str(e)}")

        
    def convertir_imagen_a_bytes(self, imagen):
        if imagen:
            img = Image.open(imagen)
            byte_array = BytesIO()
            img.save(byte_array, format='PNG')  # o el formato que necesites
            return byte_array.getvalue()
        return None
    
    
    def cargar_dni_foto(self, form_window):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
            if file_path:
                self.dni_foto = Image.open(file_path)
                if self.dni_foto.mode != 'RGB':
                    self.dni_foto = self.dni_foto.convert('RGB')
                messagebox.showinfo("Éxito", "Foto de DNI cargada correctamente.", parent=form_window)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}", parent=form_window)

    def cargar_foto_licencia(self, form_window):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
            if file_path:
                self.foto_licencia = Image.open(file_path)
                if self.foto_licencia.mode != 'RGB':
                    self.foto_licencia = self.foto_licencia.convert('RGB')
                messagebox.showinfo("Éxito", "Foto de Licencia cargada correctamente.", parent=form_window)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}", parent=form_window)

    def buscar_clientes(self):
        search_term = self.search_entry.get().lower()
        # Limpiar el Treeview antes de insertar nuevos resultados
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Llamar al método buscar_clientes pasando el término de búsqueda
        resultados = self.cliente_model.buscar_clientes(search_term)
        
        for cliente in resultados:
            # Insertar el cliente encontrado en el Treeview
            self.tree.insert('', 'end', values=cliente)
    
    def habilitar_cliente(self):
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.cliente_model.habilitar_cliente(client_id)
            self.obtener_clientes()
            messagebox.showinfo("Éxito", "Cliente habilitado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una compañía para habilitar.")


    def deshabilitar_cliente(self):     
        selected_item = self.tree.selection()
        if selected_item:
            client_id = self.tree.item(selected_item, 'values')[0]
            self.cliente_model.deshabilitar_cliente(client_id)
            self.obtener_clientes()
            messagebox.showinfo("Éxito", "Cliente deshabilitado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para deshabilitar.")
                
