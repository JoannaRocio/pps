# Views/Vehiculos/vehiculos_view.py
import tkinter as tk
from tkinter import ttk, Toplevel
import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox

class VehiculosView:
    def __init__(self, root, cliente_model, vehiculo_model):
        self.root = root
        self.cliente_model = cliente_model
        self.vehiculo_model = vehiculo_model
    
    def abrir_ventana_vehiculo(self):
        self.cargar_vehiculo("Agregar Vehiculo")
        
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
    
    def cargar_vehiculo(self, titulo):
        
                form_window = tk.Toplevel(self.root)
                form_window.title(titulo)
                form_window.config(bg='#2b2b2b') 
                
                self.centrar_ventana(form_window)
                
                años = [str(year) for year in range(1995, 2031)]

                ctk.CTkLabel(form_window, text="Marca", fg_color='#2b2b2b', text_color='white').grid(row=0, column=0, padx=10, pady=10)
                marca = ctk.CTkEntry(form_window)
                marca.grid(row=0, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Modelo", fg_color='#2b2b2b', text_color='white').grid(row=1, column=0, padx=10, pady=10)
                modelo = ctk.CTkEntry(form_window)
                modelo.grid(row=1, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Año", fg_color='#2b2b2b', text_color='white').grid(row=2, column=0, padx=10, pady=10)
                año = ttk.Combobox(form_window, values=años, state="readonly")
                año.grid(row=2, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Patente", fg_color='#2b2b2b', text_color='white').grid(row=3, column=0, padx=10, pady=10)
                patente = ctk.CTkEntry(form_window)
                patente.grid(row=3, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Compañia", fg_color='#2b2b2b', text_color='white').grid(row=4, column=0, padx=10, pady=10)
                compañia = ttk.Combobox(form_window)
                compañia.grid(row=4, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Tipo de Vehiculo", fg_color='#2b2b2b', text_color='white').grid(row=5, column=0, padx=10, pady=10)
                tVehiculo = ctk.CTkEntry(form_window)
                tVehiculo.grid(row=5, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Categoria Seguro", fg_color='#2b2b2b', text_color='white').grid(row=6, column=0, padx=10, pady=10)
                categoria = ctk.CTkEntry(form_window)
                categoria.grid(row=6, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Accesorios", fg_color='#2b2b2b', text_color='white').grid(row=7, column=0, padx=10, pady=10)
                categoria = ctk.CTkEntry(form_window)
                categoria.grid(row=7, column=1, padx=10, pady=10)
                
                ctk.CTkLabel(form_window, text="Vencimiento de Poliza", fg_color='#2b2b2b', text_color='white').grid(row=8, column=0, padx=10, pady=10)
                fecha_poliza = DateEntry(form_window, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
                fecha_poliza.grid(row=8, column=1, padx=10, pady=10)
                
                boton_guardar = ctk.CTkButton(form_window, text="Guardar", fg_color='green', font=('Arial', 18))
                boton_guardar.grid(row=10, column=1, padx=10, pady=10)
    
    
