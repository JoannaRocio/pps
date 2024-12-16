# views/vencimientos_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from Controller.VencimientosController import VencimientosController
from Views.Home.home_view import HomeView

class VencimientosView:
    def __init__(self, root, cliente_model, compania_model, vencimiento_model, siniestros_model, vehiculo_model, volver_menu):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.vehiculo_model = vehiculo_model
        
        self.controller = VencimientosController(vencimiento_model, self)
        self.volver_menu = volver_menu

        # Configuración de la ventana
        self.root.geometry("1200x700")
        self.root.title("Próximos Vencimientos")
        self.root.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Vencimientos", font=('Arial', 24), text_color='white')
        title.grid(row=0, column=0, columnspan=6, padx=20, pady=20)

        # Botón "Volver"
        back_button = ctk.CTkButton(self.main_frame, text="Volver", command=self.volver_menu, fg_color='#3b3b3b', font=('Arial', 18))
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='w')
        
        # Campo de búsqueda y botones
        search_frame = ctk.CTkFrame(self.main_frame, fg_color='#2b2b2b')
        search_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10, sticky='ew')

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        search_entry.pack(side='left', padx=(0, 10), fill='x', expand=True)

        search_button = ctk.CTkButton(search_frame, text="🔍", command=self.buscar_cliente, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.pack(side='left', padx=(0, 10))

        notificaciones_button = ctk.CTkButton(search_frame, text="Próximos Vencimientos", command=self.mostrar_notificaciones, fg_color='#3b3b3b', font=('Arial', 18))
        notificaciones_button.pack(side='left')

        # Creamos la tabla de vencimientos (Treeview)
        self.treeview = ttk.Treeview(self.main_frame, columns=("Nombre", "Apellido",  "Fecha de Licencia","Patente", "Fecha de Póliza", "Compania", "Sitio Web"), show="headings")

        # Configuramos las columnas
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Apellido", text="Apellido")
        self.treeview.heading("Patente", text="Patente")
        self.treeview.heading("Fecha de Licencia", text="Fecha de Licencia")
        self.treeview.heading("Fecha de Póliza", text="Fecha de Póliza")
        self.treeview.heading("Compania", text="Compania")
        self.treeview.heading("Sitio Web", text="Sitio Web")

        self.treeview.column("Nombre", width=100)
        self.treeview.column("Apellido", width=100)
        self.treeview.column("Patente", width=120)
        self.treeview.column("Fecha de Licencia", width=120)
        self.treeview.column("Fecha de Póliza", width=120)
        self.treeview.column("Compania", width=150)
        self.treeview.column("Sitio Web", width=200)

        self.treeview.grid(row=2, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

      
        self.main_frame.grid_rowconfigure(2, weight=1)
        for i in range(6):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.treeview.bind("<Double-1>", self.abrir_sitio_web)

        self.controller.ver_vencimientos()
        
    def actualizar_vencimientos(self, vencimientos):
        self.treeview.delete(*self.treeview.get_children())
        for cliente in vencimientos:
            self.treeview.insert('', 'end', values=cliente)

    def buscar_cliente(self):
        search_term = self.search_var.get().lower()
        self.controller.buscar_cliente(search_term)

    def abrir_sitio_web(self, event):
        selected_item = self.treeview.selection()[0]
        sitio_web = self.treeview.item(selected_item, "values")[6]
        self.controller.abrir_sitio_web(sitio_web)

    def mostrar_notificaciones_sin_parametros(self):
        self.controller.mostrar_notificaciones()

    def mostrar_notificaciones(self, proximos_vencimientos=None):
        if proximos_vencimientos is None:
            proximos_vencimientos = []
            
        if proximos_vencimientos:
            notificaciones = "\n".join([f"{v[0]} {v[1]}: {v[2]} (Fecha de Licencia: {v[3]}, Fecha de Póliza: {v[4]})" for v in proximos_vencimientos])
            messagebox.showinfo("Próximos Vencimientos", notificaciones)
        else:
            messagebox.showinfo("Próximos Vencimientos", "No hay vencimientos próximos en los próximos 15 días.")

    def volver_menu(self):
        self.volver_menu()  
        self.main_frame.pack_forget()  

#h
if __name__ == "__main__":
    root = ctk.CTk()
    cliente_model = None  
    vencimientos_view = VencimientosView(root, cliente_model, None, None, None, None, lambda: print("Volviendo al menú principal"))
    root.mainloop()
