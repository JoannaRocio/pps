import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry  # Asegúrate de tener instalado tkcalendar
# from Views.Clientes.clientes_view import ClientesView

class HomeView:
    def __init__(self, root, cliente_model, compania_model, siniestros_model , vencimiento_model, vehiculo_model ):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.vehiculo_model = vehiculo_model
   
        
        # self.main_frame = ctk.CTkFrame(self.root)
        # self.main_frame.pack(fill="both", expand=True)

        self.root.geometry("900x600")
        self.root.title("Sistema de Gestión de Clientes")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.clientes_view = None 

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Menú principal", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Configuración de columnas para centrar
        self.main_frame.grid_columnconfigure(0, weight=1)  # Columna izquierda
        self.main_frame.grid_columnconfigure(1, weight=1)  # Columna central (donde estarán los botones)
        self.main_frame.grid_columnconfigure(2, weight=1)  # Columna derecha

        # Botones de funcionalidad centrados en la columna 1
        btn_view = ctk.CTkButton(self.main_frame, text="Cartera", command=self.mostrar_clientes_view, fg_color='#3b3b3b', font=('Arial', 18))
        btn_view.grid(row=1, column=1, pady=30)

        btn_add = ctk.CTkButton(self.main_frame, text="Compañias", command=self.mostrar_companias_view, fg_color='#3b3b3b', font=('Arial', 18))
        btn_add.grid(row=2, column=1, pady=30)
        
        btn_view = ctk.CTkButton(self.main_frame, text="Siniestros", command=self.mostrar_siniestros_view, fg_color='#3b3b3b', font=('Arial', 18))
        btn_view.grid(row=3, column=1, pady=30)

        btn_edit = ctk.CTkButton(self.main_frame, text="Vencimientos", command=self.mostrar_vencimientos_view, fg_color='#3b3b3b', font=('Arial', 18))
        btn_edit.grid(row=4, column=1, pady=30)

        btn_delete = ctk.CTkButton(self.main_frame, text="Cerrar sesión", command=self.cerrar_sesion, fg_color='#3b3b3b', font=('Arial', 18))
        btn_delete.grid(row=5, column=1, pady=30)

    # Función para abrir la vista de Cartera
    # def mostrar_cliente_view(self):
    #     # Oculta el contenido actual de HomeView usando pack_forget() en lugar de destroy()
    #     self.main_frame.pack_forget()

    #     # Asegúrate de pasar el modelo de cliente al instanciar ClienteView
    #     self.cliente_view = ClienteView(self.root, self.cliente_model)  # Pasa el root y el modelo

    def mostrar_clientes_view(self):
        from Views.Clientes.clientes_view import ClientesView
        
        # Oculta el marco principal
        self.main_frame.pack_forget()
        
        # Crea la vista de clientes
        self.clientes_view = ClientesView(self.root, self.cliente_model, self.compania_model, self.vencimiento_model, self.vehiculo_model,  self.siniestros_model, self.volver_menu)
        
        # Muestra el marco de ClientesView
        self.clientes_view.main_frame.pack(fill="both", expand=True)

    def mostrar_companias_view(self): 
        from Views.Companias.companias_view import CompaniasView
        
        # Oculta el marco principal
        self.main_frame.pack_forget()
        
        # Crea la vista de companias
        self.companias_view = CompaniasView(self.root, self.cliente_model, self.compania_model, self.vencimiento_model, self.vehiculo_model, self.siniestros_model , self.volver_menu)
        
        # Muestra el marco de CompaniasView
        self.companias_view.main_frame.pack(fill="both", expand=True)
        
    def mostrar_vencimientos_view(self): 
        from Views.Vencimientos.vencimientos_view import VencimientosView
        
        # Oculta el marco principal
        self.main_frame.pack_forget()
        
        # Crea la vista de clientes
        self.vencimientos_view = VencimientosView(self.root, self.cliente_model, self.compania_model, self.vehiculo_model, self.vencimiento_model, self.siniestros_model, self.volver_menu)
        
        # Muestra el marco de ClientesView
        self.vencimientos_view.main_frame.pack(fill="both", expand=True)
        
    def mostrar_siniestros_view(self): 
        from Views.Siniestros.siniestros_view import SiniestrosView
        
        # Oculta el marco principal
        self.main_frame.pack_forget()
        
        # Crea la vista de clientes
        self.clientes_view = SiniestrosView(self.root, self.cliente_model, self.compania_model, self.vehiculo_model, self.vencimiento_model, self.siniestros_model, self.volver_menu)
        
        # Muestra el marco de ClientesView
        self.clientes_view.main_frame.pack(fill="both", expand=True)
        
    def volver_menu(self):
        if self.clientes_view:  # Verifica si clientes_view existe
            self.clientes_view.main_frame.pack_forget()  # Oculta la vista de clientes
            self.clientes_view = None  # Limpia la referencia a ClientesView
        if self.companias_view:  # Verifica si clientes_view existe
            self.companias_view.main_frame.pack_forget()  # Oculta la vista de clientes
            self.companias_view = None  # Limpia la referencia a ClientesView
        if self.siniestros_view:  # Verifica si clientes_view existe
            self.siniestros_view.main_frame.pack_forget()  # Oculta la vista de clientes
            self.siniestros_view = None  # Limpia la referencia a ClientesView
        if self.vencimientos_view:  # Verifica si clientes_view existe
            self.vencimientos_view.main_frame.pack_forget()  # Oculta la vista de clientes
            self.vencimientos_view = None  # Limpia la referencia a ClientesView
        # Muestra el marco principal de HomeView
        self.main_frame.pack(fill="both", expand=True)
        

    # Función para cerrar sesión
    def cerrar_sesion(self):
        self.root.destroy()

    def open_add_client_window(self):
        # self.client_form_window("Agregar Cliente", None)
        hola = 1

    def open_edit_client_window(self):
        hola = 2
        # selected_item = self.tree.selection()
        # if selected_item:
        #     client_id = self.tree.item(selected_item, 'values')[0]
        #     self.client_form_window("Editar Cliente", client_id)
        # else:
        #     messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")

    # def volver_menu(self):
    #     # Regresar a la vista principal
    #     self.main_frame.pack(fill="both", expand=True)  # Mostrar la vista principal

# Código principal
if __name__ == "__main__":
    root = ctk.CTk()
    menu = HomeView(root)
    root.mainloop()