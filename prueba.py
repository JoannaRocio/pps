import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

# Función que se ejecuta al seleccionar un año
def obtener_anno():
    anno = combo_anno.get()
    print("Año seleccionado:", anno)

# Crear la ventana principal
root = ctk.CTk()

# Título de la ventana
root.title("Seleccionar un Año")

# Crear un frame para la selección de año
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20)

# Crear una lista de años para elegir (por ejemplo, entre 2000 y 2030)
años = [str(year) for year in range(2000, 2031)]

# Crear un ComboBox para seleccionar el año
combo_anno = ttk.Combobox(frame, values=años, state="readonly", width=10)
combo_anno.pack(pady=10)

# Botón para mostrar el año seleccionado
boton = ctk.CTkButton(root, text="Obtener Año", command=obtener_anno)
boton.pack(pady=10)

# Ejecutar el bucle de eventos
root.mainloop()
