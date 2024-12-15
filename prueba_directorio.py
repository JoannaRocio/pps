import customtkinter as ctk
import os
import subprocess
import platform

class PhotoViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Abrir Carpeta de Imágenes")
        
        # Botón para abrir una carpeta específica
        self.open_folder_button = ctk.CTkButton(root, text="Abrir Carpeta de Imágenes", command=self.open_image_folder)
        self.open_folder_button.grid(row=0, column=0, padx=10, pady=10)

    def open_image_folder(self):
        # Ruta de la carpeta de imágenes (ajústala a la ubicación que necesites)
        folder_path = r"C:\Users\RL\Pictures\Camera Roll"  # Cambia esto por la ruta de tu carpeta
        
        # Verifica el sistema operativo y usa el método adecuado para abrir la carpeta
        if platform.system() == "Windows":
            os.startfile(folder_path)  # Método para abrir carpetas en Windows
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux
            subprocess.run(["xdg-open", folder_path])

if __name__ == "__main__":
    root = ctk.CTk()
    app = PhotoViewerApp(root)
    root.mainloop()
