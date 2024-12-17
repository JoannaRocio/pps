import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from PIL import Image, ImageTk
import io
import tempfile

class DetalleSiniestroView:
    def __init__(self, root, siniestro, volver_func):
        self.root = root
        self.siniestro = siniestro
        self.volver_func = volver_func

        self.top_detalle = ctk.CTkToplevel(self.root)
        self.top_detalle.title("Detalles del Siniestro")

        if self.siniestro is None:
            messagebox.showerror("Error", "No se encontró el siniestro.")
            return 
        
        self.mostrar_detalle()

    def mostrar_detalle(self):
        """Muestra los detalles del siniestro en una nueva ventana emergente."""
        label_detalle = ctk.CTkLabel(self.top_detalle, text=f"ID: {self.siniestro['id']}")
        label_detalle.pack(padx=10, pady=10)

        label_cliente = ctk.CTkLabel(self.top_detalle, text=f"Cliente: {self.siniestro['nombre']}")
        label_cliente.pack(padx=10, pady=10)

        label_fecha = ctk.CTkLabel(self.top_detalle, text=f"Fecha: {self.siniestro['fecha_inicio_siniestro']}")
        label_fecha.pack(padx=10, pady=10)

        label_descripcion = ctk.CTkLabel(self.top_detalle, text=f"Descripción: {self.siniestro['descripcion']}")
        label_descripcion.pack(padx=10, pady=10)
        
        label_descripcion = ctk.CTkLabel(self.top_detalle, text=f"Estado: {self.siniestro['estado']}")
        label_descripcion.pack(padx=10, pady=10)
       
        
        btn_pdf = ctk.CTkButton(self.top_detalle, text="Ver PDF", command=self.ver_pdf)
        btn_pdf.pack(padx=10, pady=10)

        btn_imagenes = ctk.CTkButton(self.top_detalle, text="Ver Imágenes", command=self.ver_imagenes)
        btn_imagenes.pack(padx=10, pady=10)

        
        btn_volver = ctk.CTkButton(self.top_detalle, text="Volver", command=self.volver_func)
        btn_volver.pack(padx=10, pady=10)


    def ver_pdf(self):
        pdf_data = self.siniestro.get('archivo')
        if not pdf_data:
            print("No hay PDF disponible.")
            return
        
        try:
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf_data)
                temp_file_path = temp_file.name  
            
            webbrowser.open(temp_file_path)
            print(f"PDF abierto correctamente: {temp_file_path}")
        except Exception as e:
            print(f"Error al abrir el PDF: {e}")

   
    def ver_imagenes(self):
        img_data = self.siniestro.get('imagenes')
        if not img_data:
            print("No hay imágenes disponibles.")
            return
        
        # Abrir la imagen
        from PIL import Image
        import io

        img = Image.open(io.BytesIO(img_data))
        img.show()  # Mostrar la imagen
