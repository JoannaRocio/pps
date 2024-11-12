import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk, Toplevel
from tkcalendar import DateEntry
from Views.Home.home_view import HomeView
from tkinter import ttk

class VencimientosView:
    def __init__(self, root, cliente_model, compania_model, vencimiento_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.volver_menu_callback = volver_menu_callback  # Guarda la referencia del método

        # Configuración de la ventana
        self.root.geometry("900x600")
        self.root.title("Próximos Vencimientos")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Vencimientos", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.main_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        search_button = ctk.CTkButton(self.main_frame, text="🔍", command=self.buscarCliente, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.grid(row=1, column=3, padx=20, pady=10)
        
        # Creamos la tabla de vencimientos (Treeview)
        self.treeview = ttk.Treeview(self.main_frame, columns=("Nombre", "Apellido", "Patente", "Fecha de Licencia", "Fecha de Póliza"), show="headings")
        
        # Configuramos las columnas
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Apellido", text="Apellido")
        self.treeview.heading("Patente", text="Patente")
        self.treeview.heading("Fecha de Licencia", text="Fecha de Licencia")
        self.treeview.heading("Fecha de Póliza", text="Fecha de Póliza")
        
        self.treeview.grid(row=2, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")

        # Hacer que la tabla sea "expandible"
        self.main_frame.grid_rowconfigure(2, weight=1)  # La fila de la tabla debe ocupar el máximo espacio
        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)  # Las columnas de la tabla se expanden
            
        self.ver_vencimientos()
        
    def ver_vencimientos(self):
        self.treeview.delete(*self.treeview.get_children())  # Limpiar la tabla
        vencimientos = self.vencimiento_model.mostrar_vencimientos()  # Asegúrate de que este método retorna clientes ordenados
        for cliente in sorted(vencimientos, key=lambda x: (x[1], x[2])):  # Ordenar por nombre y apellido
            self.treeview.insert('', 'end', values=cliente)

    def buscarCliente(self):
        """
        Función de búsqueda. Filtra los clientes según el texto ingresado en el campo de búsqueda.
        """
        search_term = self.search_var.get().lower()  # Obtener término de búsqueda en minúsculas

        # Limpiar la tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Ejemplo de búsqueda (esto se puede hacer más dinámico según tu base de datos)
        vencimientos_data = [
            ("Juan", "Pérez", "NULL", "NULL"),
            ("María", "González", "NULL", "NULL"),
            ("Carlos", "Rodríguez", "NULL", "NULL"),
            ("Laura", "Martínez", "NULL", "NULL"),
        ]

        # Filtrar y volver a insertar solo los que coinciden con la búsqueda
        for data in vencimientos_data:
            if any(search_term in str(field).lower() for field in data):
                self.treeview.insert("", "end", values=data)

    def volver_menu(self):
        # Cierra la ventana actual
        self.root.destroy()  
        # Crea una nueva instancia de la ventana principal
        main_window = ctk.CTk()  
        # Instancia del menú principal
        menu = HomeView(main_window, self.cliente_model, self.compania_model, self.vencimiento_model)  # Asegúrate de pasar el cliente_model
        main_window.mainloop()  # Comienza el ciclo principal

# Uso de la clase (en otro archivo, cuando se crea la vista)
if __name__ == "__main__":
    root = ctk.CTk()
    # Asumiendo que 'cliente_model' es un modelo de datos real.
    cliente_model = None  # Aquí deberías pasar tu modelo de cliente real
    vencimientos_view = VencimientosView(root, cliente_model, lambda: print("Volviendo al menú principal"))
    root.mainloop()
