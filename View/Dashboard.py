import customtkinter as ctk
from PIL import Image
from Controller.ClienteController import ClienteController  # Asegúrate de que la ruta sea correcta

class Dashboard:
    def __init__(self):
        # Inicialización de la ventana principal
        self.app = ctk.CTk()
        self.app.geometry("1200x800")
        self.app.title("Dashboard Gestoría de Seguros")
        self.app.config(bg='#2b2b2b')

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.app, fg_color='#2b2b2b')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Panel lateral
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200, fg_color='#1e1e1e')
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky='ns', padx=(0, 10))

        # Área de contenido
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color='#2b2b2b')
        self.content_frame.grid(row=0, column=1, sticky='nsew')

        # Configuración de columnas y filas
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # Título
        title = ctk.CTkLabel(self.content_frame, text="Bienvenido a la Gestoría de Seguros", font=('Arial', 24), fg_color='#2b2b2b', text_color='white')
        title.grid(row=0, column=0, padx=20, pady=20)

        # Botones en el panel lateral
        self.create_sidebar_buttons()

        # Logo utilizando CTkImage
        image_path = 'D:\\python\\mvc\\imagenes\\logo.png'  # Cambia la ruta al logo que tengas
        image = Image.open(image_path)
        logo = ctk.CTkImage(light_image=image, dark_image=image)  # Usa la misma imagen para ambos modos
        logo_label = ctk.CTkLabel(self.content_frame, image=logo, text="")
        logo_label.grid(row=2, column=0, pady=20)

    def create_sidebar_buttons(self):
        btn_clients = ctk.CTkButton(self.sidebar, text="Clientes", command=self.show_clients, fg_color='#3b3b3b', font=('Arial', 18))
        btn_clients.pack(pady=10, padx=10, fill='x')

        btn_users = ctk.CTkButton(self.sidebar, text="Usuarios", command=self.manage_users, fg_color='#3b3b3b', font=('Arial', 18))
        btn_users.pack(pady=10, padx=10, fill='x')

        btn_quotes = ctk.CTkButton(self.sidebar, text="Cotizaciones", command=self.generate_quotes, fg_color='#3b3b3b', font=('Arial', 18))
        btn_quotes.pack(pady=10, padx=10, fill='x')

        btn_notifications = ctk.CTkButton(self.sidebar, text="Notificaciones", command=self.notifications, fg_color='#3b3b3b', font=('Arial', 18))
        btn_notifications.pack(pady=10, padx=10, fill='x')

        btn_logout = ctk.CTkButton(self.sidebar, text="Cerrar Sesión", command=self.logout, fg_color='#c0392b', font=('Arial', 18))
        btn_logout.pack(pady=10, padx=10, fill='x')

    def update_content_frame(self, text):
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Limpiar el área de contenido

        label = ctk.CTkLabel(self.content_frame, text=f"Vista de {text}", font=('Arial', 20), fg_color='#2b2b2b', text_color='white')
        label.grid(row=0, column=0, padx=20, pady=20)

        if text == "Clientes":
            cliente_controller = ClienteController()  # Inicializa el controlador de clientes
            cliente_controller.load_view(self.content_frame)  # Asegúrate de que load_view reciba el content_frame

    def show_clients(self):
        self.update_content_frame("Clientes")

    def manage_users(self):
        self.update_content_frame("Usuarios")

    def generate_quotes(self):
        self.update_content_frame("Cotizaciones")

    def notifications(self):
        self.update_content_frame("Notificaciones")

    def logout(self):
        self.app.quit()  # Cierra la aplicación

    def run(self):
        self.app.mainloop()  # Ejecuta la aplicación

# Ejecutar la aplicación
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
