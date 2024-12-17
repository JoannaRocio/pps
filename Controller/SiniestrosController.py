# controller.py

from Views.Siniestros.agregar_siniestro_view import AgregarSiniestroView
from tkinter import messagebox

class SiniestroController:
    def __init__(self,siniestro_model,cliente_model,vehiculo_model,view):
       
        self.siniestro_model = siniestro_model
        self.cliente_model = cliente_model
        self.vehiculo_model = vehiculo_model
        self.view = view
        
    def obtener_conexion(self):
        if not self.connection or self.connection.closed:
            self.connection = self.db_connection()  # Asegúrate de reabrir la conexión si está cerrada
        return self.connection

    def guardar_siniestro(self, cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo):
        """Llamar al modelo para guardar el siniestro."""
        self.siniestro_model.guardar_siniestro(cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo)

                
    def mostrar_siniestros(self):
            """
            Obtiene los siniestros del modelo y los pasa a la vista.
            """
            try:
                siniestros = self.siniestro_model.obtener_siniestros() or []  # Obtener siniestros del modelo
                
                if not siniestros:  # Si no hay siniestros
                    from tkinter import messagebox
                    messagebox.showinfo("Sin Siniestros", "No hay siniestros registrados.")
                else:
                    # Pasar los datos a la vista para actualizarlos en el Treeview
                    self.view.actualizar_siniestro(siniestros)
            except Exception as e:
                print(f"Error al obtener siniestros: {e}")
                from tkinter import messagebox
                messagebox.showerror("Error", "Hubo un problema al obtener los siniestros.")


    def obtener_detalle_siniestro(self, siniestro_id):
        """Método que obtiene los detalles de un siniestro dado su ID."""
        siniestro = self.siniestro_model.obtener_siniestro_por_id(siniestro_id)
        return siniestro
    
    
    def buscar_clientes(self, search_term):
        return self.cliente_model.obtener_clientes_sinestro(search_term)

    def cargar_vehiculos(self, cliente_id):
        return self.vehiculo_model.cargar_vehiculos_por_cliente(cliente_id)

    def guardar_siniestro(self, cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo):
        self.siniestro_model.guardar_siniestro(cliente_nombre, vehiculo_id, estado, descripcion, fecha_inicio, imagenes, archivo)

    def mostrar_agregar_siniestro(self, root, volver_func):
        # Aquí el controlador crea la vista y le pasa los parámetros
        agregar_siniestro_view = AgregarSiniestroView(
            root, 
            volver_func, 
            self,  # Pasar el controlador para la comunicación entre vista y controlador
            self.siniestro_model, 
            self.cliente_model, 
            self.vehiculo_model
        )
