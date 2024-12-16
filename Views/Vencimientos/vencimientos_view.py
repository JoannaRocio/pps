# views/vencimientos_view.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from Controller.VencimientosController import VencimientosController
from Views.Home.home_view import HomeView

class VencimientosView:
    def __init__(self, root, cliente_model, compania_model,vencimiento_model, siniestros_model, vehiculo_model, volver_menu_callback):
        self.root = root
        self.cliente_model = cliente_model
        self.compania_model = compania_model
        self.vencimiento_model = vencimiento_model
        self.siniestros_model = siniestros_model
        self.vehiculo_model = vehiculo_model
        
        self.controller = VencimientosController(vencimiento_model, self)

        
        self.volver_menu_callback = volver_menu_callback 

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
        back_button.grid(row=0, column=0, padx=20, pady=20, sticky='ne')
        
        # Campo de búsqueda
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(self.main_frame, textvariable=self.search_var, placeholder_text="Buscar cliente")
        search_entry.grid(row=1, column=0, padx=20, pady=10, columnspan=3, sticky="ew")

        search_button = ctk.CTkButton(self.main_frame, text="🔍", command=self.buscar_cliente, fg_color='#3b3b3b', font=('Arial', 18))
        search_button.grid(row=1, column=3, padx=20, pady=10)

        # Botón "Próximos Vencimientos"
        notificaciones_button = ctk.CTkButton(self.main_frame, text="Próximos Vencimientos", command=self.mostrar_notificaciones, fg_color='#3b3b3b', font=('Arial', 18))
        notificaciones_button.grid(row=1, column=4, padx=20, pady=10)
        
        # Creamos la tabla de vencimientos (Treeview)
        self.treeview = ttk.Treeview(self.main_frame, columns=("Nombre", "Apellido", "Patente", "Fecha de Licencia", "Fecha de Póliza", "Compania", "Sitio Web"), show="headings")

        # Configuramos las columnas
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Apellido", text="Apellido")
        self.treeview.heading("Patente", text="Patente")
        self.treeview.heading("Fecha de Licencia", text="Fecha de Licencia")
        self.treeview.heading("Fecha de Póliza", text="Fecha de Póliza")
        self.treeview.heading("Compania", text="Compania")
        self.treeview.heading("Sitio Web", text="Sitio Web")

        self.treeview.grid(row=2, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

        # Hacer que la tabla sea "expandible"
        self.main_frame.grid_rowconfigure(2, weight=1)  # La fila de la tabla debe ocupar el máximo espacio
        for i in range(6):
            self.main_frame.grid_columnconfigure(i, weight=1)  # Las columnas de la tabla se expanden

        self.treeview.bind("<Double-1>", self.abrir_sitio_web)

        self.controller.ver_vencimientos()
        
    def actualizar_vencimientos(self, vencimientos):
        self.treeview.delete(*self.treeview.get_children())  # Limpiar la tabla
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

    def mostrar_notificaciones(self, proximos_vencimientos):
        if proximos_vencimientos:
            notificaciones = "\n".join([f"{v[0]} {v[1]}: {v[2]} (Fecha de Licencia: {v[3]}, Fecha de Póliza: {v[4]})" for v in proximos_vencimientos])
            messagebox.showinfo("Próximos Vencimientos", notificaciones)
        else:
            messagebox.showinfo("Próximos Vencimientos", "No hay vencimientos próximos en los próximos 15 días.")

    def volver_menu(self):
        self.main_frame.pack_forget()  # Oculta el marco actual
        self.main_frame = None  # Limpia la referencia al marco actual

        # Crea y muestra la vista del HomeView en la misma ventana
        menu = HomeView(self.root, self.compania_model, self.cliente_model, self.vencimiento_model, self.vehiculo_model, self.siniestros_model)


if __name__ == "__main__":
    root = ctk.CTk()
    cliente_model = None  
    vencimientos_view = VencimientosView(root, cliente_model, lambda: print("Volviendo al menú principal"))
    root.mainloop()
